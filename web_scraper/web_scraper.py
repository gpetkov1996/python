from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_and_collect_elements(driver, class_name):
    """Scrolls the page and collects elements with the specified class name."""
    elements = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down by a small amount.
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for new content to load.

        # Collect elements.
        new_elements = driver.find_elements(By.CLASS_NAME, class_name)
        elements.update(new_elements)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(elements)

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

# Scroll and collect elements
producer_elements = scroll_and_collect_elements(driver, 'card-figure')
names = [element.text for element in producer_elements]

# Print the names of the producers
for name in names:
    try:
        producer_name = name.split('\n', 1)[0]
        print(producer_name)
    except NoSuchElementException:
        print("Could not find the name in the element.")

# Quit the driver (optional)
driver.quit()
