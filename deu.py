from PIL import Image
import numpy as np
#deu->green
# Deuteranope (Green-Blind) Simulation Matrix
CVDMatrix = {
    "Deuteranope": np.array([
        [1.0, 0.0, 0.0],
        [0.494207, 0.0, 1.24827],
        [0.0, 0.0, 1.0]
    ])
}

# RGB to LMS conversion matrix
RGB_TO_LMS = np.array([
    [17.8824, 43.5161, 4.11935],
    [3.45565, 27.1554, 3.86714],
    [0.0299566, 0.184309, 1.46709]
])

# LMS to RGB conversion matrix
LMS_TO_RGB = np.array([
    [0.0809444479, -0.130504409, 0.116721066],
    [-0.0102485335, 0.0540193266, -0.113614708],
    [-0.000365296938, -0.00412161469, 0.693511405]
])

def daltonize(image_path, output_path):
    img = Image.open(image_path).convert("RGB")
    np_img = np.array(img, dtype=np.float32) / 255.0  # Normalize to [0,1]

    # Flatten the image array
    h, w, _ = np_img.shape
    np_img_flat = np_img.reshape(-1, 3)

    # Convert to LMS space
    LMS = np_img_flat @ RGB_TO_LMS.T

    # Simulate color blindness
    cvd_matrix = CVDMatrix["Deuteranope"]
    LMS_cvd = LMS @ cvd_matrix.T

    # Convert back to RGB
    simulated_rgb = LMS_cvd @ LMS_TO_RGB.T
    simulated_rgb = np.clip(simulated_rgb, 0, 1)  # Keep values in [0,1]

    # Calculate error matrix
    error = np_img_flat - simulated_rgb

    # Adjust colors to compensate
    correction = np.array([
        [0.0, 0.0, 0.0], 
        [0.7, 1.0, 0.0], 
        [0.7, 0.0, 1.0]
    ])

    correction_applied = error @ correction.T
    corrected_rgb = np_img_flat + correction_applied
    corrected_rgb = np.clip(corrected_rgb, 0, 1)  # Clamp RGB values

    # Reshape back to image shape
    corrected_img_np = (corrected_rgb.reshape(h, w, 3) * 255).astype(np.uint8)
    corrected_img = Image.fromarray(corrected_img_np, 'RGB')
    
    corrected_img.save(output_path)
    print(f"Processed image saved at: {output_path}")

# Example usage
daltonize("sampletest.jpg", "deu.jpg")
