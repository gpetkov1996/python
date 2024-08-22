from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_down(driver):
    """A method for scrolling the page and collecting producer names."""

    names = []  # Use a set to avoid duplicates
    itemTargetCount = 50

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while itemTargetCount > len(names):
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

        # Find producer elements by CSS selector
        producer_elements = driver.find_elements(By.CSS_SELECTOR, '#app-body > mp-root > div > div > ng-component > mp-search-v3 > div > div > section > mp-search-results > mp-list-card-member > mp-list-card-template > div > mp-card-figure-member')

        for producer_element in producer_elements:
            try:
                producer_name = producer_element.find_element(By.CLASS_NAME, 'card-figure').text.split('\n', 1)[0].strip()
                if producer_name not in names:
                    names.append(producer_name)
            except NoSuchElementException:
                print("Could not find the link in the element.")

    return list(names)

# For keeping the browser open after the script runs
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Create a Service object to manage the ChromeDriver
service = Service(ChromeDriverManager().install())

# Initialize the Chrome WebDriver with the service
driver = webdriver.Chrome(options=options, service=service)

# Open the website
web = 'https://www.beatstars.com/search?type=musicians'
driver.get(web)

# Wait until the elements are loaded (use WebDriverWait for dynamic content)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
)

accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
accept_button.click()

# Wait until the elements are loaded (use WebDriverWait for dynamic content)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'card-figure'))
)

# Scroll down and collect names
producer_names = scroll_down(driver)

# Print all collected names
for name in producer_names:
    print(name)

# Quit the driver (optional)
driver.quit()
