import os
from pathlib import Path
from utils import clear, file_exists, update_tracking_file
from ytdlp import extract_videos_from_playlist, download_video, get_video_title
from config import APP_NAME, VERSION, YOUTUBE_PLAYLIST_URL_PREFIX, OUTPUT_FOLDER_PATH, PLAYLIST_TRACKING, CHANGE_TRACK_NUMBER, TRACKING_FILE_NAME
from help import *

print(f"{APP_NAME} - v{VERSION}")
print("Repository: github.com/lucastozo/yt-dlp-quick-tool")

while True:
    print("Press any key to download videos or type \"help\" to show additional options")
    option = input(">> ").lower()

    if option not in OPTIONS:
        break

    match option:
        case "help":
            clear()
            for option in OPTIONS:
                print(f"{option}: {OPTIONS[option]}")

        case "sync_playlist":
            clear()
            if not PLAYLIST_TRACKING:
                print("PLAYLIST_TRACKING setting is not enabled, exiting...")
                continue
            while True:
                folder_path = input("Insert the path of the FOLDER you want to sync with the YouTube playlist: ")
                folder = Path(folder_path)
                if folder.exists() and folder.is_dir():
                    break
                print("ERROR: Invalid folder path")
            while True:
                playlist_url = input("Insert the YouTube playlist URL: ")
                if any(playlist_url.startswith(prefix) for prefix in YOUTUBE_PLAYLIST_URL_PREFIX):
                    break
                print("ERROR: Invalid playlist URL")

            print("Initiating sync...")
            youtube_playlist = extract_videos_from_playlist(playlist_url)

            folder_playlist = []
            with open(f"{folder}/{TRACKING_FILE_NAME}") as f:
                folder_playlist = f.read().splitlines()

            # Elements in youtube_playlist but NOT in folder_playlist (videos to download)
            videos_added = list(set(youtube_playlist) - set(folder_playlist))
            # Elements in folder_playlist but NOT in youtube_playlist (videos to delete)
            videos_removed = list(set(folder_playlist) - set(youtube_playlist))

            if len(videos_added) == 0 and len(videos_removed) == 0:
                print("The folder is already synced with the YouTube playlist, nothing to do")
                continue

            if len(videos_added) > 0:
                print("The following videos exists in YouTube playlist but not in folder:")
                for i, video in enumerate(videos_added): # fuck pythonic
                    print(f"{i + 1}: {video}")

            if len(videos_removed) > 0:
                print("The following videos does not exists in YouTube playlist but exists in folder:")
                for i, video in enumerate(videos_removed): # fuck pythonic
                    print(f"{i + 1}: {video}")

            print()
            if input("Proceed with sync? This will download all videos that are not present in folder and delete all videos not present in the YouTube playlist (y/n): ").lower() != "y":
                continue

            download_as_audio = False
            if len(videos_added) > 0:
                if input("Would you like to download the video(s) as AUDIO? (y/n): ").lower() == "y":
                    download_as_audio = True

            print("Proceeding with sync, please wait...")
            
            for video in videos_removed:
                video_title = get_video_title(video)
                files = os.listdir(folder_path)
                files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

                file_to_delete = None
                for file in files:
                    if video_title in file:
                        file_to_delete = file
                        break
                
                if file_to_delete:
                    os.remove(os.path.join(folder_path, file_to_delete))
                    print(f"Deleted: {file_to_delete}")
                else:
                    print(f"File not found for: {video_title}")

            # update progress on tracking file, just in case the pc turns off or something happens. Its not totally updated yet
            folder_playlist = [video for video in folder_playlist if video not in videos_removed]
            if not update_tracking_file(folder_path, folder_playlist):
                print("ERROR: Failed to update tracking file")
                continue

            # DOWNLOAD VIDEOS TO ADD NOW
            for video in videos_added:
                print(f"Downloading video: {video}")
                download_video(video.strip(), download_as_audio, output_folder=folder_path)
            
            # update tracking file with the youtube playlist
            if not update_tracking_file(folder_path, youtube_playlist):
                print("ERROR: Failed to update tracking file")
                continue

            print("Sync completed successfully")


folder = Path(OUTPUT_FOLDER_PATH)
if folder.exists() and folder.is_dir():
    if input(f"ALERT: {OUTPUT_FOLDER_PATH} folder already exists. Use it anyway? (y/n): ").lower() != "y":
        exit()

youtube_playlist = []
if input("Would you like to download a playlist? (y/n): ").lower() == "y":
    while len(youtube_playlist) == 0:
        clear()
        playlist_url = input("Insert the YouTube playlist URL: ")
        if not any(playlist_url.startswith(prefix) for prefix in YOUTUBE_PLAYLIST_URL_PREFIX):
            print("ERROR: Invalid playlist URL")
            input("Press any key to continue...")
            continue

        print("Extracting videos...")
        youtube_playlist = extract_videos_from_playlist(playlist_url)
        print("All videos extracted")

download_as_audio = False
if input("Would you like to download the video(s) as AUDIO? (y/n): ").lower() == "y":
    download_as_audio = True

clear()

# Download
if len(youtube_playlist) == 0: # Single video only
    url = input("Insert the URL of the video you want to download: ")
    download_video(url, download_as_audio)
else:
    urls_to_skip = []
    # Tracking file in OUTPUT_FOLDER_PATH
    if PLAYLIST_TRACKING and file_exists(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}"):
        with open(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}") as f:
            urls_to_skip = f.readlines()

    i=0
    for url in youtube_playlist:
        if url in urls_to_skip:
            print(f"URL {url} already exists in folder, skipping...")
            continue
        
        i+=1
        print(f"Downloading video {i} of {len(youtube_playlist)}...")
        download_video(url.strip(), download_as_audio)

        if PLAYLIST_TRACKING:
            with open(f"{OUTPUT_FOLDER_PATH}/{TRACKING_FILE_NAME}", 'a') as f:
                f.write(f"{url}")

if CHANGE_TRACK_NUMBER:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3
    from mutagen.id3._frames import TRCK

    mp3_files = [f for f in Path(OUTPUT_FOLDER_PATH).iterdir() 
             if f.is_file() and f.suffix.lower() == '.mp3' and f.name != TRACKING_FILE_NAME]

    i = len(mp3_files)

    for file in Path(OUTPUT_FOLDER_PATH).iterdir():
        if file.is_file():
            if file.name == TRACKING_FILE_NAME or file.suffix.lower() != '.mp3':
                print(f"Skipping file: {file.name}")
                continue
            
            audio_file = MP3(file, ID3=ID3)

            if audio_file.tags is None:
                audio_file.add_tags()

            if audio_file.tags is not None:
                track_number = i
                i -= 1
                audio_file.tags['TRCK'] = TRCK(encoding=3, text=str(track_number))
                audio_file.save()
                print(f"Changed track number for {file.name} to {track_number}")