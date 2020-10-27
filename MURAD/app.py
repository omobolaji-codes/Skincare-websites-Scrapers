from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)
import time
import gspread  # Gspread to access google sheets


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
DRIVER_PATH = r"chromedriver"
options.binary_location = (
    r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
)
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("MURAD")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Category", "Brand", "Product", "Description", "Size", "Price"]
)  # Append first header row

url = "https://www.murad.com/skincare/bestsellers-c/"  # URL
driver.get(url)
time.sleep(8)

numPages = 3
for j in range(numPages):
    products = driver.find_elements_by_class_name("product")
    for i, product in enumerate(products):
        items = driver.find_elements_by_class_name("product")
        
        productName = items[i].find_element_by_class_name("h6.card-title").text
        productSize = items[i].find_element_by_class_name("size").text
        productPrice = items[i].find_element_by_class_name("price.price--withoutTax").text

        productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
        driver.get(productUrl)
        time.sleep(15)

        try:
            productDesc = driver.find_element_by_class_name("productView-short-description").text
        except NoSuchElementException: pass

        productList = [productUrl, "Skincare", "Murad", productName, productDesc, productSize, productPrice]
        print(productList)
        worksheet.append_row(
            values=productList
        )  # append Category Names and description to worksheet

        driver.back() #go back to previous page
        time.sleep(10)
    
    #access next page
    page = driver.find_element_by_css_selector("#product-listing-container > div.pagination > ul > li.pagination-item.pagination-item--next > a").get_attribute("href")
    print(page)
    driver.get(page)
    time.sleep(10)