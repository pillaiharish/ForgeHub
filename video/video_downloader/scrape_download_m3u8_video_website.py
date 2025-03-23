import os
import time
import json
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Target URL
# VIDEO_PAGE_URL = "https://ottverse.com/free-hls-m3u8-test-urls/"
VIDEO_PAGE_URL = "https://castr.com/hlsplayer/"

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
    return driver

def get_latest_html_file():
    """
    Finds the latest HTML file saved in the `browser_captures/` folder.
    """
    html_files = sorted(
        [os.path.join(SAVE_FOLDER, f) for f in os.listdir(SAVE_FOLDER) if f.endswith(".html")],
        key=os.path.getmtime,
        reverse=True
    )
    return html_files[0] if html_files else None

def extract_video_src(html_file):
    """
    Parses the latest HTML file to extract the `video.src` URL.
    """
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Find video tag
        video_tag = soup.find("video")
        if video_tag and video_tag.get("src"):
            video_url = video_tag["src"]
            print(f"[SUCCESS] Extracted Video URL: {video_url}")
            return video_url
        else:
            print("[ERROR] Video source URL not found in the HTML file.")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to parse HTML file: {e}")
        return None

def download_video(video_url, output_folder="downloads"):
    """
    Downloads the video from the extracted `video.src` URL.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_name = "downloaded_video.mp4"
        file_path = os.path.join(output_folder, file_name)

        print(f"[INFO] Downloading video from {video_url}...")
        response = requests.get(video_url, stream=True)

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
    Main function to execute the browser capture script.
    """
    driver = setup_driver()

    try:
        print("[INFO] Opening target page...")
        driver.get(VIDEO_PAGE_URL)

        # Step 1: Wait for Cloudflare verification
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)  # Allow full page load
        driver.refresh()  # Refresh after Cloudflare verification
        time.sleep(3)

        # Step 2: Wait for overlay to disappear
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay"))
        )

        print("[SUCCESS] Overlay removed. Monitoring page for video playback...")

        # Step 3: Monitor for video to start playing
        start_time = time.time()
        while time.time() - start_time < 60:  # Run for 60 seconds
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save page source every second
            html_path = os.path.join(SAVE_FOLDER, f"page_{timestamp}.html")
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(driver.page_source)
            print(f"[INFO] Page source saved: {html_path}")

            time.sleep(1)  # Capture every second

        print("[INFO] Completed monitoring. Extracting video source...")

        # Step 4: Extract video.src from the latest HTML file
        latest_html = get_latest_html_file()
        if latest_html:
            video_url = extract_video_src(latest_html)
            if video_url:
                # Step 5: Download the video
                download_video(video_url)

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()


# Output:
# $ python scrape_download_m3u8_video_website.py 
# [INFO] Opening target page...
# [SUCCESS] Overlay removed. Monitoring page for video playback...
# [INFO] Page source saved: browser_captures/page_20250324_010449.html
# [INFO] Page source saved: browser_captures/page_20250324_010450.html
# [INFO] Page source saved: browser_captures/page_20250324_010451.html
# [INFO] Page source saved: browser_captures/page_20250324_010452.html
# [INFO] Page source saved: browser_captures/page_20250324_010453.html
# [INFO] Page source saved: browser_captures/page_20250324_010454.html
# [INFO] Page source saved: browser_captures/page_20250324_010455.html