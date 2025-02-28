from PIL import Image
import numpy as np
#tri->blue
CVDMatrix = {
    "Tritanope": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [-0.395913, 0.801109, 0.0]
    ])
}

# RGB to LMS and LMS to RGB transformation matrices
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

def daltonize(image_path):
    img = Image.open(image_path).convert("RGB")
    np_img = np.array(img, dtype=float) / 255.0  # Normalize to [0,1]

    # Flatten the image array for batch processing
    h, w, c = np_img.shape
    flat_img = np_img.reshape(-1, 3)

    # Convert to LMS color space
    lms = flat_img @ RGB_TO_LMS.T

    # Simulate color blindness
    lms_cvd = lms @ CVDMatrix["Tritanope"].T

    # Convert back to RGB
    sim_rgb = lms_cvd @ LMS_TO_RGB.T

    # Compute the error matrix
    error = flat_img - sim_rgb

    # Apply correction
    correction = error @ np.array([
        [0.0, 0.0, 0.0],  
        [0.7, 1.0, 0.0],  
        [0.7, 0.0, 1.0]  
    ]).T

    # Apply correction and clip values
    corrected_img = np.clip(flat_img + correction, 0, 1) * 255.0
    corrected_img = corrected_img.reshape(h, w, 3).astype(np.uint8)

    # Save the corrected image
    corrected_img = Image.fromarray(corrected_img)
    return corrected_img

# Example usage
corrected_image = daltonize("sampletest.jpg")
corrected_image.save("tri.jpg")
