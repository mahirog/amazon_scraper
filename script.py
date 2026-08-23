from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


def human_sleep(min_sec=1.5, max_sec=4.0):
    time.sleep(random.uniform(min_sec, max_sec))


def human_scroll(driver, direction="down", intensity="normal"):
    scroll_amounts = {
        "light": (100, 300),
        "normal": (300, 700),
        "heavy": (600, 1200),
    }
    lo, hi = scroll_amounts.get(intensity, (300, 700))
    amount = random.randint(lo, hi)
    if direction == "up":
        amount = -amount
    driver.execute_script(f"window.scrollBy(0, {amount});")
    human_sleep(0.5, 1.5)


def move_mouse_naturally(driver, element):
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(-200, 200), random.randint(-100, 100))
    actions.perform()
    human_sleep(0.2, 0.6)
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(
        element,
        random.randint(-10, 10),
        random.randint(-5, 5)
    )
    actions.perform()
    human_sleep(0.3, 0.8)


def simulate_reading(driver, duration=None):
    if duration is None:
        duration = random.uniform(3, 8)
    end_time = time.time() + duration
    while time.time() < end_time:
        scroll_chance = random.random()
        if scroll_chance < 0.4:
            human_scroll(driver, "down", random.choice(["light", "normal"]))
        elif scroll_chance < 0.5:
            human_scroll(driver, "up", "light")
        human_sleep(0.8, 2.5)


def scrape_amazon_product_brave(url):
    brave_path = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    chromedriver_path = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\chromedriver-win64\\chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.binary_location = brave_path

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """
    })

    try:
        driver.get("https://www.amazon.com")
        human_sleep(2.5, 4.5)

        try:
            wait = WebDriverWait(driver, 8)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            move_mouse_naturally(driver, search_box)
            human_sleep(0.4, 0.9)

            dummy_searches = ["mechanical keyboard", "laptop stand", "usb hub"]
            dummy_query = random.choice(dummy_searches)
            for char in dummy_query:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))

            human_sleep(0.8, 1.8)
            search_box.clear()
            human_sleep(0.3, 0.7)
        except Exception:
            pass

        human_sleep(1.0, 2.5)

        driver.get(url)
        human_sleep(3.0, 6.0)

        simulate_reading(driver, duration=random.uniform(4, 9))

        wait = WebDriverWait(driver, 15)

        title_element = wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
        move_mouse_naturally(driver, title_element)
        human_sleep(0.5, 1.2)
        title = title_element.text.strip()

        human_scroll(driver, "down", "normal")
        human_sleep(1.0, 2.5)

        price_whole = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole")))
        move_mouse_naturally(driver, price_whole)
        human_sleep(0.3, 0.8)

        price_fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction")
        price = f"{price_whole.text.strip()}.{price_fraction.text.strip()}"

        human_sleep(1.5, 3.0)
        simulate_reading(driver, duration=random.uniform(2, 5))

        print(f"Product Title: {title}")
        print(f"Product Price: ${price}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        human_sleep(1.5, 3.5)
        driver.quit()


if __name__ == "__main__":
    product_url = "https://www.amazon.com/dp/B00NLZUM36/"
    scrape_amazon_product_brave(product_url)
