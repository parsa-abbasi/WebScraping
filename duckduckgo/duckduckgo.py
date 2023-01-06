from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get("https://duckduckgo.com/")

search_query = 'quera'
driver.find_element(By.ID, 'search_form_input_homepage').send_keys(search_query)
driver.find_element(By.ID, "search_button_homepage").click()

result_links = driver.find_elements(By.CSS_SELECTOR, '.nrn-react-div h2 a')
for r in result_links:
    print(r.get_attribute('href'))

driver.quit()