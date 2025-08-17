import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.divan.ru/category/sad-i-dacha"
driver.get(url)
time.sleep(5)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

products = driver.find_elements(By.CSS_SELECTOR, "div.WdR1o")

data = []
for product in products:
    try:
        name = product.find_element(By.CSS_SELECTOR, "div.lsooF span").text
    except:
        name = "Нет названия"
    try:
        price = product.find_element(By.CSS_SELECTOR, "div.pY3d2 span").text
    except:
        price = "Нет цены"
    try:
        link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = "Нет ссылки"

    data.append([name, price, link])

with open("divan_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Название", "Цена", "Ссылка"])
    writer.writerows(data)

driver.quit()
print("Данные сохранены в divan_products.csv")
