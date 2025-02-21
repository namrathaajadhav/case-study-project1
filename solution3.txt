# -*- coding: utf-8 -*-
from selenium import webdriver
import logging
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def save_to_txt(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' has been saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def solution3(url, max_hits=5):
    hits = 0  # Counter to track the number of actions (hits)
    
    try:
        # Define the headers
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=nlx0rq1wt2uioy0ptfjbvlps; 46455243=939669258.47873.0000',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://forms.ferc.gov/'
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

        # Wait until the body tag is present in the page source
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # ==================Logic=========
        # Attempting to click first button
        try:
            time.sleep(2)
            if hits >= max_hits:
                print(f"Limit of {max_hits} hits reached. Stopping further actions.")
            script = "document.querySelector('#LinkButton1').click()"
            driver.execute_script(script)
            time.sleep(5)
            hits += 1
        except Exception as e:
            print(f"Error in click action: {e}")
        
        # Check if main table contains SHA256 and extract the text
        try:
            if hits >= max_hits:
                print(f"Limit of {max_hits} hits reached. Stopping further actions.")
            main_table = driver.find_element(By.CSS_SELECTOR, '#Content1_TableViewer')
            if "SHA256" in main_table.text or "SHA-256" in main_table.text or "256" in main_table.text:
                text_area = main_table.find_element(By.CSS_SELECTOR, '[id*="ViewSHA256"]')
                save_to_txt(filename="sha256.txt", content=text_area.text)
                hits += 1
        except Exception as error:
            print(f"Error in extracting SHA256: {error}")

        if hits >= max_hits:
            print(f"Limit of {max_hits} hits reached. Stopping further actions.")

    except WebDriverException as e:
        if "net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("Error: Internet disconnected. Please check your internet connection.")
        else:
            print(f"Error: {str(e)}")

    finally:
        # Ensure that the WebDriver is closed, even if an exception occurs
        if 'driver' in locals():
            driver.quit()


if __name__ == '__main__':
    url = "https://forms.ferc.gov/"
    solution3(url)