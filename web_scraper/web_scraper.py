from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def scroll_down(driver):
    """A method for scrolling the page and collecting producer names."""

    names = set()  # Use a set to avoid duplicates
    producer_pages = []
    itemTargetCount = 20

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while itemTargetCount > len(names):
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3) #Wait for page to load

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
                    names.add(producer_name)

                    producer_page = producer_element.find_element(By.XPATH, f"//a[@class='name ng-star-inserted' and text()=' {producer_name} ']")

                    link = producer_page.get_attribute('href')

                    producer_pages.append(link)

            except NoSuchElementException:
                print("Could not find the link in the element.")

    return list(producer_pages)

def convert_to_number(value):
    if 'k' in value:
        return int(float(value.replace('k', '')) * 1000)
    return int(value)

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
producer_pages = scroll_down(driver)
# Print all collected names
for producer_page in producer_pages:
    driver.get(producer_page)

    time.sleep(5)

    try:
        producer_name = driver.find_element(By.XPATH, "(//h1[text()])[3]").text
        producer_followers = driver.find_element(By.XPATH, "(//span[@class='value ng-star-inserted'])[1]").text
        producer_email = None

        email_found = False

        try:
            producer_email = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]").text
            email_found = True
        except NoSuchElementException as exception_one:
            try:
                view_more = driver.find_element(By.XPATH, "//a[contains(@href, '/about')]")

                view_more.click()

                time.sleep(5)
# Check about me section for email
                about_me = driver.find_element(By.XPATH, "//div[@class='about-me-info vb-margin-b-2xl']").text
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                emails = re.findall(email_pattern, about_me)

                if emails:
                    producer_email = emails[0]
                    email_found = True
            except NoSuchElementException as exception_three:
                email_found = False

        number = convert_to_number(producer_followers)
        integer_to_compare = 100000

        if number <= integer_to_compare:
            print(producer_name)
            print(number)
            if email_found:
                print(producer_email)
            else:
                print("No email found")
            print()
    except NoSuchElementException as exception_two:
        print(f"Element not found: {exception_two}")
    except TimeoutException:
        print(f"Timeout while waiting for an element on {producer_page}")
        
# Quit the driver (optional)
driver.quit()