import os, sys
import pyocr, pyocr.builders
import deepl
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
tools = pyocr.get_available_tools()
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
translator = deepl.Translator('c6d83823-f89e-753e-1c19-b3fcea525a1b:fx')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'sample1234'

# OCRが使えるかチェック
if len(tools) == 0:
    flash('ERROR:OCRツールが使えません', 'failed')
    sys.exit(1)

tool = tools[0]

# 拡張子の確認
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 画像アップロード設定
@app.route('/tr', methods=['POST'])
def translate():
    if 'file' in request.form:
        file = request.files['file']

        if file.filename == '':
            flash('ERROR:ファイルがありません', 'failed')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # OCRを実行する画像、言語、オプションの指定
            try:
                txt = tool.image_to_string(
                    Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)), # アップロードされた画像を指定する
                    lang = 'eng',
                    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
                )
                result = translator.translate_text(txt, target_lang="JA")

                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #uploadフォルダに保存された画像を削除する

                return render_template('index.html', orig_txt=txt, tr_txt=result)
            except ValueError as error:
                flash('ERROR:ValueError', 'failed')
                return redirect(request.url)
        else:
            flash('ERROR:拡張子が不正です', 'failed')
            return redirect(request.url)
    elif 'text' in request.form:
        txt = request.form.get('text')

        if txt == '':
            flash('ERROR:テキストが入力されていません', 'failed')
            return redirect(request.url)

        result = translator.translate_text(txt, target_lang="JA")

        return render_template('index.html', orig_txt=txt, tr_txt=result)
@app.route('/')
def index():
    return render_template('landing.html', landing='landing Page')

@app.route('/tr')
def tr():
    return render_template('index.html',
                           orig_txt='原文が表示されます。\n文字認識がおかしい場合は編集できます。\n編集したら再翻訳ボタンを押してください。',
                           tr_txt='翻訳文が表示されます。\n日本語にしたい英文の写った画像をアップロードしてください。\n毎月50万文字までしか翻訳できません。')

def main():
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)

if __name__ == '__main__':
    main()
