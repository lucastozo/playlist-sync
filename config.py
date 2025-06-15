OUTPUT_FOLDER_PATH = "Downloads"
COOKIES_FILE_PATH = "" # Leave it empty if you do not need cookies file. Example: "/path/to/cookies.txt"

EMBED_THUMBNAIL = False # Download the video thumbnail
PLAYLIST_TRACKING = False # This will keep a file inside the OUTPUT_FOLDER_PATH containing all URLs downloaded from the playlist. This is useful to not waste time trying to download videos that already exists
CHANGE_MODIFIED_DATE = False # Enabling this will make the Date modified property the same as Date created
SILENT_MODE = False # Enabling this will hidden yt-dlp download info on terminal

AUDIO_PARAMS = "-f bestaudio -x --audio-format mp3 --audio-quality 320k"
VIDEO_PARAMS = "-f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
ADDITIONAL_PARAMS = "" # Additional yt-dlp options you may want to use

# APP INFO AND SETTINGS, DO NOT CHANGE VALUES BELOW
APP_NAME = "playlist-sync"
VERSION = "1.0.1"
PLAYLIST_FILE_NAME = ".playlist"
TRACKING_FILE_NAME = ".tracking"

YOUTUBE_PLAYLIST_URL_PREFIX = ["https://youtube.com/playlist?list=", "https://www.youtube.com/playlist?list="]