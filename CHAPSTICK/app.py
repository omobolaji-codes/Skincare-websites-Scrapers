#CHAPSTICK
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)
import requests
import time
import gspread  # Gspread to access google sheets


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
DRIVER_PATH = r"chromedriver"
options.binary_location = (
    r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
)



mla_profile_id = "5a87328c-c658-402d-823c-915537215b3e"  
mla_url = "http://localhost.multiloginapp.com:35000/api/v1/profile/start?automation=true&profileId={}".format(
    mla_profile_id
)
resp = requests.get(mla_url).json()
print(resp)
driver = webdriver.Remote(command_executor=resp["value"], options=options)



# driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
url = "https://www.chapstick.com/shop"  # URL
driver.get(url)
time.sleep(10)

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("CHAPSTICK")
worksheet = sh.sheet1
worksheet.append_row(
    values=["URL", "Brand", "Category", "Product", "Description", "Price"]
)  # Append first header row

products = driver.find_elements_by_class_name("product")
for i, product in enumerate(products):
    items = driver.find_elements_by_class_name("product")
    productUrl = items[i].find_element_by_tag_name("a").get_attribute("href")
    productName = items[i].find_element_by_class_name("card-title").text
    productCategory = items[i].find_element_by_class_name("card-brand").text
    productPrice = items[i].find_element_by_class_name("price-section.price-section--withoutTax").text
    print(productPrice)
    items[i].click()
    time.sleep(15)
    try:
        productDesc = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/section[4]/p").text
    except NoSuchElementException: pass
    driver.back()
    time.sleep(8)
    productList = [productUrl, "Chapstick", productCategory, productName, productDesc,  productPrice]
    print(productList)
    # worksheet.append_row(
    #     values=productList
    # )  # append Category Names and description to worksheet