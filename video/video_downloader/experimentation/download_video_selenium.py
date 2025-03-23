import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import random

def download_mp4(url, output_folder="downloads"):
    """
    Download an .mp4 file from the given URL and save it to the specified folder.
    """
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Extract the file name from the URL
        file_name = os.path.basename(url)
        file_path = os.path.join(output_folder, file_name)

        # Send a GET request to the URL
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the file to the specified path
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"File saved to: {file_path}")
        else:
            print(f"Failed to download. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

def extract_hyperlinks(driver):
    """
    Extract all HTTP/HTTPS hyperlinks from the webpage and print them.
    """
    try:
        # Find all <a> tags with href attributes
        links = driver.find_elements(By.TAG_NAME, "a")
        hyperlinks = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        # Print all hyperlinks
        print("Hyperlinks found on the page:")
        for link in hyperlinks:
            print(link)

    except Exception as e:
        print(f"An error occurred while extracting hyperlinks: {e}")

def extract_mp4_url():
    """
    Use undetected-chromedriver to extract the .mp4 URL from the website.
    """
    try:
        # Initialize undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
        driver = uc.Chrome(options=options)

        # Open the website
        driver.get("https://ottverse.com/free-hls-m3u8-test-urls/")

        # Add a random delay to mimic human behavior
        time.sleep(random.uniform(5, 10))  # Wait between 5 and 10 seconds

        # Extract and print all hyperlinks
        extract_hyperlinks(driver)

        # Wait for the translucent screen (loading overlay) to disappear
        wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay"))  # Adjust the selector for the overlay
        )

        # Wait for the video element to load
        video_element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        # Extract the .mp4 URL from the <video> tag
        mp4_url = video_element.get_attribute("src")

        if mp4_url:
            print(f"Found .mp4 URL: {mp4_url}")
            return mp4_url
        else:
            print("No .mp4 URL found on the page.")
            return None

    except Exception as e:
        print(f"An error occurred while extracting the .mp4 URL: {e}")
        return None

    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    # Extract the .mp4 URL using undetected-chromedriver
    mp4_url = extract_mp4_url()

    if mp4_url:
        # Download the .mp4 file
        download_mp4(mp4_url)
    else:
        print("Failed to extract .mp4 URL.")



# Output:
# $ python download_video_selenium.py 
# Hyperlinks found on the page:
# https://ottverse.com/free-hls-m3u8-test-urls/#content
# https://ottverse.com/
# https://ottverse.com/
# https://ottverse.com/video-encoding/
# https://ottverse.com/video-streaming/
# https://ottverse.com/drm/
# https://ottverse.com/adtech/
# https://ottverse.com/recipes-in-ffmpeg/
# https://ottverse.com/category/ott-news/
# https://ottverse.com/category/press-release/
# https://ottverse.com/category/guest/
# https://ottverse.com/category/whitepaper/
# https://ottverse.com/category/interviews-features/
# https://ottverse.com/category/women-in-streaming/
# https://ottverse.com/category/buyers-guide/
# https://ottverse.com/events-2025/
# https://ottverse.com/events-2025/
# https://ottverse.com/ottverse-events/
# https://ottverse.com/subscribe/
# https://ottverse.com/about-us/
# https://ottverse.com/contact/
# https://ottverse.com/guest-posts/
# https://ottverse.com/advertise/
# https://ottverse.com/privacy-policy/
# https://ottverse.com/category/nab-2024/
# https://ottverse.com/nab-2023/
# https://ottverse.com/directory/
# https://ottverse.com/free-hls-m3u8-test-urls/#
# https://ottverse.com/
# https://ottverse.com/
# https://ottverse.com/video-encoding/
# https://ottverse.com/video-streaming/
# https://ottverse.com/drm/
# https://ottverse.com/adtech/
# https://ottverse.com/recipes-in-ffmpeg/
# https://ottverse.com/category/ott-news/
# https://ottverse.com/category/press-release/
# https://ottverse.com/category/guest/
# https://ottverse.com/category/whitepaper/
# https://ottverse.com/category/interviews-features/
# https://ottverse.com/category/women-in-streaming/
# https://ottverse.com/category/buyers-guide/
# https://ottverse.com/events-2025/
# https://ottverse.com/events-2025/
# https://ottverse.com/ottverse-events/
# https://ottverse.com/subscribe/
# https://ottverse.com/about-us/
# https://ottverse.com/contact/
# https://ottverse.com/guest-posts/
# https://ottverse.com/advertise/
# https://ottverse.com/privacy-policy/
# https://ottverse.com/category/nab-2024/
# https://ottverse.com/nab-2023/
# https://ottverse.com/directory/
# https://ottverse.com/category/video-streaming/
# https://ottverse.com/free-mpeg-dash-mpd-manifest-example-test-urls/
# https://ottverse.com/hls-http-live-streaming-how-does-it-work/
# https://ottverse.com/hls-packaging-using-ffmpeg-live-vod/
# https://ottverse.com/top-online-m3u8-players-to-test-hls-m3u8-streams/
# https://ottverse.com/hls-vs-mpeg-dash-video-streaming/
# https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8
# https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8
# https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_fmp4/master.m3u8
# https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.mp4/.m3u8
# https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8
# https://moctobpltc-i.akamaihd.net/hls/live/571329/eight/playlist.m3u8
# https://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_stereo_subs.m3u8
# https://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multichannel_subs.m3u8
# https://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multi_language_subs.m3u8
# http://amssamples.streaming.mediaservices.windows.net/91492735-c523-432b-ba01-faba6c2206a2/AzureMediaServicesPromo.ism/manifest(format=m3u8-aapl)
# http://amssamples.streaming.mediaservices.windows.net/69fbaeba-8e92-4740-aedc-ce09ae945073/AzurePromo.ism/manifest(format=m3u8-aapl)
# http://amssamples.streaming.mediaservices.windows.net/634cd01c-6822-4630-8444-8dd6279f94c6/CaminandesLlamaDrama4K.ism/manifest(format=m3u8-aapl)
# https://www.linkedin.com/in/krishnaraovijayanagar/
# https://ottverse.com/
# https://www.harmonicinc.com/
# https://mediamelon.com/
# https://visionular.ai/
# https://ottverse.com/top-online-m3u8-players-to-test-hls-m3u8-streams/
# https://ottverse.com/top-online-m3u8-players-to-test-hls-m3u8-streams/
# https://ottverse.com/free-mpeg-dash-mpd-manifest-example-test-urls/
# https://ottverse.com/free-mpeg-dash-mpd-manifest-example-test-urls/
# https://ottverse.com/hls-http-live-streaming-and-meaning-ottverse/
# https://ottverse.com/hls-http-live-streaming-and-meaning-ottverse/
# https://ottverse.com/hls-packaging-using-ffmpeg-live-vod/
# https://ottverse.com/hls-packaging-using-ffmpeg-live-vod/
# https://ottverse.com/hls-vs-mpeg-dash-video-streaming/
# https://ottverse.com/hls-vs-mpeg-dash-video-streaming/
# https://ottverse.com/what-is-ext-x-key-in-hls-playlists/
# https://ottverse.com/what-is-ext-x-key-in-hls-playlists/
# https://ottverse.com/apple-fairplay-streaming-drm-how-does-it-work/
# https://ottverse.com/apple-fairplay-streaming-drm-how-does-it-work/
# https://ottverse.com/online-mpeg-dash-players-mpd-player-test-mpd-streams/
# https://ottverse.com/online-mpeg-dash-players-mpd-player-test-mpd-streams/
# https://ottverse.com/best-html5-video-players-for-the-web-free-and-paid/
# https://ottverse.com/best-html5-video-players-for-the-web-free-and-paid/
# https://ottverse.com/what-is-ott-video-streaming/
# https://ottverse.com/what-is-abr-video-streaming/
# https://ottverse.com/hls-http-live-streaming-how-does-it-work/
# https://hcanlitv.net/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-746
# http://xxxxxxx.com/live/video.m3u8
# https://xxxxxxx.com/live/video.m3u8
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-746
# https://hcanlitv.net/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-3062
# http://149.255.155.142/Xazar/index.m3u8
# https://149.255.155.142/Xazar/index.m3u8
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-3062
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-7200
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-7200
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-8383
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-8383
# https://cookie.technology/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-13298
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-13298
# https://ottverse.com/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-14021
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-14021
# https://ireplay.tv/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-26860
# https://ireplay.tv/test/blender.m3u8
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-26860
# http://www.eubezhranic.eu/stream
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-16925
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-16925
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-19428
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-19428
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-22853
# https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-22853
# https://ottverse.com/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-22858
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-22858
# https://www.youtube.com/channel/UCntyj4YCyhZ0p5_BXwHDqUg
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-26967
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-26967
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-29012
# https://www.radiomast/reference-streams
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-29012
# https://differencebee.com/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-32162
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-32162
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-32453
# https://ottverse.com/free-mpeg-dash-mpd-manifest-example-test-urls/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-32453
# https://liveclip.app/
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-68080
# https://ottverse.com/free-hls-m3u8-test-urls/#comment-68080
# https://ottverse.com/free-hls-m3u8-test-urls/#respond
# https://bit.ly/49HtRpn
# An error occurred while extracting the .mp4 URL: Message: 
# Stacktrace:
# 0   undetected_chromedriver             0x0000000101096568 undetected_chromedriver + 6088040
# 1   undetected_chromedriver             0x000000010108e17a undetected_chromedriver + 6054266
# 2   undetected_chromedriver             0x0000000100b2d540 undetected_chromedriver + 415040
# 3   undetected_chromedriver             0x0000000100b7f0a0 undetected_chromedriver + 749728
# 4   undetected_chromedriver             0x0000000100b7f2f1 undetected_chromedriver + 750321
# 5   undetected_chromedriver             0x0000000100bcf764 undetected_chromedriver + 1079140
# 6   undetected_chromedriver             0x0000000100ba541d undetected_chromedriver + 906269
# 7   undetected_chromedriver             0x0000000100bcca19 undetected_chromedriver + 1067545
# 8   undetected_chromedriver             0x0000000100ba51c3 undetected_chromedriver + 905667
# 9   undetected_chromedriver             0x0000000100b7105a undetected_chromedriver + 692314
# 10  undetected_chromedriver             0x0000000100b721b1 undetected_chromedriver + 696753
# 11  undetected_chromedriver             0x0000000101055c90 undetected_chromedriver + 5823632
# 12  undetected_chromedriver             0x0000000101059b44 undetected_chromedriver + 5839684
# 13  undetected_chromedriver             0x0000000101030e86 undetected_chromedriver + 5672582
# 14  undetected_chromedriver             0x000000010105a53b undetected_chromedriver + 5842235
# 15  undetected_chromedriver             0x000000010101f824 undetected_chromedriver + 5601316
# 16  undetected_chromedriver             0x000000010107c618 undetected_chromedriver + 5981720
# 17  undetected_chromedriver             0x000000010107c7df undetected_chromedriver + 5982175
# 18  undetected_chromedriver             0x000000010108dd58 undetected_chromedriver + 6053208
# 19  libsystem_pthread.dylib             0x00007ff8018e4253 _pthread_start + 99
# 20  libsystem_pthread.dylib             0x00007ff8018dfbef thread_start + 15

# Failed to extract .mp4 URL.