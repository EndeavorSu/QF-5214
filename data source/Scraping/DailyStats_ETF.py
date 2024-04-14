from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

driver.get('https://www.sse.com.cn/assortment/options/date/')
try:
    driver.implicitly_wait(30)
    # element = driver.find_element(By.CLASS_NAME, "sse_searchContainer")
    element = driver.find_element(By.CSS_SELECTOR, ".table.table-hover ")
    thead = driver.find_element(By.TAG_NAME,"thead")
    header = thead.find_element(By.TAG_NAME, "tr")
    tbody = element.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    header1 = header.text.replace("\n", "").split(' ')

    row_arr = []
    for r in rows:
        new_row = r.text.split(' ')
        row_arr.append(new_row)

    df = pd.DataFrame(row_arr, columns=header1)
    print(df)

finally:
    driver.quit()