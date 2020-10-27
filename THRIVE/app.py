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
sh = gc.open("THRIVE")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Product", "Description", "Price", "Reviews"]
)  # Append first header row

url = "https://thrivecausemetics.com/collections/all-makeup-skincare-products"
driver.get(url)
time.sleep(10)

num_pages = 3
for j in range(num_pages):
    products = driver.find_elements_by_class_name("tile.tile-product")
    for i, product in enumerate(products):
        time.sleep(8)
        items = driver.find_elements_by_class_name("tile.tile-product")
        productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
        driver.get(productUrl)
        time.sleep(10)

        try:
            productName = driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/section[1]/div[1]/h1").text
            productDesc = driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/section[1]/div[2]/div[2]").text
            productPrice = driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/section[1]/div[1]/div").text
            productReview = driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/section[1]/a/span").text
        except NoSuchElementException: 
            productReview = " "
            pass

        productList = [productUrl, "THRIVE CAUSEMETICS", productName, productDesc,  productPrice, productReview]
        print(productList)
        worksheet.append_row(values=productList)

        driver.back()
        time.sleep(10)
    nextpage = driver.find_element_by_css_selector("#js-pagination > li.page-item.next > a")
    print(nextpage.text)
    nextpage.click()
    time.sleep(10)