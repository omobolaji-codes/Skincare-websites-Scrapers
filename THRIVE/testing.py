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
url = "https://thrivecausemetics.com/collections/all-makeup-skincare-products"  # URL
driver.get(url)
time.sleep(10)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("THRIVE")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Category", "Product", "Description", "Price", "Reviews"]
)  # Append first header row

products = driver.find_elements_by_class_name("tile.tile-product")
for i, product in enumerate(products):
    items = driver.find_elements_by_class_name("tile.tile-product")
    productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
    productName = items[i].find_element_by_class_name("tile-heading").text
    # productCategory = items[i].find_element_by_class_name("card-brand").text
    productPrice = items[i].find_element_by_class_name("price").text
    productReview = items[i].find_element_by_class_name("review-summary").text
    print(productPrice)
    items[i].click()
    time.sleep(10)

    try:
        productDesc = driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/section[1]/div[2]/div[2]").text
    except NoSuchElementException: pass

    productList = [productUrl, "THRIVE", "Category", productName, productDesc,  productPrice, productReview]
    print(productList)
    worksheet.append_row(
        values=productList
    )  # append Category Names and description to worksheet
    driver.back()
    time.sleep(10)
    