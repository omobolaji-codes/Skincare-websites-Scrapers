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
url = "https://www.neosporin.com/products"  # URL
driver.get(url)
time.sleep(20)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("NEOSPORIN")
worksheet = sh.sheet1
worksheet.append_row(
    values=["BRAND", "TYPE", "URL", "NAME", "DESCRIPTION", "PRICE"]
)  # Append first header row


categories = driver.find_elements_by_class_name("panel-pane.pane-taco-pane.taco-polls.vertical.one-third")
for i, category in enumerate(categories):
    print(category)
    print(driver.current_url)
    sections = driver.find_elements_by_class_name("panel-pane.pane-taco-pane.taco-polls.vertical.one-third")

    categoryUrl = sections[i].find_element_by_tag_name("a").get_attribute("href")
    categoryName = sections[i].find_element_by_class_name("field-item.even").text
    Name = categoryName.split(" ", maxsplit=1)[1]
    sectionList = ["NEOSPORIN", "Category", categoryUrl, Name]
    worksheet.append_row(
        values=sectionList
    )  # append Category Names and description to worksheet

    click_ = sections[i].find_element_by_class_name("field-item.even")
    click_.click()
    print("clicked")
    time.sleep(10)

    products = driver.find_elements_by_class_name("node.node--product.node--product-short.node--product--product-short.clearfix")
    for j, product in enumerate(products):
        print(driver.current_url)
        products_ = driver.find_elements_by_class_name("node.node--product.node--product-short.node--product--product-short.clearfix")
        productUrl = products_[j].find_element_by_tag_name("a").get_attribute("href")
        productName = products_[j].find_element_by_class_name("node__title").text
        print(productUrl, "bhsbif", productName)

        productClicks = driver.find_elements_by_class_name("node__title")
        # print("product clicks", productClicks[j])
        for productclick in productClicks:
            productClicks_ = driver.find_elements_by_class_name("node__title")
            productClicks_[j].click()
            print("product clicked")
            time.sleep(10)
            print(driver.current_url)
            productDesc = driver.find_element_by_css_selector("#description > li > div > div > div > p:nth-child(1)").text
            try:
                
                productPrice = driver.find_element_by_css_selector("#walmartcom > div.retail-price").text
            except NoSuchElementException:
                productPrice = " "
            productList = ["NEOSPORIN", "Product", productUrl, productName, productDesc, productPrice]
            print(productList)
            worksheet.append_row(values=productList)
            driver.back()
            time.sleep(10)
            break

    driver.back()
    time.sleep(10)