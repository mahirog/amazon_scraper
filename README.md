# Amazon Product Scraper (Brave + Selenium)

A human-behavior-emulating Amazon product scraper built with Selenium and Brave Browser. Randomized delays, natural mouse movement, scroll simulation, and bot-fingerprint erasure make requests indistinguishable from a real user session.

---

## Features

- Launches Brave Browser via ChromeDriver
- Rotates User-Agent strings across recent Chrome versions
- Erases `navigator.webdriver` and other automation fingerprints via CDP
- Warms up with an Amazon homepage visit before hitting the product URL
- Randomized sleep intervals — no fixed delays
- Natural mouse movement with offset jitter before interacting with elements
- Scroll-based reading simulation while the page is open
- Saves results to both `product_details.csv` and `product_details.txt`

---

## Requirements

- Python 3.8+
- Brave Browser installed
- ChromeDriver matching your Brave version (placed alongside Brave's executable)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Find your Brave version

Open Brave and go to `brave://version`. Note the version number (e.g. `124.0.6367.82`).

### 2. Download the matching ChromeDriver

Go to https://googlechromelabs.github.io/chrome-for-testing/ and download the ChromeDriver that matches your Brave version.

Extract it and place the `chromedriver.exe` inside:

```
C:\Users\mehed\AppData\Local\BraveSoftware\Brave-Browser\Application\chromedriver-win64\
```

### 3. Verify paths in the script

Open `scraper.py` and confirm these two paths match your machine:

```python
brave_path      = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
chromedriver_path = "C:\\Users\\mehed\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\chromedriver-win64\\chromedriver.exe"
```

---

## Usage

```bash
python scraper.py
```

By default it scrapes:

```
https://www.amazon.com/dp/B00NLZUM36/
```

To scrape a different product, change the URL at the bottom of the script:

```python
if __name__ == "__main__":
    product_url = "https://www.amazon.com/dp/YOUR_ASIN_HERE/"
    scrape_amazon_product_brave(product_url)
```

---

## Output

Results are written to two files in the project directory:

| File | Format | Contents |
|---|---|---|
| `product_details.csv` | CSV | title, price, URL, timestamp — one row per run |
| `product_details.txt` | Plain text | Human-readable log of each scrape session |

---

## File Structure

```
project/
├── scraper.py            # Main scraper script
├── requirements.txt      # Python dependencies
├── product_details.csv   # Scraped output (CSV)
├── product_details.txt   # Scraped output (plain text log)
└── README.md
```

---

## How the Human Emulation Works

| Technique | What it does |
|---|---|
| Homepage warm-up | Visits amazon.com first, types a dummy search, then navigates — avoids cold `/dp/` jumps |
| Fingerprint erasure | CDP script overrides `navigator.webdriver`, `navigator.languages`, and `navigator.plugins` |
| User-Agent rotation | Randomly selects from a pool of real Chrome UAs each session |
| `human_sleep()` | All pauses are random ranges (e.g. 1.5–4s), never fixed values |
| `move_mouse_naturally()` | Moves cursor to a random offset first, then glides to element with jitter |
| `simulate_reading()` | Randomly scrolls down and occasionally back up, mimicking reading behavior |

---

## Notes

- Amazon actively updates its bot detection. If you hit a CAPTCHA, wait a few hours before retrying.
- Do not run this at high frequency from the same IP. Space requests at least several minutes apart.
- This scraper is for personal/educational use only. Review Amazon's Terms of Service before use.

---

## Troubleshooting

**`SessionNotCreatedException`** — ChromeDriver version doesn't match Brave. Re-download the correct version from the link in Setup step 2.

**`NoSuchElementException` on price** — Amazon sometimes renders price differently (e.g. subscribe-and-save, out-of-stock). The page structure may have changed; inspect the element and update the class name.

**Blank title / price** — The page likely loaded a CAPTCHA or bot-check interstitial. Run the script manually once to confirm Brave opens the page correctly.
