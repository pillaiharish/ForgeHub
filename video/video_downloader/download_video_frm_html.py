import os
import re
import requests
from bs4 import BeautifulSoup

# Define directories
CAPTURES_FOLDER = "browser_captures"
DOWNLOADS_FOLDER = "downloads"

# Create the downloads folder if it doesn't exist
if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)

def extract_video_url_from_html(file_path):
    """
    Extracts the video source URL from the given HTML file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Search for video.src pattern in JavaScript inside <script> tags
        video_src_match = re.search(r'video\.src\s*=\s*[\'"]([^\'"]+\.mp4[^\']*)[\'"]', html_content)

        if video_src_match:
            video_url = video_src_match.group(1)
            print(f"[SUCCESS] Extracted video URL from {file_path}: {video_url}")
            return video_url

        print(f"[WARNING] No video source found in {file_path}.")
        return None

    except Exception as e:
        print(f"[ERROR] Failed to extract video from {file_path}: {e}")
        return None

def download_video(video_url):
    """
    Downloads the video from the given URL and saves it to the downloads folder.
    """
    try:
        if not video_url:
            print("[ERROR] No video URL provided.")
            return None

        file_name = os.path.basename(video_url.split("?")[0])  # Remove query params
        file_path = os.path.join(DOWNLOADS_FOLDER, file_name)

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

def process_all_html_files():
    """
    Reads all .html files in the `browser_captures/` folder, extracts video URLs, and downloads them.
    """
    print("[INFO] Scanning HTML files for video URLs...")
    
    for file_name in os.listdir(CAPTURES_FOLDER):
        if file_name.endswith(".html"):
            file_path = os.path.join(CAPTURES_FOLDER, file_name)
            video_url = extract_video_url_from_html(file_path)

            if video_url:
                download_video(video_url)

if __name__ == "__main__":
    process_all_html_files()
