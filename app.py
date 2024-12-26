from flask import Flask, request, jsonify, render_template, url_for
import os
import pytesseract
import cv2
from googletrans import Translator, LANGUAGES
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize dependencies
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
translator = Translator()

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/text')
def text_translation():
    return render_template('text.html', languages=LANGUAGES)

@app.route('/image')
def image_translation():
    return render_template('image.html', languages=LANGUAGES)

@app.route('/voice')
def voice_translation():
    return render_template('voice.html', languages=LANGUAGES)

@app.route('/translate-voice', methods=['POST'])
def translate_voice():
    # Receive the audio file from the request
    audio_file = request.files['audio'] 

    # **Implement voice-to-text conversion here**
    # Example using a hypothetical library (replace with actual implementation)
    try:
        text = convert_audio_to_text(audio_file) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # **Implement text translation here**
    # Example using a hypothetical translation function
    try:
        translated_text = translate_text(text, source_lang='en', target_lang='es') 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'translated_text': translated_text})

@app.route('/learn')
def learn_language():
    return render_template('learn.html', languages=LANGUAGES)

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.json
    source_text = data.get('text')
    source_lang = data.get('source_lang', 'auto')  # Default to 'auto' if not provided
    target_lang = data.get('target_lang')

    if not source_text or not target_lang:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Translate text using Google Translate
        translated = translator.translate(source_text, src=source_lang, dest=target_lang)
        return jsonify({'translated_text': translated.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to improve text extraction
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # You can also apply other preprocessing techniques like Gaussian blur, noise reduction, etc.
    # For example: blurred = cv2.GaussianBlur(thresh, (5, 5), 0)
    
    return thresh

@app.route('/translate-image', methods=['POST'])
def translate_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed file types are: png, jpg, jpeg'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(file_path)

        if preprocessed_image is None:
            return jsonify({'error': 'Failed to preprocess the image. Please upload a valid image file.'}), 400
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(preprocessed_image)

        if not extracted_text.strip():
            return jsonify({'error': 'No text could be extracted from the image'}), 400

        target_lang = request.form.get('target_lang', 'en')
        translated = translator.translate(extracted_text, dest=target_lang)

        return jsonify({
            'extracted_text': extracted_text,
            'translated_text': translated.text
        })

    except Exception as e:
        return jsonify({'error': f'Error during image processing or translation: {str(e)}'}), 500

    finally:
        # Clean up by removing the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
