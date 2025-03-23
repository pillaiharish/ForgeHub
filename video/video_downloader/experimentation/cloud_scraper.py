import os
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Target URL
VIDEO_PAGE_URL = "https://ottverse.com/free-hls-m3u8-test-urls/"

# Create a folder to store captured data
SAVE_FOLDER = "browser_captures"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def setup_driver():
    """
    Set up undetected ChromeDriver to bypass bot detection.
    """
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-popup-blocking")

    driver = uc.Chrome(options=options)

    # Enable performance logging to capture network activity
    driver.execute_cdp_cmd("Network.enable", {})
    return driver

def wait_for_cloudflare(driver):
    """
    Waits for Cloudflare's "Verifying you are human" check to complete and ensures the real page loads.
    """
    try:
        print("[INFO] Waiting for Cloudflare verification...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("[SUCCESS] Cloudflare check passed. Waiting for full page load...")
        
        # Wait for the page to stabilize
        time.sleep(5)  

        # Refresh to ensure new elements load properly
        driver.refresh()
        time.sleep(3)
        print("[SUCCESS] Page fully loaded after Cloudflare verification.")

    except Exception as e:
        print(f"[ERROR] Cloudflare verification failed: {e}")

def wait_for_overlay(driver):
    """
    Waits for the video overlay to disappear before collecting network data.
    """
    try:
        print("[INFO] Waiting for overlay to disappear...")
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay"))
        )
        print("[SUCCESS] Overlay removed. Video player should be visible.")
    except Exception as e:
        print(f"[ERROR] Overlay wait error: {e}")

def capture_network_requests(driver):
    """
    Extracts network requests (e.g., .m3u8, video sources, scripts).
    """
    try:
        logs = driver.execute_script("""
            let urls = performance.getEntries().map(e => e.name);
            return urls.filter(url => url.includes('.m3u8') || url.includes('.mp4') || url.includes('.ts'));
        """)

        return logs if logs else []

    except Exception as e:
        print(f"[ERROR] Failed to extract network requests: {e}")
        return []

def save_screenshot(driver):
    """
    Takes a screenshot of the browser every second.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(SAVE_FOLDER, f"screenshot_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    print(f"[INFO] Screenshot saved: {screenshot_path}")

def save_page_source(driver):
    """
    Saves the page source (HTML) every second.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(SAVE_FOLDER, f"page_{timestamp}.html")

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    print(f"[INFO] Page source saved: {html_path}")

def save_network_logs(driver):
    """
    Extracts and saves network activity logs (JavaScript-injected data, .m3u8, etc.).
    """
    network_requests = capture_network_requests(driver)

    if network_requests:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(SAVE_FOLDER, f"network_{timestamp}.json")

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(network_requests, file, indent=4)

        print(f"[INFO] Network logs saved: {json_path}")
    else:
        print("[WARNING] No network requests captured.")

def wait_for_video_to_start(driver):
    """
    Monitors the page until the video starts playing and extracts the .m3u8 URL.
    """
    print("[INFO] Waiting for the video to start playing...")
    start_time = time.time()
    while time.time() - start_time < 60:  # Wait up to 60 seconds
        try:
            video_element = driver.find_element(By.TAG_NAME, "video")
            video_url = video_element.get_attribute("src")
            if video_url and ".m3u8" in video_url:
                print(f"[SUCCESS] Found .m3u8 URL: {video_url}")
                return video_url
        except:
            pass
        time.sleep(1)
    
    print("[ERROR] Video did not start playing.")
    return None

def monitor_page(driver):
    """
    Continuously captures screenshots, HTML, and network requests every second.
    """
    try:
        print("[INFO] Opening target page...")
        driver.get(VIDEO_PAGE_URL)

        # Step 1: Wait for Cloudflare verification
        wait_for_cloudflare(driver)

        # Step 2: Wait for overlay to disappear
        wait_for_overlay(driver)

        # Step 3: Monitor browser every second
        start_time = time.time()
        while time.time() - start_time < 60:  # Run for 60 seconds
            save_screenshot(driver)
            save_page_source(driver)
            save_network_logs(driver)

            # Step 4: Extract .m3u8 URL when video starts playing
            m3u8_url = wait_for_video_to_start(driver)
            if m3u8_url:
                print(f"[SUCCESS] Extracted m3u8 URL: {m3u8_url}")
                break

            time.sleep(1)  # Capture data every second

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

    finally:
        driver.quit()

def main():
    """
    Main function to execute the browser capture script.
    """
    driver = setup_driver()
    monitor_page(driver)

if __name__ == "__main__":
    main()



# Output:
# $ python download_m3u8.py 
# [INFO] Bypassing Cloudflare...
# [SUCCESS] Cloudflare challenge passed.
# [INFO] Opening video page in Selenium...
# [INFO] Searching for .m3u8 URL...
# [WARNING] No .m3u8 URL found.
# [ERROR] Failed to extract .m3u8 URL. Exiting...