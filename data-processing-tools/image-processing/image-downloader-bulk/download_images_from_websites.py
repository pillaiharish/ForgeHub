import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

def create_folder(folder_name):
    """Create a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def get_domain_name(url):
    """Extract the domain name from the URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc

def download_image(image_url, folder_name):
    """Download an image from the given URL and save it to the specified folder."""
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_name = os.path.join(folder_name, os.path.basename(image_url))
            with open(image_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Failed to download: {image_url}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

def find_images_in_website(url, folder_name):
    """Find all images on a website and download them."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if img_url:
                # Handle relative URLs
                img_url = urljoin(url, img_url)
                download_image(img_url, folder_name)

        # Find embedded images (e.g., in CSS or JavaScript)
        for tag in soup.find_all(['style', 'script']):
            if tag.name == 'style':
                # Extract URLs from CSS
                css_urls = re.findall(r'url\((.*?)\)', tag.string or '')
                for css_url in css_urls:
                    css_url = urljoin(url, css_url.strip('\'"'))
                    download_image(css_url, folder_name)
            elif tag.name == 'script':
                # Extract URLs from JavaScript (if needed)
                pass

    except Exception as e:
        print(f"Error processing {url}: {e}")

def read_urls_from_file(file_path):
    """Read URLs from a file. URLs can be separated by new lines, spaces, or commas."""
    with open(file_path, 'r') as file:
        content = file.read()
        # Split URLs by new lines, spaces, or commas
        urls = re.split(r'[\s,]+', content)
        # Remove empty strings from the list
        urls = [url.strip() for url in urls if url.strip()]
    return urls

def download_images_from_websites(file_path):
    """Download images from multiple websites listed in a file."""
    website_urls = read_urls_from_file(file_path)
    for website_url in website_urls:
        domain_name = get_domain_name(website_url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = create_folder(f"{domain_name}_{timestamp}")

        print(f"Downloading images from: {website_url}")
        find_images_in_website(website_url, folder_name)

if __name__ == "__main__":
    # Path to the file containing URLs
    file_path = "website-urls.txt"

    # Check if the file exists
    if os.path.exists(file_path):
        download_images_from_websites(file_path)
    else:
        print(f"File '{file_path}' not found. Please create the file and add URLs.")



# Output:
# harish $ python download_images_from_websites.py 
# Downloading images from: https://picsum.photos/id/1015/600/400
# Downloading images from: https://example.com
# Downloading images from: https://dummyimage.com/600x400/000/fff&text=Image+1
# Downloading images from: https://www.wikipedia.org/
# Downloaded: www.wikipedia.org_20250324_015648/Wikipedia-logo-v2.png
# Downloaded: www.wikipedia.org_20250324_015648/sprite-de847d1a.svg
# Error downloading data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="%23fff" d="M7 14.17L2.83 10l-1.41 1.41L7 17 19 5l-1.41-1.42z"/></svg>: No connection adapters were found for 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="%23fff" d="M7 14.17L2.83 10l-1.41 1.41L7 17 19 5l-1.41-1.42z"/></svg>'
# Error downloading data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="filter"><feComponentTransfer color-interpolation-filters="sRGB"><feFuncR type="table" tableValues="1 0" /><feFuncG type="table" tableValues="1 0" /><feFuncB type="table" tableValues="1 0" /></feComponentTransfer></filter></svg>#filter: No connection adapters were found for 'data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="filter"><feComponentTransfer color-interpolation-filters="sRGB"><feFuncR type="table" tableValues="1 0" /><feFuncG type="table" tableValues="1 0" /><feFuncB type="table" tableValues="1 0" /></feComponentTransfer></filter></svg>#filter'
# Failed to download: https://www.wikipedia.org/portal/wikipedia.org/assets/img/noimage.png
# Error downloading data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 56'%3E%3Cpath fill='%23eee' d='M0 0h56v56H0z'/%3E%3Cpath fill='%23999' d='M36.4 13.5H17.8v24.9c0 1.4.9 2.3 2.3 2.3h18.7v-25c.1-1.4-1-2.2-2.4-2.2zM30.2 17h5.1v6.4h-5.1V17zm-8.8 0h6v1.8h-6V17zm0 4.6h6v1.8h-6v-1.8zm0 15.5v-1.8h13.8v1.8H21.4zm13.8-4.5H21.4v-1.8h13.8v1.8zm0-4.7H21.4v-1.8h13.8v1.8z'/%3E%3C/svg%3E: No connection adapters were found for "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 56'%3E%3Cpath fill='%23eee' d='M0 0h56v56H0z'/%3E%3Cpath fill='%23999' d='M36.4 13.5H17.8v24.9c0 1.4.9 2.3 2.3 2.3h18.7v-25c.1-1.4-1-2.2-2.4-2.2zM30.2 17h5.1v6.4h-5.1V17zm-8.8 0h6v1.8h-6V17zm0 4.6h6v1.8h-6v-1.8zm0 15.5v-1.8h13.8v1.8H21.4zm13.8-4.5H21.4v-1.8h13.8v1.8zm0-4.7H21.4v-1.8h13.8v1.8z'/%3E%3C/svg%3E"
# Failed to download: https://www.wikipedia.org/portal/wikipedia.org/assets/img/noimage.png
# Downloaded: www.wikipedia.org_20250324_015648/Wikinews-logo_sister.png
# Downloaded: www.wikipedia.org_20250324_015648/Wikinews-logo_sister@2x.png
# Error downloading data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="filter"><feComponentTransfer color-interpolation-filters="sRGB"><feFuncR type="table" tableValues="1 0" /><feFuncG type="table" tableValues="1 0" /><feFuncB type="table" tableValues="1 0" /></feComponentTransfer></filter></svg>#filter: No connection adapters were found for 'data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="filter"><feComponentTransfer color-interpolation-filters="sRGB"><feFuncR type="table" tableValues="1 0" /><feFuncG type="table" tableValues="1 0" /><feFuncB type="table" tableValues="1 0" /></feComponentTransfer></filter></svg>#filter'