import subprocess
from utils import delete_file
from config import OUTPUT_FOLDER_PATH, COOKIES_FILE_PATH, EMBED_THUMBNAIL, AUDIO_PARAMS, VIDEO_PARAMS, ADDITIONAL_PARAMS, SILENT_MODE, PLAYLIST_FILE_NAME

def extract_videos_from_playlist(playlist_url: str) -> None:
    delete_file(PLAYLIST_FILE_NAME)
    command = [
        "yt-dlp",
        "--flat-playlist",
        "-i",
        "--print-to-file", "url", PLAYLIST_FILE_NAME,
        playlist_url
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def download_video(video_url: str, download_as_audio: bool = False) -> None:
    command = ["yt-dlp", "--no-warnings", "--no-playlist", "--output", f"{OUTPUT_FOLDER_PATH}/%(title)s.%(ext)s"]

    if COOKIES_FILE_PATH != "":
        command.extend(["--cookies", COOKIES_FILE_PATH])

    if EMBED_THUMBNAIL:
        command.extend(["--embed-thumbnail"])

    if ADDITIONAL_PARAMS != "":
        command.extend(ADDITIONAL_PARAMS.split())

    if download_as_audio:
        command.extend(AUDIO_PARAMS.split())
    else:
        command.extend(VIDEO_PARAMS.split())
    
    command.append(video_url)

    if SILENT_MODE:
        subprocess.run(command, stdout=subprocess.DEVNULL)
    else:
        subprocess.run(command)