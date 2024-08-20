from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


# Find producer elements by class name
producer_elements = driver.find_elements(By.CLASS_NAME, 'card-figure')
names = [producer_element.text for producer_element in producer_elements]

# Iterate over each producer element and get the name of the producer
for name in names:
    try:
        producer_name = name.split('\n', 1)[0]
        print(producer_name)
    except NoSuchElementException:
        print("Could not find the name in the element.")

# Quit the driver (optional)
driver.quit()