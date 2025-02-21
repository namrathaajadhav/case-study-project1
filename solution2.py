# -*- coding: utf-8 -*-
from selenium import webdriver
import logging
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os




def save_to_excel(df, filename='scraped_data.xlsx'):
    """Function to save DataFrame to Excel, appending if file exists"""
    if os.path.exists(filename):
        # If file exists, append the data
        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, sheet_name='Sheet1')
        print(f"Data appended to '{filename}'")
    else:
        # If file does not exist, create a new one
        df.to_excel(filename, index=False)
        print(f"Data saved to '{filename}'")


def visit_next_page(driver):
    """Function to visit the next page using a button click."""
    time.sleep(5)  # Wait before clicking
    driver.execute_script("document.querySelector('[id*=\"DXPagerBottom_PBN\"]').click()")
    # Wait for the table to load on the new page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table[id*='DXMainTable']")))


def solution2(url):
    try:
       # Define the headers
        headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'no-cache',
  'cookie': 'ASP.NET_SessionId=enhnwrkco3qg1lhwta2pkcxh; SessionStart=2/17/2025 9:41:22 AM; LastController=RenewableGeneratorsRegisteredinGATS/Index; LastControllerTime=2/17/2025 9:41:29 AM',
  'pragma': 'no-cache',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
  'referer': 'https://gats.pjm-eis.com/gats2/PublicReports/RenewableGeneratorsRegisteredinGATS',
  'dxcss': '1_208,100_1707,1_66,1_207,100_1712,1_205,1_204,100_1807,100_1812,1_72,1_71,100_1716,100_1721,1_82,100_1683',
  'dxscript': '1_9,1_10,1_253,1_21,1_62,1_11,1_12,1_13,1_14,1_18,1_181,1_182,1_183,1_19,1_20,14_0,1_180,14_24,1_203,14_25,1_192,14_18,1_201,14_20,1_186,1_188,1_196,1_15,1_39,1_197,1_198,1_202,1_184,1_191,14_17,14_22,1_190,14_19,1_59,1_193,1_187,14_16,1_195,1_38,1_189,14_43,1_200,1_194,14_21,1_17,1_211,1_224,1_225,1_226,1_210,1_218,1_214,1_219,1_220,1_215,1_221,1_216,1_217,1_212,1_222,1_223,1_209,1_228,1_237,1_239,1_240,1_227,1_232,1_233,1_234,1_213,1_229,1_230,1_231,1_235,1_236,1_238,1_241,14_49,14_50,14_2,1_22,1_31,1_32,1_37,14_12,14_9,1_251,14_1,10_0,10_1,10_2,10_3,10_4,14_23',
  'x-requested-with': 'XMLHttpRequest'
}

        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        
        # Add headers to the Chrome options
        for key, value in headers.items():
            chrome_options.add_argument(f'--header={key}: {value}')

        # Disable DevTools protocol message
        chrome_options.add_argument('--disable-dev-shm-usage')  # Prevents DevTools from starting
        # Additional options to mimic human-like behavior
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation features
        chrome_options.add_argument('--disable-extensions')  # Disable extensions
        chrome_options.add_argument('--disable-notifications')  # Disable notifications
        chrome_options.add_argument('--disable-popup-blocking')

         # Set logging level to ERROR to suppress INFO and WARNING messages
        logging.getLogger('WDM').setLevel(logging.ERROR)

        chrome_options.add_argument('--headless')  # Headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration when in headless mode
        chrome_options.add_argument('--incognito')  # Incognito mode
        chrome_options.add_argument('--disable-extensions')  # Disable extensions
        chrome_options.add_argument('--disable-notifications')  # Disable notifications
        chrome_options.add_argument('--disable-popup-blocking')  # Disable pop-up blocking
        
        # Create a Chrome webdriver with the configured options
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='dxp-num']")))

        # Define the maximum page hits
        max_hits = 5
        page_hit_counter = 0
        
        end_page = 400
        start_page = 200

        # Loop through pages
        table_data = list()
        for page_num in range(end_page + 1):
            if page_num <= start_page:  # skip first page
                print(f"Skipping==={page_num}===========")
                visit_next_page(driver)
            else:
                # Ensure we do not exceed max hits
                if page_hit_counter >= max_hits:
                    print("Maximum page hit limit reached. Stopping scraping.")
                    break

                # Fetch the table and rows for each page to avoid stale element reference
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table[id*='DXMainTable']")))
                table = driver.find_element(By.CSS_SELECTOR, "table[id*='DXMainTable']")
                headers = table.find_elements(By.CSS_SELECTOR, "td[class*='dxgvHeader'] td[id*='tcheader']")
                header_names = [header.text.strip() for header in headers]

                # Fetch rows on the current page
                rows = table.find_elements(By.CSS_SELECTOR, "tr[class*='dxgvDataRow']")

                # Loop through each row and extract data
                for row in rows:
                    try:
                        cells = row.find_elements(By.CSS_SELECTOR, 'td')
                        row_data = [cell.text.strip() for cell in cells]
                        if row_data:
                            print(row_data)
                            table_data.append(row_data)
                    except StaleElementReferenceException:
                        continue

                # Optionally, convert to DataFrame after the page is done
                df = pd.DataFrame(table_data, columns=header_names)
                # Save or append DataFrame to Excel
                save_to_excel(df, 'scraped_data.xlsx')

                # Increment page hit counter
                page_hit_counter += 1
                print(f"Page hit {page_hit_counter}/{max_hits}")

                visit_next_page(driver)

                print("================================================")
                print(df)

    except WebDriverException as e:
        if "net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("Error: Internet disconnected. Please check your internet connection.")
        else:
            print(f"Error: {str(e)}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    url = "https://gats.pjm-eis.com/gats2/PublicReports/RenewableGeneratorsRegisteredinGATS"
    solution2(url)
