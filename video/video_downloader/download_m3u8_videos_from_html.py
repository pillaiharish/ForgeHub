import os
import re
import requests
import m3u8
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Folder with HTML captures
INPUT_FOLDER = "./browser_captures"
OUTPUT_FOLDER = "./downloaded_videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Regex to catch m3u8 URLs even in JS
M3U8_REGEX = re.compile(r'https?://[^\s"\'<>]+\.m3u8')

def extract_m3u8_from_html(file_path):
    urls = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Search in raw text
        text = soup.get_text()
        urls.update(M3U8_REGEX.findall(text))
        
        # Also check in <script> tags
        for script in soup.find_all('script'):
            if script.string:
                urls.update(M3U8_REGEX.findall(script.string))
    return urls

def download_hls_stream(m3u8_url, output_name):
    print(f"\n[+] Downloading from: {m3u8_url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        r = requests.get(m3u8_url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[-] Failed to fetch playlist: {e}")
        return

    try:
        playlist = m3u8.loads(r.text)
    except Exception as e:
        print(f"[-] Error parsing playlist: {e}")
        print("[!] Partial content for debug:")
        print(r.text[:500])
        return

    if not playlist.segments:
        print("[-] No segments found in the playlist. Possibly a master playlist or empty stream.")
        print("[!] Here’s a snippet of the playlist:")
        print(r.text[:500])
        return

    filelist_path = os.path.join(OUTPUT_FOLDER, f"{output_name}_filelist.txt")
    segment_files = []

    with open(filelist_path, 'w') as f:
        for i, seg in enumerate(playlist.segments):
            seg_url = urljoin(m3u8_url, seg.uri)
            seg_name = os.path.join(OUTPUT_FOLDER, f"{output_name}_{i}.ts")

            try:
                seg_resp = requests.get(seg_url, headers=headers, timeout=10)
                seg_resp.raise_for_status()
                with open(seg_name, 'wb') as seg_file:
                    seg_file.write(seg_resp.content)
                f.write(f"file '{seg_name}'\n")
                segment_files.append(seg_name)
                print(f"[✓] Segment {i+1}/{len(playlist.segments)} downloaded.")
            except Exception as e:
                print(f"[-] Failed segment {i}: {e}")

    final_output = os.path.join(OUTPUT_FOLDER, f"{output_name}.mp4")
    cmd = f'ffmpeg -loglevel error -f concat -safe 0 -i "{filelist_path}" -c copy "{final_output}"'
    subprocess.run(cmd, shell=True)
    print(f"[✓] Merged video saved as: {final_output}")

    # Cleanup
    for f in segment_files:
        os.remove(f)
    os.remove(filelist_path)

def main():
    all_m3u8_urls = set()
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.html'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            found_urls = extract_m3u8_from_html(file_path)
            all_m3u8_urls.update(found_urls)
            print(f"[i] {filename}: found {len(found_urls)} m3u8 URLs")

    if not all_m3u8_urls:
        print("[-] No m3u8 URLs found.")
        return

    for idx, url in enumerate(all_m3u8_urls):
        download_hls_stream(url, f"video_{idx}")

if __name__ == "__main__":
    main()



# harish $ python download_m3u8_videos_from_html.py 
# [i] page_20250324_010454.html: found 13 m3u8 URLs
# [i] page_20250324_010927.html: found 0 m3u8 URLs
# [i] page_20250324_010926.html: found 0 m3u8 URLs
# [i] page_20250324_010455.html: found 13 m3u8 URLs
# [i] page_20250324_010452.html: found 13 m3u8 URLs
# [i] page_20250324_010453.html: found 13 m3u8 URLs
# [i] page_20250324_010449.html: found 13 m3u8 URLs
# [i] page_20250324_010450.html: found 13 m3u8 URLs
# [i] page_20250324_010451.html: found 13 m3u8 URLs
# [i] page_20250324_010929.html: found 0 m3u8 URLs
# [i] page_20250324_010925.html: found 0 m3u8 URLs
# [i] page_20250324_010924.html: found 0 m3u8 URLs
# [i] page_20250324_010928.html: found 0 m3u8 URLs

# [+] Downloading from: http://149.255.155.142/Xazar/index.m3u8
# [-] Failed to load playlist: <urlopen error [Errno 60] Operation timed out>

# [+] Downloading from: http://xxxxxxx.com/live/video.m3u8
# [-] Failed to load playlist: HTTP Error 522: 

# [+] Downloading from: https://149.255.155.142/Xazar/index.m3u8
# [-] Failed to load playlist: <urlopen error [Errno 60] Operation timed out>

# [+] Downloading from: http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multi_language_subs.m3u8
# [-] Failed to load playlist: HTTP Error 403: Forbidden

# [+] Downloading from: https://moctobpltc-i.akamaihd.net/hls/live/571329/eight/playlist.m3u8
# [in#0 @ 0x121632e30] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_4_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_4.mp4

# [+] Downloading from: https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_fmp4/master.m3u8
# [in#0 @ 0x14ce12900] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_5_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_5.mp4

# [+] Downloading from: https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8
# [in#0 @ 0x1427065f0] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_6_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_6.mp4

# [+] Downloading from: https://xxxxxxx.com/live/video.m3u8
# [-] Failed to load playlist: HTTP Error 522: 

# [+] Downloading from: http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multichannel_subs.m3u8
# [-] Failed to load playlist: HTTP Error 403: Forbidden

# [+] Downloading from: https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.mp4/.m3u8
# [in#0 @ 0x12af22b90] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_9_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_9.mp4

# [+] Downloading from: http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_stereo_subs.m3u8
# [-] Failed to load playlist: HTTP Error 403: Forbidden

# [+] Downloading from: https://ireplay.tv/test/blender.m3u8
# [in#0 @ 0x129e329c0] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_11_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_11.mp4

# [+] Downloading from: https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8
# [in#0 @ 0x1256329c0] Error opening input: Invalid data found when processing input
# Error opening input file ./downloaded_videos/video_12_filelist.txt.
# Error opening input files: Invalid data found when processing input
# [✓] Merged video saved as: ./downloaded_videos/video_12.mp4