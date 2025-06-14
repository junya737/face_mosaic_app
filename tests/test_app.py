import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image
import cv2

# Allow importing the app module from the repository root
sys.path.append(str(Path(__file__).resolve().parents[1]))
import app


def test_mosaic_area_basic():
    # use an image with varying values so mosaic changes pixels
    img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
    original = img.copy()
    app.mosaic_area(img, 10, 10, 20, 20, downscale=0.5)
    assert not np.array_equal(img[10:30, 10:30], original[10:30, 10:30])
    # area outside mosaic remains the same
    assert np.array_equal(img[:10, :], original[:10, :])


def test_index_returns_image(monkeypatch):
    class DummyCascade:
        def detectMultiScale(self, *args, **kwargs):
            return np.array([[0, 0, 20, 20]])

    monkeypatch.setattr(cv2, "CascadeClassifier", lambda *args, **kwargs: DummyCascade())
    client = app.app.test_client()
    image = Image.new("RGB", (20, 20), color=(255, 0, 0))
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    data = {"image": (buf, "test.jpg")}
    resp = client.post("/", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert resp.mimetype == "image/jpeg"
