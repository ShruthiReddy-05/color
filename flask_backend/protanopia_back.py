# protanopia.py
import cv2
import numpy as np
import colorsys
from main import Flet

def rgb_to_hsl(r, g, b):
    return colorsys.rgb_to_hls(r/255, g/255, b/255)

def hsl_to_rgb(h, s, l):
    return colorsys.hls_to_rgb(h, l, s)

def adjust_hsl(h, s, l, dominant_color):
    if dominant_color == 'red':
        if abs(h - 0) < 0.1 or abs(h - 1) < 0.1:  # Red is near 0 or 1 in HSL
            h = (h + 0.3) % 1.0  # Adjust hue by 30%
            s = max(0, min(1, s - 0.1))  # Decrease saturation by 10%
            l = min(1, l + 0.25)  # Increase lightness by 25%
        else:
            s = min(1, s + 0.1)  # Increase saturation by 10%
            l = max(0, min(1, l - 0.1))  # Decrease lightness by 10%
    return h, s, l

def correct_protanopia(image):
    # Convert RGB image to HSL
    hsl_image = np.zeros_like(image, dtype=float)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r, g, b = image[i, j]
            h, l, s = rgb_to_hsl(r, g, b)
            hsl_image[i, j] = [h, l, s]

    # Determine the dominant color (red or green) based on average hue
    average_hue = np.mean(hsl_image[:, :, 0])
    dominant_color = 'red' if average_hue < 0.5 else 'green'

    # Adjust HSL values
    adjusted_hsl_image = np.zeros_like(hsl_image)
    for i in range(hsl_image.shape[0]):
        for j in range(hsl_image.shape[1]):
            h, l, s = hsl_image[i, j]
            adjusted_hsl_image[i, j] = adjust_hsl(h, s, l, dominant_color)

    # Convert HSL back to RGB
    corrected_image = np.zeros_like(image, dtype=np.uint8)
    for i in range(adjusted_hsl_image.shape[0]):
        for j in range(adjusted_hsl_image.shape[1]):
            h, l, s = adjusted_hsl_image[i, j]
            r, g, b = hsl_to_rgb(h, l, s)
            corrected_image[i, j] = [int(r*255), int(g*255), int(b*255)]

    return corrected_image

@Flet.register_function
def process_image(image_path):
    # Read the image file
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image file {image_path} not found.")

    # Correct for protanopia
    corrected_image = correct_protanopia(image)

    # Save the processed image
    processed_image_path = f'processed_{image_path}'
    cv2.imwrite(processed_image_path, corrected_image)
    
    return processed_image_path
