# yt-dlp-quick-tool

lightweight Python tool that streamlines the use of [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube videos and playlists. It offers a simple interactive interface and automates common tasks like playlist syncing, audio extraction, and download tracking.

---

## Purpose

This tool was made for users who want a quick and straightforward way to:

- Download individual YouTube videos or full playlists
- Keep a local folder in sync with a YouTube playlist

---

## Features

- Download single videos or entire playlists
- Sync a local folder with a YouTube playlist (add missing, delete removed)

---

## Requirements

- Python 3.9+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and available in your system's PATH
- [FFmpeg](https://ffmpeg.org/download.html) (required for audio extraction, format conversion, and thumbnail embedding)

---

## Configuration (via `config.py`)

You can edit the behavior of the tool by modifying `config.py`. Below is a breakdown of all the settings:

| Setting                    | Description                                                                                      | Default Value                                                                 |
|----------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `OUTPUT_FOLDER_PATH`       | Folder where downloaded files will be saved                                                     | `"Downloads"`                                                                  |
| `COOKIES_FILE_PATH`        | Path to cookies file for handling restricted/private videos                                     | `""` (empty string, cookies not used)                                          |
| `EMBED_THUMBNAIL`          | If `True`, embeds the video thumbnail                                                           | `False`                                                                        |
| `PLAYLIST_TRACKING`        | If `True`, stores downloaded playlist URLs to skip duplicates                                   | `False`                                                                        |
| `CHANGE_MODIFIED_DATE`     | If `True`, aligns the file's modified time to its creation time                                 | `False`                                                                        |
| `SILENT_MODE`              | If `True`, hides all yt-dlp output in the terminal                                              | `False`                                                                        |
| `AUDIO_PARAMS`             | yt-dlp flags used for audio downloads                                                           | `"-f bestaudio -x --audio-format mp3 --audio-quality 320k"`                   |
| `VIDEO_PARAMS`             | yt-dlp flags used for video downloads                                                           | `"-f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"`               |
| `ADDITIONAL_PARAMS`        | Extra global yt-dlp flags you may want to add (e.g., proxy, geo-bypass)                         | `""` (empty string, no extras)                                                 |

---

## Installation

```bash
git clone https://github.com/lucastozo/yt-dlp-quick-tool
cd yt-dlp-quick-tool
python main.py
