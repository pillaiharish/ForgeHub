import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Settings
INPUT_FILE = "website-urls.txt"
OUTPUT_DIR = "downloaded_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common image extensions
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')

# Check if a URL is an image by extension
def is_image_by_extension(url):
    return url.lower().endswith(IMAGE_EXTENSIONS)

# Sanitize file name
def sanitize_filename(url):
    return os.path.basename(urlparse(url).path) or f"{hash(url)}.jpg"

# Download image
def download_image(url, prefix=""):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        print(f"[+] Checking URL: {url}")
        r = requests.get(url, headers=headers, timeout=10, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").lower()

        if "image" in content_type or is_image_by_extension(url):
            path = urlparse(url).path
            base = os.path.basename(path) or f"image_{hash(url)}"
            ext = os.path.splitext(base)[1]

            # If extension is missing, try getting it from Content-Type
            if not ext and "image/" in content_type:
                ext = "." + content_type.split("/")[-1].split(";")[0]
            
            filename = prefix + base + ext
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"[✓] Saved: {filepath}")
            return True
        else:
            print(f"[*] Not a direct image, parsing HTML: {url}")
            return False
    except Exception as e:
        print(f"[×] Failed to fetch: {url} → {e}")
        return False

# Process HTML page to extract <img> links
def process_webpage(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        images = soup.find_all("img")

        if not images:
            print(f"[!] No <img> tags found on: {url}")
            return

        for i, img in enumerate(images):
            img_src = img.get("src")
            if not img_src:
                continue
            full_url = urljoin(url, img_src)
            download_image(full_url, prefix=f"{i}_")
    except Exception as e:
        print(f"[×] Error parsing HTML at {url}: {e}")

def main():
    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        print(f"\n=== Processing: {url} ===")
        if not download_image(url):  # if not a direct image
            process_webpage(url)

if __name__ == "__main__":
    main()


# Output:
# harish $ python download_images.py 

# === Processing: https://picsum.photos/id/1015/600/400 ===
# [+] Checking URL: https://picsum.photos/id/1015/600/400
# [✓] Saved: downloaded_images/400.jpeg

# === Processing: https://example.com ===
# [+] Checking URL: https://example.com
# [*] Not a direct image, parsing HTML: https://example.com
# [!] No <img> tags found on: https://example.com

# === Processing: https://dummyimage.com/600x400/000/fff&text=Image+1 ===
# [+] Checking URL: https://dummyimage.com/600x400/000/fff&text=Image+1
# [✓] Saved: downloaded_images/fff&text=Image+1.png

# === Processing: https://www.wikipedia.org/ ===
# [+] Checking URL: https://www.wikipedia.org/
# [*] Not a direct image, parsing HTML: https://www.wikipedia.org/
# [+] Checking URL: https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2.png
# [✓] Saved: downloaded_images/0_Wikipedia-logo-v2.png.png