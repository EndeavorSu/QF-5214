from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


import time

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

driver.get('https://www.sse.com.cn/assortment/options/disclo/preinfo/')

try:
    driver.implicitly_wait(300)
    element = driver.find_element(By.CSS_SELECTOR, ".sse_colContent.js_preinfo")
    counter = 0
    while True:
        counter += 1
        print(counter)

        pages = element.find_element(By.XPATH, "//div[@class='pagination-box']//ul")
        table = element.find_element(By.XPATH, "//div[@class='table-responsive ']//table[@class='table table-hover ']")
        thead = table.find_element(By.TAG_NAME, "thead")
        print(thead.text)
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for r in rows:
            print(r.text)
        next_page = pages.find_elements(By.TAG_NAME, "li")[-1]
        if next_page.get_attribute("class") == "next":
            actions = ActionChains(driver)
            actions.move_to_element(next_page).click().perform()
            time.sleep(5)

        else:
            print("The End")
            break

finally:
    driver.quit()
