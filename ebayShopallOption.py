import time
import requests
from bs4 import BeautifulSoup
from modulePackage import *
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://www.ebay.com/"

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

driver.get(url)

# shopAllcategory = driver.find_element(by=By.ID, value = 'gh-shop-ei')
# shopAllcategory.click()
#
# time.sleep(10)
#
# driver.quit()

# Wait for the 'shopAllcategory' element to be clickable and click it
wait = WebDriverWait(driver, 10)
shop_all_category = wait.until(EC.element_to_be_clickable((By.ID, 'gh-shop-ei')))
shop_all_category.click()

# Wait for the content to be visible (update the selector as needed based on the page structure)
# For example, let's assume there's a container with ID 'shop-categories' that holds the content
content_container = wait.until(EC.visibility_of_element_located((By.ID, 'gh-shop-see-all')))
content_container.click()

pageSource = driver.current_url
driver.quit()

print(pageSource)
soup = get_soup(pageSource, headers=HEADERS)
csv_file = "ebaysubsubmainlinksContent"
all_data = []

mainCategoriesContent = soup.find_all('div', class_='cat-container')

for topCat in mainCategoriesContent:
        print(topCat.find('h2').text.strip()+"------>/n")
        ebayMainCat = topCat.find('h2').text.strip()
        subCatCont = topCat.find_all('div', class_='sub-cat-container')
        for subcat in subCatCont:
                print(subcat.find('h3').text.strip())
                ebaySubMenuCat = subcat.find('h3').text.strip()
                subCatMenuUls = subcat.find_all('ul', class_='sub-cats')
                for subCatMenu in subCatMenuUls:
                        subCatMenus = subCatMenu.find_all('a')
                        for link in subCatMenus:
                                if(link.get('title', '')):
                                        dictionary = {
                                                'E_Bay_Main_Category': ebayMainCat,
                                                'E_Bay_Sub_Menu_cat': ebaySubMenuCat,
                                                'E_bay_sub_sub_cat_menu': link['title'],
                                                'Ebay_sub_sub_cat_links': link['href']
                                        }
                                        all_data.append(dictionary)
                                        ebayMenus = pd.DataFrame(all_data)
                                        output_dir = r'D:\python\ebayProject'
                                        if not os.path.exists(output_dir):
                                                os.makedirs(output_dir)
                                        file_path = os.path.join(output_dir, f'{csv_file}.csv')
                                        ebayMenus.to_csv(file_path, index=False)