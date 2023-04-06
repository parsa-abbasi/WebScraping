__author__ = "Parsa Abbasi"
__email__ = "parsa.abbasi1996@gmail.com"
__organization__ = "Quera"
__website__ = "https://parsa-abbasi.github.io/"
__version__ = "1.0.1"
__date__ = "2023-04-04"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
# options.headless = True
driver = webdriver.Chrome(options=options)

driver.maximize_window()

driver.get("https://duckduckgo.com/")

# fill the input field with the search query
search_query = 'quera'
driver.find_element(By.ID, 'searchbox_input').send_keys(search_query)

driver.implicitly_wait(5)
time.sleep(4)

# click on search button
driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search"]').click()

time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'a.result--more__btn').click()
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'a.result--more__btn').click()
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# find all the result links
result_links = driver.find_elements(By.CSS_SELECTOR, '.nrn-react-div h2 a')

# scroll to each result link
for link in result_links:
    driver.execute_script("arguments[0].scrollIntoView();", link)
    print(link.get_attribute('href'))
    time.sleep(1)

time.sleep(3)
driver.quit()