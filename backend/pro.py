from PIL import Image
import cv2
import numpy as np
#pro->red
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
    
    # Adjustments
    h[dominant_mask] = (h[dominant_mask] + 0.3) % 1.0  # Hue shift by 30%
    s *= 1.1  # Increase saturation
    v *= 1.1  # Increase brightness

    # Clamping
    s = np.clip(s, 0, 1)
    v = np.clip(v, 0, 1)

    hsv[:, :, 0] = (h * 179).astype(np.uint8)
    hsv[:, :, 1] = (s * 255).astype(np.uint8)
    hsv[:, :, 2] = (v * 255).astype(np.uint8)

    return hsv

def color_blind_filter(image_path, output_path):
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)

    # Determine dominant color
    r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]
    red_count = np.sum(r > g) + np.sum(r > b)
    green_count = np.sum(g > r) + np.sum(g > b)
    dominant_color = "red" if red_count > green_count else "green"

    hsv = rgb_to_hsv(img_np)
    dominant_mask = is_dominant_color(img_np, dominant_color)
    hsv = adjust_hsv(hsv, dominant_mask)

    result_img = Image.fromarray(hsv_to_rgb(hsv))
    result_img.save(output_path)
    print(f"Processed image saved at: {output_path}")

# Example usage
color_blind_filter("assets/sampletest.jpg", "assets/pro.jpg")
