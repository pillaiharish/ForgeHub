import os
import requests
import m3u8
import subprocess
from urllib.parse import urljoin

OUTPUT_FOLDER = "test_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_hls_stream(m3u8_url, output_name):
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"[+] Fetching: {m3u8_url}")
    try:
        r = requests.get(m3u8_url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[-] Error fetching playlist: {e}")
        return

    try:
        playlist = m3u8.loads(r.text)

        # 🔁 Handle master playlist (EXT-X-STREAM-INF)
        if playlist.is_variant:
            print(f"[i] Master playlist with {len(playlist.playlists)} variants found.")
            best_variant = playlist.playlists[0]  # Or use resolution/bitrate logic
            variant_uri = urljoin(m3u8_url, best_variant.uri)
            print(f"[→] Switching to variant playlist: {variant_uri}")
            
            # Fetch and re-parse the selected variant
            r = requests.get(variant_uri, headers=headers, timeout=10)
            r.raise_for_status()
            playlist = m3u8.loads(r.text)

    except Exception as e:
        print(f"[-] Error parsing playlist: {e}")
        return

    if not playlist.segments:
        print("[-] No segments found in playlist.")
        print(r.text[:300])
        return

    filelist_path = os.path.join(OUTPUT_FOLDER, f"{output_name}_filelist.txt")
    segment_files = []

    with open(filelist_path, 'w') as f:
        for i, segment in enumerate(playlist.segments):
            segment_url = urljoin(m3u8_url, segment.uri)
            segment_path = os.path.join(OUTPUT_FOLDER, f"{output_name}_{i}.ts")
            try:
                seg_resp = requests.get(segment_url, headers=headers, timeout=10)
                with open(segment_path, 'wb') as seg_file:
                    seg_file.write(seg_resp.content)
                f.write(f"file '{segment_path}'\n")
                segment_files.append(segment_path)
                print(f"[✓] Segment {i+1}/{len(playlist.segments)}")
            except Exception as e:
                print(f"[-] Failed to download segment {i}: {e}")

    output_video = os.path.join(OUTPUT_FOLDER, f"{output_name}.mp4")
    cmd = f'ffmpeg -f concat -safe 0 -i "{filelist_path}" -c copy "{output_video}"'
    subprocess.run(cmd, shell=True)
    print(f"[✓] Merged video saved as: {output_video}")

    for file in segment_files:
        os.remove(file)
    os.remove(filelist_path)

# ▶️ TEST URL
test_url = "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
download_hls_stream(test_url, "sintel_test")


# Output:
# harish $ python download_m3u8_directly.py 
# [+] Fetching: https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
# [i] Master playlist with 8 variants found.
# [→] Switching to variant playlist: https://bitdash-a.akamaihd.net/content/sintel/hls/video/250kbit.m3u8
# [✓] Segment 1/444
# [✓] Segment 2/444
# [✓] Segment 3/444
# [✓] Segment 4/444
# [✓] Segment 5/444
# [✓] Segment 6/444
# [✓] Segment 7/444
# ^CTraceback (most recent call last):