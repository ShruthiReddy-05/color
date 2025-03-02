from flask import Flask, request, jsonify, send_file
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Color Blindness Correction Functions

def rgb_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)

def hsv_to_rgb(image):
    return cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_HSV2RGB)

def is_dominant_color(image, dominant_color):
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    if dominant_color == "red":
        return (r > g) & (r > b)
    elif dominant_color == "green":
        return (g > r) & (g > b)
    return np.zeros_like(r, dtype=bool)

def adjust_hsv(hsv, dominant_mask):
    h, s, v = hsv[:, :, 0] / 179.0, hsv[:, :, 1] / 255.0, hsv[:, :, 2] / 255.0
    h[dominant_mask] = (h[dominant_mask] + 0.3) % 1.0
    s = np.clip(s * 1.1, 0, 1)
    v = np.clip(v * 1.1, 0, 1)
    hsv[:, :, 0] = (h * 179).astype(np.uint8)
    hsv[:, :, 1] = (s * 255).astype(np.uint8)
    hsv[:, :, 2] = (v * 255).astype(np.uint8)
    return hsv

def correct_protanopia(image_path, output_path):
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]
    dominant_color = "red" if np.sum(r > g) + np.sum(r > b) > np.sum(g > r) + np.sum(g > b) else "green"
    hsv = rgb_to_hsv(img_np)
    dominant_mask = is_dominant_color(img_np, dominant_color)
    hsv = adjust_hsv(hsv, dominant_mask)
    result_img = Image.fromarray(hsv_to_rgb(hsv))
    result_img.save(output_path)

def daltonize(image_path, output_path, matrix):
    img = Image.open(image_path).convert("RGB")
    np_img = np.array(img, dtype=np.float32) / 255.0
    h, w, _ = np_img.shape
    np_img_flat = np_img.reshape(-1, 3)

    RGB_TO_LMS = np.array([
        [17.8824, 43.5161, 4.11935],
        [3.45565, 27.1554, 3.86714],
        [0.0299566, 0.184309, 1.46709]
    ])

    LMS_TO_RGB = np.array([
        [0.0809444479, -0.130504409, 0.116721066],
        [-0.0102485335, 0.0540193266, -0.113614708],
        [-0.000365296938, -0.00412161469, 0.693511405]
    ])

    LMS = np_img_flat @ RGB_TO_LMS.T
    LMS_cvd = LMS @ matrix.T
    simulated_rgb = LMS_cvd @ LMS_TO_RGB.T
    simulated_rgb = np.clip(simulated_rgb, 0, 1)

    error = np_img_flat - simulated_rgb
    correction = np.array([[0.0, 0.0, 0.0], [0.7, 1.0, 0.0], [0.7, 0.0, 1.0]])
    correction_applied = error @ correction.T
    corrected_rgb = np.clip(np_img_flat + correction_applied, 0, 1)
    corrected_img_np = (corrected_rgb.reshape(h, w, 3) * 255).astype(np.uint8)
    corrected_img = Image.fromarray(corrected_img_np, 'RGB')
    corrected_img.save(output_path)

CVD_MATRICES = {
    "deuteranopia": np.array([[1.0, 0.0, 0.0], [0.494207, 0.0, 1.24827], [0.0, 0.0, 1.0]]),
    "tritanopia": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-0.395913, 0.801109, 0.0]])
}

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files or 'type' not in request.form:
        return jsonify({"error": "Missing image or type"}), 400

    image = request.files['image']
    correction_type = request.form['type'].lower()

    if correction_type not in ['protanopia', 'deuteranopia', 'tritanopia']:
        return jsonify({"error": "Invalid type"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, image.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "corrected_" + image.filename)
    image.save(input_path)

    if correction_type == 'protanopia':
        correct_protanopia(input_path, output_path)
    else:
        daltonize(input_path, output_path, CVD_MATRICES[correction_type])

    return send_file(output_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
