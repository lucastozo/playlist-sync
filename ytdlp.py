import subprocess
from utils import delete_file
from config import OUTPUT_FOLDER_PATH, COOKIES_FILE_PATH, EMBED_THUMBNAIL, AUDIO_PARAMS, VIDEO_PARAMS, ADDITIONAL_PARAMS, SILENT_MODE, PLAYLIST_FILE_NAME

def extract_videos_from_playlist(playlist_url: str, output_path = PLAYLIST_FILE_NAME) -> list[str]:
    delete_file(output_path)
    command = [
        "yt-dlp",
        "--flat-playlist",
        "-i",
        "--print-to-file", "url", output_path,
        playlist_url
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        delete_file(output_path)
        return urls
    except FileNotFoundError:
        delete_file(output_path)
        return []

def download_video(video_url: str, download_as_audio: bool = False, output_folder: str = OUTPUT_FOLDER_PATH) -> None:
    command = ["yt-dlp", "--no-warnings", "--no-playlist", "--output", f"{output_folder}/%(title)s.%(ext)s"]

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

def get_video_title(video_url: str) -> str:
    command = [
        "yt-dlp",
        "--print", "title",
        "--no-warnings",
        video_url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error getting title: {result.stderr}")
            return "Unknown Title"
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown Title"