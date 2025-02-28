from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Function to scrape product details using Selenium with Brave Browser
def scrape_amazon_product_brave(url):
    # Path to Brave Browser executable
    brave_path = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    # Path to ChromeDriver executable
    chromedriver_path = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\chromedriver-win64\\chromedriver.exe"

    # Set up ChromeDriver to use Brave
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path  # Tell Selenium to use Brave Browser

    # Add a custom User-Agent to mimic a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up the ChromeDriver service with the full path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the Amazon product page
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)

    try:
        # Extract the product title
        title_element = driver.find_element(By.ID, "productTitle")
        title = title_element.text.strip()

        # Extract the product price
        price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
        price_fraction_element = driver.find_element(By.CLASS_NAME, "a-price-fraction")
        price = f"{price_element.text.strip()}.{price_fraction_element.text.strip()}"

        # Print the results
        print(f"Product Title: {title}")
        print(f"Product Price: {price}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    product_url = "https://www.amazon.com/dp/B00NLZUM36/"
    scrape_amazon_product_brave(product_url)
