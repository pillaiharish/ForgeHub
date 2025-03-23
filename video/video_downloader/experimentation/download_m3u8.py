

# # Target Video Page URL
# VIDEO_PAGE_URL = ""  # Change accordingly

import cloudscraper
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse, parse_qs
import requests
import os

# Target Video Page
VIDEO_PAGE_URL = "https://ottverse.com/free-hls-m3u8-test-urls/"

def setup_driver():
    """
    Set up undetected ChromeDriver with necessary options.
    """
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")  # For debugging, set False
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options)
    return driver

def bypass_cloudflare():
    """
    Uses Cloudscraper to bypass Cloudflare's challenge and retrieve cookies.
    """
    print("[INFO] Bypassing Cloudflare...")
    scraper = cloudscraper.create_scraper()
    response = scraper.get(VIDEO_PAGE_URL)

    if response.status_code == 200:
        print("[SUCCESS] Cloudflare challenge passed.")
        return scraper.cookies.get_dict()
    else:
        print(f"[ERROR] Cloudflare bypass failed! Status Code: {response.status_code}")
        return None

def open_video_page(driver, cookies):
    """
    Opens the video page and sets Cloudflare cookies to avoid detection.
    """
    print("[INFO] Opening video page in Selenium...")
    driver.get(VIDEO_PAGE_URL)

    # Apply Cloudflare bypass cookies
    for name, value in cookies.items():
        driver.add_cookie({"name": name, "value": value, "domain": ".ottverse.com"})

    time.sleep(2)  # Give time for cookies to take effect
    driver.refresh()  # Reload with cookies applied

def extract_m3u8_url(driver):
    """
    Extracts the .m3u8 URL from network requests.
    """
    try:
        print("[INFO] Searching for .m3u8 URL...")

        for _ in range(30):  # Retry for 30 seconds
            m3u8_url = driver.execute_script("""
                let urls = performance.getEntries().map(e => e.name);
                return urls.find(url => url.includes('.m3u8') || url.includes('master.m3u8'));
            """)
            if m3u8_url:
                print(f"[SUCCESS] Found .m3u8 URL: {m3u8_url}")
                return m3u8_url
            time.sleep(1)

        print("[WARNING] No .m3u8 URL found.")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to extract .m3u8 URL: {e}")
        return None

def construct_mp4_url(m3u8_url):
    """
    Constructs the final .mp4 download URL from .m3u8 query parameters.
    """
    try:
        parsed_url = urlparse(m3u8_url)
        query_params = parse_qs(parsed_url.query)

        base_path = parsed_url.path.replace("hls2", "v").replace("_.urlset/master.m3u8", "_l/l.mp4")

        mp4_url = f"{parsed_url.scheme}://{parsed_url.netloc}{base_path}"

        query_params = {k: v[0] for k, v in query_params.items()}
        mp4_url += f"?t={query_params.get('t', '')}&s={query_params.get('s', '')}&e={query_params.get('e', '')}&f={query_params.get('f', '')}&sp={query_params.get('sp', '')}&i={query_params.get('i', '')}"

        print(f"[SUCCESS] Constructed .mp4 URL: {mp4_url}")
        return mp4_url

    except Exception as e:
        print(f"[ERROR] Failed to construct .mp4 URL: {e}")
        return None

def download_mp4(mp4_url, output_folder="downloads"):
    """
    Downloads the final .mp4 video.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_name = "downloaded_video.mp4"
        file_path = os.path.join(output_folder, file_name)

        print(f"[INFO] Downloading video from {mp4_url}...")
        response = requests.get(mp4_url, stream=True)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"[SUCCESS] Video saved at: {file_path}")
            return file_path
        else:
            print(f"[ERROR] Failed to download video. Status: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Download error: {e}")
        return None

def main():
    """
    Main function to extract and download video.
    """
    driver = setup_driver()

    try:
        # Step 1: Bypass Cloudflare
        cf_cookies = bypass_cloudflare()
        if not cf_cookies:
            print("[ERROR] Cloudflare bypass failed! Exiting...")
            return

        # Step 2: Open the page and inject cookies
        open_video_page(driver, cf_cookies)

        # Step 3: Extract master .m3u8 URL
        m3u8_url = extract_m3u8_url(driver)
        if not m3u8_url:
            print("[ERROR] Failed to extract .m3u8 URL. Exiting...")
            return

        # Step 4: Construct final .mp4 URL
        mp4_url = construct_mp4_url(m3u8_url)
        if not mp4_url:
            print("[ERROR] Failed to construct .mp4 URL. Exiting...")
            return

        # Step 5: Download the video
        download_mp4(mp4_url)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
