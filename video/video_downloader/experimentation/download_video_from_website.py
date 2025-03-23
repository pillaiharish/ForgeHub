import os
import requests

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

if __name__ == "__main__":
    # URL of the .mp4 file
    mp4_url = "https://ottverse.com/free-hls-m3u8-test-urls"

    # Download the file
    download_mp4(mp4_url)