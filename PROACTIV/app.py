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
url = "https://www.proactiv.com/en_us/our-products.html"  # URL
driver.get(url)
time.sleep(10)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("PROACTIV")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Product", "Description", "Price"]
)  # Append first header row


#Number 1
product1 = driver.find_element_by_class_name("proactivmd-text.large-7.medium-7.small-12.float-left.column")
productUrl = product1.find_element_by_tag_name("a").get_attribute("href")
productDesc1 = product1.find_element_by_tag_name("h2").text
productDesc2 = product1.find_element_by_css_selector("#main > div:nth-child(3) > div > div.proactivmd > div > div.proactivmd-text.large-7.medium-7.small-12.float-left.column > p:nth-child(3) > strong").text
productDesc = productDesc1 + "; " + productDesc2
orderNow = driver.find_element_by_class_name("large-5.medium-6.small-12.float-left.column.no-padding-left")

orderNow.click()
productPrice = driver.find_element_by_class_name("old-price-value").text
time.sleep(8)
productList = [productUrl, "PROACTIV", "proactivMD", productDesc, productPrice]
worksheet.append_row(values=productList)
print(productList)
driver.back()
time.sleep(10)


#Number 2
product2 = driver.find_element_by_class_name("proactiv-text.large-7.medium-7.small-12.float-left.column")
productUrl2 = product2.find_element_by_tag_name("a").get_attribute("href")
productDesc3 = product2.find_element_by_tag_name("h2").text
productDesc4 = product2.find_element_by_css_selector("#main > div:nth-child(3) > div > div.proactiv > div > div.proactiv-text.large-7.medium-7.small-12.float-left.column > p:nth-child(3) > strong").text
productDesc_ = productDesc3 + "; " + productDesc4

orderNow2 = driver.find_element_by_class_name("large-5.medium-6.small-12.float-left.column.no-padding-left")
orderNow2.click()
productPrice2 = driver.find_element_by_css_selector("#system > div.slider.slider-active-elements.row > div > div.owl-wrapper-outer > div > div:nth-child(2) > div > div > div.large-12.medium-12.columns.brand-pseudo > div.brand-wrap-content.large-8.medium-7.columns > div.product-price > div.hide-for-small-only > div > h2 > span").text
time.sleep(8)
productList2 = [productUrl2, "PROACTIV", "proactiv", productDesc_, productPrice2]
worksheet.append_row(values=productList2)
print(productList2)
driver.back()
time.sleep(10)


#Number3
product3 = driver.find_element_by_class_name("proactivplus-text.large-7.medium-7.small-12.float-left.column")
productUrl3 = product3.find_element_by_tag_name("a").get_attribute("href")
productDesc5 = product3.find_element_by_tag_name("h2").text
productDesc6 = product3.find_element_by_css_selector("#main > div:nth-child(3) > div > div.proactivplus > div > div.proactivplus-text.large-7.medium-7.small-12.float-left.column > p:nth-child(3) > strong").text
productDesc__ = productDesc5 + "; " + productDesc6

orderNow3 = driver.find_element_by_class_name("large-5.medium-6.small-12.float-left.column.no-padding-left")
orderNow3.click()
productPrice3 = driver.find_element_by_css_selector("#system > div.slider.slider-active-elements.row > div > div.owl-wrapper-outer > div > div:nth-child(3) > div > div > div.large-12.medium-12.columns.brand-pseudo > div.brand-wrap-content.large-8.medium-7.columns > div.product-price > div.hide-for-small-only > div > h2 > span").text
time.sleep(8)
productList3 = [productUrl3, "PROACTIV", "proactiv+", productDesc__, productPrice3]
worksheet.append_row(values=productList3)
print(productList3)
driver.back()
time.sleep(10)