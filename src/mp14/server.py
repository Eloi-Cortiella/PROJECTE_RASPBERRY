from flask import Flask, send_from_directory, jsonify
import flask
import os
import importlib
from pathlib import Path


def main():
    static_path = Path(importlib.resources.files("mp14")) / "static"
    print(static_path)
    app = Flask(__name__)

    # Ruta on es guarden els vídeos
    video_path = Path.cwd() / "videos"

    @app.route("/")
    def index():
        return flask.send_file(static_path / "index.html")

    @app.route("/videos/<path:path>")
    def send_video(path):
        return send_from_directory(video_path, path)

    @app.route("/videos")
    def list_videos():
        files = [f for f in os.listdir(video_path) if f.endswith(".mp4")]
        return jsonify(videos=files)

    app.run(host="0.0.0.0", port=5050)


if __name__ == "__main__":
    main()
