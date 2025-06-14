from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__)


def mosaic_area(img, x, y, w, h, downscale=0.1):
    # clip bounding box to image boundaries
    h_img, w_img = img.shape[:2]
    x = max(0, x)
    y = max(0, y)
    w = min(w_img - x, w)
    h = min(h_img - y, h)

    roi = img[y:y+h, x:x+w]
    if roi.size == 0:
        return img
    # Downscale then upscale to create pixelation (mosaic)
    small = cv2.resize(roi, (0, 0), fx=downscale, fy=downscale, interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    img[y:y+h, x:x+w] = mosaic
    return img


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='画像ファイルがありません')
        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error='画像ファイルがありません')
        # Load image using PIL then convert to OpenCV format
        image = Image.open(file.stream).convert('RGB')
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            img = mosaic_area(img, x, y, w, h, downscale=0.05)

        # Convert back to bytes
        _, buf = cv2.imencode('.jpg', img)
        return send_file(BytesIO(buf.tobytes()), mimetype='image/jpeg')
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
