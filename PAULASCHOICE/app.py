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
url = "https://www.paulaschoice.com/skin-care-products"  # URL
driver.get(url)
time.sleep(10)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("PAULASCHOICE")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Category", "Product", "Description", "Price", "Reviews"]
)  # Append first header row

products = driver.find_elements_by_class_name("ProductTile__HoverWrapper-sc-1da97ke-1.epeFAS")
for i, product in enumerate(products):
    items = driver.find_elements_by_class_name("ProductTile__HoverWrapper-sc-1da97ke-1.epeFAS")
    print(i)
    print(driver.current_url)
    productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
    productName = items[i].find_element_by_class_name("ProductTile__ProductName-sc-1da97ke-6.dewaIO").text
    productCategory = items[i].find_element_by_class_name("ProductTile__Collection-sc-1da97ke-3.kumHNG.rowLayoutClass.medium2.uppercase").text
    print(productCategory)
    productPrice = items[i].find_element_by_class_name("Price__Wrapper-sc-1a08nql-0.dvXtaX").text
    productReview = items[i].find_element_by_class_name("Rating__ReviewsContainer-wawbnr-4.bYWYwE").text
    items[i].click()
    print("clicked")
    time.sleep(10)
# Html__HtmlWrapper-sc-1qeeh0z-0.gLXCkT.format.normalcase
    # <div class="ProductDetailsPage__MobileOnly-sc-1j1lrfq-0 loWfqm"><div class="Html__HtmlWrapper-sc-1qeeh0z-0 gLXCkT  format normalcase">A highly concentrated niacinamide serum that effectively tightens and minimizes the look of sagging pores and rough bumps caused by age or sun damage.<br></div></div>
    try:
        productDesc = driver.find_element_by_class_name("ProductDetailsPage__MobileOnly-sc-1j1lrfq-0.loWfqm").text
    except NoSuchElementException: pass

    productList = [productUrl, "PAULASCHOICE", productCategory, productName,  productDesc, productPrice, productReview]
    print(productList)
    worksheet.append_row(
        values=productList
    )  # append Category Names and description to worksheet
    driver.back()
    time.sleep(10)

# <div class="Rating__ReviewsContainer-wawbnr-4 bYWYwE"><span class="Rating__Reviews-wawbnr-5 iserSH tiny1 normalcase">10 reviews</span></div>
    # <div class="Html__HtmlWrapper-sc-1qeeh0z-0 gLXCkT  format normalcase">A essential skincare routine replenishes moisture to combat dryness while refining the appearance of wrinkles and skin tone for a younger, revitalized-looking appearance.</div>