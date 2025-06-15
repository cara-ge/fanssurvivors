from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': '缺少视频链接'}), 400

    try:
        filename = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, f'{filename}.%(ext)s')

        command = [
            'yt-dlp',
            '-o', output_path,
            url
        ]

        subprocess.run(command, check=True)

        return jsonify({'status': 'success', 'message': '下载完成', 'filename': filename})
    except subprocess.CalledProcessError:
        return jsonify({'status': 'error', 'message': '下载失败，请检查链接'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def home():
    return '视频下载后端服务运行中 ✅'
