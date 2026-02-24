# YouTube to MP3 Converter

A local web app that converts YouTube videos to MP3.

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) installed and on your PATH

## Setup

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install ffmpeg (needed for audio conversion):
   - **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Run

```
python app.py
```

Then open **http://localhost:5000** in your browser.

## Usage

1. Paste a YouTube URL into the input field
2. Click **Download**
3. The MP3 will download automatically when ready
