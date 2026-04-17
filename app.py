from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

@app.route('/')
def home():
    return render_template('index.html')

# 🔍 Pegar info do vídeo (preview)
@app.route('/info', methods=['POST'])
def get_info():
    url = request.json.get('url')

    ydl_opts = {'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for f in info['formats']:
            if f.get('height'):
                formats.append({
                    'format_id': f['format_id'],
                    'quality': f"{f['height']}p",
                    'ext': f['ext']
                })

        return jsonify({
            'title': info['title'],
            'thumbnail': info['thumbnail'],
            'formats': formats[:10]  # limita
        })

    except Exception as e:
        return jsonify({'error': str(e)})

# ⬇️ Download
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_id = request.form.get('format_id')

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': format_id,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=10000)