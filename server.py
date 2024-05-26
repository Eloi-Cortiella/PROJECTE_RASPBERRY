from flask import Flask, send_from_directory, jsonify
import os

def main():
    app = Flask(__name__)

    # Ruta on es guarden els vídeos
    VIDEO_DIR = './videos'

    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')

    @app.route('/videos/<path:path>')
    def send_video(path):
        return send_from_directory(VIDEO_DIR, path)

    @app.route('/videos')
    def list_videos():
        files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
        return jsonify(videos=files)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)