import os
from pathlib import Path
from utils import clear, delete_file, file_exists
from ytdlp import extract_videos_from_playlist, download_video
from config import YOUTUBE_PLAYLIST_URL_PREFIX, OUTPUT_FOLDER_PATH, PLAYLIST_TRACKING, CHANGE_MODIFIED_DATE, PLAYLIST_FILE_NAME, TRACKING_FILE_NAME

folder = Path(OUTPUT_FOLDER_PATH)
if folder.exists() and folder.is_dir():
    if input(f"ALERT: {OUTPUT_FOLDER_PATH} folder already exists. Use it anyway? (y/n): ").lower() != "y":
        exit()

playlist = []
if input("Would you like to download a playlist? (y/n): ").lower() == "y":
    while len(playlist) == 0:
        clear()
        playlist_url = input("Insert the YouTube playlist URL: ")
        if not any(playlist_url.startswith(prefix) for prefix in YOUTUBE_PLAYLIST_URL_PREFIX):
            print("ERROR: Invalid playlist URL")
            input("Press any key to continue...")
            continue

        print("Extracting videos...")
        extract_videos_from_playlist(playlist_url)

        # Fill playlist list
        with open(PLAYLIST_FILE_NAME, "r") as f:
            playlist = f.readlines()

        print("All videos extracted")

download_as_audio = False
if input("Would you like to download the video(s) as AUDIO? (y/n): ").lower() == "y":
    download_as_audio = True

clear()

# Download
if len(playlist) == 0: # Single video only
    url = input("Insert the URL of the video you want to download: ")
    download_video(url, download_as_audio)
else:
    urls_to_skip = []
    # Tracking file in OUTPUT_FOLDER_PATH
    if PLAYLIST_TRACKING and file_exists(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}"):
        with open(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}") as f:
            urls_to_skip = f.readlines()

    i=0
    for url in playlist:
        if url in urls_to_skip:
            print(f"URL {url} already exists in folder, skipping...")
            continue
        
        i+=1
        print(f"Downloading video {i} of {len(playlist)}...")
        download_video(url.strip(), download_as_audio)

        if PLAYLIST_TRACKING:
            with open(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}", 'a') as f:
                f.write(f"{url}")

if CHANGE_MODIFIED_DATE:
    for file in Path(OUTPUT_FOLDER_PATH).iterdir():
        if file.is_file():
            created_time = file.stat().st_ctime
            os.utime(file, (created_time, created_time))

delete_file(PLAYLIST_FILE_NAME)