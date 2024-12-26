from flask import Flask, request, jsonify, render_template
import os
import cv2
import pytesseract
from googletrans import Translator, LANGUAGES
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
translator = Translator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    languages = LANGUAGES
    return render_template('index.html', languages=languages)

@app.route('/translate-text', methods=['POST'])
def translate_text():
    source_text = request.form.get('text')
    source_lang = request.form.get('source_lang', 'auto')
    target_lang = request.form.get('target_lang')

    if not source_text or not target_lang:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        translated = translator.translate(source_text, src=source_lang, dest=target_lang)
        return jsonify({'translated_text': translated.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate-image', methods=['POST'])
def translate_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        img = cv2.imread(file_path)
        extracted_text = pytesseract.image_to_string(img)

        target_lang = request.form.get('target_lang', 'en')
        translated = translator.translate(extracted_text, dest=target_lang)

        return jsonify({
            'extracted_text': extracted_text,
            'translated_text': translated.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
