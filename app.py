import os
import tempfile
import re
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import imageio_ffmpeg

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

DOWNLOAD_DIR = tempfile.mkdtemp()


def is_valid_youtube_url(url):
    pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
    return bool(re.match(pattern, url))


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"].strip()
    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL"}), 400

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": ffmpeg_path,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "audio")
            # Find the downloaded mp3 file
            safe_title = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
            if not os.path.exists(safe_title):
                # Fallback: find any mp3 in the download dir
                mp3_files = [
                    f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")
                ]
                if not mp3_files:
                    return jsonify({"error": "MP3 file not found after download"}), 500
                safe_title = os.path.join(DOWNLOAD_DIR, mp3_files[-1])

        return send_file(
            safe_title,
            as_attachment=True,
            download_name=f"{title}.mp3",
            mimetype="audio/mpeg",
        )
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting YouTube to MP3 Converter...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=False, port=5000)
