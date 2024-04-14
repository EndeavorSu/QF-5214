from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

driver.get('https://www.sse.com.cn/assortment/options/price/')

try:

    driver.implicitly_wait(300)
    element = driver.find_element(By.CSS_SELECTOR, ".sse_outerItem.search_radio.js_code")
    table_div = driver.find_element(By.CSS_SELECTOR, ".sse_colContent.js_quotesMonDetail")
    contracts = element.find_elements(By.TAG_NAME, "i")

    contract_month = driver.find_element(By.CSS_SELECTOR, ".dropdown.bootstrap-select")
    # button = contract_month.find_element(By.TAG_NAME, "button")
    select = Select(contract_month.find_element(By.TAG_NAME, "select"))
    for c in contracts:
        print()
        actions = ActionChains(driver)
        actions.move_to_element(c).click().perform()
        # c.click()
        time.sleep(5)
        for option in contract_month.find_elements(By.XPATH, "//select[@class='selectpicker']//option"):
            # print(option.get_attribute("value"))
            select.select_by_value(option.get_attribute("value"))
            time.sleep(5)
            table = table_div.find_element(By.XPATH, "//div[contains(@class, 'table-responsive sse_table_T02')]//table[contains(@class, 'table table-hover ')]")
            thead = table.find_element(By.TAG_NAME, "thead")
            thead_row = thead.find_elements(By.TAG_NAME, "tr")
            for r in thead_row:
                print(r.text)
            tbody = table.find_element(By.TAG_NAME, "tbody")
            tbody_row = tbody.find_elements(By.TAG_NAME, "tr")
            for r in tbody_row:
                print(r.text)

finally:
    driver.quit()