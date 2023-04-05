from flask import Flask, render_template, request
from PIL import Image
from model import load, classify
import os

app = Flask(__name__)

model, class_names = load()


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        image = Image.open(f.filename).convert("RGB")

        class_name, confidence_score = classify(image, model, class_names)
        os.remove(f.filename)

        data = {'Anime': class_name[1:], 'Confidence Score': confidence_score}
        return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)