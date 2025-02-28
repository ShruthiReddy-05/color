import numpy as np
import cv2

# Transformation Matrices
Trgb2lms = np.array([
    [17.8824, 43.5161, 4.11935],
    [3.45565, 27.1554, 3.86714],
    [0.0299566, 0.184309, 1.46709]
])

Tlms2rgb = np.linalg.inv(Trgb2lms)

# CVD Matrices
CVD = {
    "Protanope": np.array([
        [0.0, 2.02344, -2.52581],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Deuteranope": np.array([
        [1.0, 0.0, 0.0],
        [0.494207, 0.0, 1.24827],
        [0.0, 0.0, 1.0]
    ]),
    "Tritanope": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [-0.395913, 0.801109, 0.0]
    ])
}

def apply_daltonization(img, deficiency_type):
    # Read and convert image to RGB
    imgIN = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert RGB to LMS
    imgLMS = np.tensordot(imgIN, Trgb2lms, axes=([2], [0]))
    
    # Apply CVD matrix
    cvd_matrix = CVD[deficiency_type]
    imgCVD = np.tensordot(imgLMS, cvd_matrix, axes=([2], [0]))
    
    # Convert LMS to RGB
    imgRGB = np.tensordot(imgCVD, Tlms2rgb, axes=([2], [0]))
    
    # Isolate invisible colors
    error_matrix = imgIN - imgRGB
    
    # Shift colors towards visible spectrum
    imgRGB[:, :, 0] += 0.0 * error_matrix[:, :, 0] + 0.0 * error_matrix[:, :, 1] + 0.0 * error_matrix[:, :, 2]
    imgRGB[:, :, 1] += 0.7 * error_matrix[:, :, 0] + 1.0 * error_matrix[:, :, 1] + 0.0 * error_matrix[:, :, 2]
    imgRGB[:, :, 2] += 0.7 * error_matrix[:, :, 0] + 0.0 * error_matrix[:, :, 1] + 1.0 * error_matrix[:, :, 2]
    
    # Clamp values to range [0, 255]
    imgRGB = np.clip(imgRGB, 0, 255).astype(np.uint8)
    
    return imgRGB

# Test the function
imgpath = "sampletest.jpg"
imgIN = cv2.imread(imgpath)
if imgIN is None:
    print("Error: Image not found or cannot be read.")
else:
    print("Image loaded successfully.")
    deficiency_type = "Tritanope"  # Change to "Deuteranope" or "Tritanope" as needed
    imgOUT = apply_daltonization(imgIN, deficiency_type)
    cv2.imwrite("daltonized_image.jpg", cv2.cvtColor(imgOUT, cv2.COLOR_RGB2BGR))
    print("Daltonized image saved successfully.")

