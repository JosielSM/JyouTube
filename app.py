from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality')

    if not url:
        return "Erro: URL não fornecida"

    # Define formato baseado na escolha
    if quality == "720":
        format_option = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "480":
        format_option = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    elif quality == "worst":
        format_option = "worst"
    else:
        format_option = "best"

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': format_option,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if not os.path.exists(filename):
            return "Erro: arquivo não encontrado."

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar: {str(e)}"

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)