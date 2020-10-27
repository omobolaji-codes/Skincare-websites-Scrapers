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
url = "https://us.laneige.com/collections/all-products"  # URL
driver.get(url)
time.sleep(12)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("LANEIGE")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Category", "Product", "Description", "Price"]
)  # Append first header row

loadMore = driver.find_element_by_css_selector("#MainContent > article > div.js-collection-filter-sort > div.collection__pagination > a")
time.sleep(5)
loadMore.click()
time.sleep(5)
loadMore.click()
time.sleep(8)
products = driver.find_elements_by_class_name("product-tile.availability--in-stock.price--regular.product-tile--grid")
for i, product in enumerate(products):
    print(driver.current_url)
    items = driver.find_elements_by_class_name("product-tile.availability--in-stock.price--regular.product-tile--grid")
    print("length items",len(items))
    productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
    productCategory = items[i].find_element_by_class_name("product-tile__subtitle").text
    productName = items[i].find_element_by_class_name("product-tile__title").text
    productPrice = items[i].find_element_by_class_name("pricing").text
    
    click_ = driver.find_elements_by_class_name("product-tile__image")
    print("All click elements", len(click_))
    click_[i].click()
    time.sleep(8)
    print("clicked")
    productDesc = driver.find_element_by_class_name("product__description").text  
    productList = [productUrl, "LANEIGE", productCategory, productName, productDesc, productPrice]
    print(productList)
    worksheet.append_row(
        values=productList
    )  # append Category Names and description to worksheet
    driver.back()
    time.sleep(15)
    
    loadMore = driver.find_element_by_css_selector("#MainContent > article > div.js-collection-filter-sort > div.collection__pagination > a")
    loadMore.click()
    time.sleep(5)
    loadMore.click()
    time.sleep(8)