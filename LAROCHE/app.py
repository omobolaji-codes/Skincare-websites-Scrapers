from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
sh = gc.open("LAROCHE")
worksheet = sh.sheet1
worksheet.append_row(
    values=["Category", "Brand", "URL", "Product", "Description", "Price"]
)  # Append first header row
url = "https://www.laroche-posay.us/shop-by/view-all-product-lines"  # URL
driver.get(url)
time.sleep(10)

shopBy = driver.find_element_by_css_selector("#lrp-primary-nav > li.has-children.level_1_list_item.menu_list_item_4")
hover = ActionChains(driver).move_to_element(shopBy)
hover.perform()
time.sleep(10)

# categories = driver.find_element_by_css_selector("#lrp-primary-nav > li.has-children.level_1_list_item.menu_list_item_4 > div.custom_navigation_slot_1 > div > ul > li:nth-child(3)")
categories = driver.find_elements_by_class_name("category")
for i, category in enumerate(categories):
    items = driver.find_elements_by_class_name("category")
    categoryName = items[i].find_element_by_tag_name("h2").text

    categoryList = [categoryName]
    worksheet.append_row(values = categoryList)
    print("items length", len(items))
    print(categoryList)
    time.sleep(5)

    products = category.find_elements_by_class_name("product_tile_wrapper")
    for j, product in enumerate(products):
        elements = category.find_elements_by_class_name("product_tile_wrapper")
        itemUrl = elements[j].find_element_by_tag_name("a").get_attribute("href")
        itemName = elements[j].find_element_by_class_name("product_name").text

        try:
            itemDesc = elements[j].find_element_by_class_name("product_description").text
        except NoSuchElementException: pass

        itemPrice = elements[j].find_element_by_class_name("price.b-price").text

        itemList = [" ", "Laroche-Posay", itemUrl, itemName, itemDesc, itemPrice]
        worksheet.append_row(values = itemList)
        time.sleep(5)
        print(itemList)
    