from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_path
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        output_name = request.form['output_name']

        # Save the PDF file
        pdf_path = os.path.join('static', pdf_file.filename)
        pdf_file.save(pdf_path)

        # Convert PDF to JPEG
        jpeg_path = os.path.join('static', output_name + '.jpg')
        pdf_to_jpeg(pdf_path, jpeg_path)

        # Return the JPEG file for download
        return send_file(jpeg_path, as_attachment=True)

    return render_template('index.html')

def pdf_to_jpeg(pdf_path, output_name):
    images = convert_from_path(pdf_path)
    images[0].save(output_name, "JPEG")
    print(f"PDF converted to JPEG: {output_name}")

if __name__ == '__main__':
    app.run(debug=True)

