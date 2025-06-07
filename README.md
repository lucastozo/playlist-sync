# playlist-sync

A Python wrapper around yt-dlp that makes downloading videos and playlists easier, with some extra features for playlist management.

## Why This Exists

I cancelled my YouTube Premium subscription and lost access to offline downloads in YouTube Music. I had playlists with hundreds of songs that I wanted to keep locally, but I also wanted them to stay in sync - when I remove a song from my playlist because I'm tired of it, I want it gone from my local folder too. When I discover new music and add it to the playlist, I want it downloaded automatically.

Basically, I wanted my local music folder to behave like YouTube Music's offline downloads used to, but without paying for Premium.

So I built this tool around yt-dlp to handle that workflow. Then I figured other people might have the same problem, so here it is.

## What It Does

- Downloads single videos or entire playlists
- Converts to audio (MP3) or keeps as video
- Tracks what you've downloaded to avoid duplicates
- **Playlist sync**: Keeps your local folder in sync with a YouTube playlist - downloads new videos, deletes removed ones

The playlist sync is the main feature that makes this different from just using yt-dlp directly. It's designed for music collections where you actively curate playlists and want your local copies to match.

## Installation & Setup

You need yt-dlp installed first:
```bash
pip install yt-dlp
```

Then just clone this repo and run it:
```bash
git clone https://github.com/lucastozo/yt-dlp-quick-tool
cd yt-dlp-quick-tool
python main.py
```

## Configuration

Edit `config.py` to change:
- Download folder
- Audio/video quality settings  
- Whether to embed thumbnails
- Cookie file path (if you need to access private playlists)

## Usage

Run `python main.py` and follow the prompts. It's pretty straightforward:

1. Choose single video or playlist
2. Choose audio or video format
3. Enter URL(s)
4. Wait for downloads

For playlist syncing, use the "sync_playlist" option. **Warning**: This will delete local files that aren't in the playlist anymore. That's intentional for music curation, but make sure you understand what it's doing.

## Features

- **Playlist tracking**: Avoids re-downloading videos you already have
- **Playlist sync**: Keeps local folder matched with YouTube playlist (adds new, removes old)
- **Audio extraction**: Downloads as MP3 with configurable quality
- **Thumbnail embedding**: Optional thumbnail embedding in audio files
- **Date matching**: Can set file modified date to match creation date

## Limitations & Warnings

- The playlist sync feature **deletes files**. It's designed for music where you want your local collection to match your current playlist exactly
- File matching for deletion is based on video title, which isn't perfect
- This was built for my personal workflow, so some design decisions might seem weird if you have different needs
- Error handling could be better
- The UI is pretty basic (it's a terminal script)

## Is This For You?

This tool is great if you:
- Want to replace YouTube Music offline downloads
- Actively curate playlists and want local copies to stay in sync
- Don't mind a simple terminal interface
- Are comfortable with the sync feature potentially deleting files

It might not be for you if you:
- Just want to download videos occasionally (use yt-dlp directly)
- Want a GUI
- Need fine-grained control over what gets deleted
- Are worried about the sync feature being too aggressive

## Contributing

Feel free to open issues or PRs. This started as a personal tool so there's definitely room for improvement, especially around error handling and user experience.
