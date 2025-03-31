from flask import Flask, render_template, request, jsonify, send_file, url_for
from gtts import gTTS
from PIL import Image
import qrcode
import os
import uuid
from PyPDF2 import PdfReader
from fpdf import FPDF
from pdf2image import convert_from_path

app = Flask(__name__)

# Ensure subdirectories exist
os.makedirs('static/mp3', exist_ok=True)
os.makedirs('static/images/uploads', exist_ok=True)
os.makedirs('static/images/processed', exist_ok=True)
os.makedirs('static/pdf', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tts')
def tts_page():
    return render_template('tts.html')

@app.route('/image-compressor')
def image_compressor_page():
    return render_template('image_compressor.html')

@app.route('/qr-code')
def qr_code_page():
    return render_template('qr_code.html')

@app.route('/pdf-service')
def pdf_service_page():
    return render_template('pdf_service.html')

@app.route('/image-resizer')
def image_resizer_page():
    return render_template('image_resizer.html')

@app.route('/compress-image', methods=['POST'])
def compress_image():
    file = request.files['image']
    target_size_kb = int(request.form['size_kb'])
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join('static/images/uploads', unique_filename)
    output_path = os.path.join('static/images/processed', f"compressed_{unique_filename}")

    # Save the uploaded image
    file.save(input_path)

    # Compress the image
    img = Image.open(input_path)
    quality = 95
    while os.path.getsize(input_path) > target_size_kb * 1024 and quality > 10:
        img.save(output_path, optimize=True, quality=quality)
        quality -= 5

    return jsonify({'compressed_image_url': url_for('static', filename=f'images/processed/compressed_{unique_filename}')})

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    speed = request.form.get('speed', 'normal')
    gender = request.form.get('gender', 'female')

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join('static/mp3', filename)

    # Generate speech
    slow = speed == 'slow'
    tts = gTTS(text=text, lang='en', slow=slow)
    tts.save(output_path)

    return jsonify({'audio_url': url_for('static', filename=f'mp3/{filename}')})

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.form['data']
    unique_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join('static/images/processed', unique_filename)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

    return jsonify({'qr_code_url': url_for('static', filename=f'images/processed/{unique_filename}')})

@app.route('/create-pdf', methods=['POST'])
def create_pdf():
    files = request.files.getlist('images')
    pdf = FPDF()

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.pdf"
    output_path = os.path.join('static/pdf', filename)

    for file in files:
        # Save the uploaded file temporarily
        temp_image_path = os.path.join('static/images/uploads', file.filename)
        file.save(temp_image_path)

        # Add the image to the PDF
        pdf.add_page()
        pdf.image(temp_image_path, x=10, y=10, w=190)

    # Save the final PDF
    pdf.output(output_path)

    return jsonify({'pdf_url': url_for('static', filename=f'pdf/{filename}')})

@app.route('/split-pdf', methods=['POST'])
def split_pdf():
    file = request.files['pdf']
    pdf_path = os.path.join('static', 'uploaded.pdf')
    file.save(pdf_path)

    output_dir = os.path.join('static', 'pdf_pages')
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=200, output_folder=output_dir, fmt='jpg', output_file='page')

    image_urls = [os.path.join('static', 'pdf_pages', f'page-{i + 1}.jpg') for i in range(len(images))]

    return jsonify({'image_urls': image_urls})

@app.route('/resize-image', methods=['POST'])
def resize_image():
    file = request.files['image']
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join('static/images/uploads', unique_filename)
    output_path = os.path.join('static/images/processed', f"resized_{unique_filename}")

    # Save the uploaded image
    file.save(input_path)

    # Resize the image
    img = Image.open(input_path)
    img = img.resize((300, 300))  # Example: Resize to 300x300
    img.save(output_path)

    return jsonify({'resized_image_url': url_for('static', filename=f'images/processed/resized_{unique_filename}')})

@app.route('/google6cda3ef54c5c2da9.html')
def google_verification():
    return app.send_static_file('google6cda3ef54c5c2da9.html')

@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')

if __name__ == '__main__':
    app.run(debug=True)
