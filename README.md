# ClairVue  

## Problem Statement  
**Enhancing Color Perception for Colorblind Individuals through Image Processing**  

## 🎯 Objective  
ClairVue is a user-friendly mobile application designed to enhance image colors for individuals with color vision deficiencies (CVD). It utilizes the **Daltonization algorithm** and the **Color Blind Filter Service (CBFS)** to provide tailored color adjustments based on the user's specific type of color blindness.  

---

## Problem Overview  
Colorblindness, or **color vision deficiency (CVD)**, affects approximately:  
🔹 **1 in 12 men**  
🔹 **1 in 200 women** worldwide  

This condition makes it difficult to distinguish between certain colors, impacting everyday activities such as:  
Reading color-coded maps  
- Identifying ripe fruits  
- Distinguishing traffic signals  
- Viewing digital content accurately  

Traditional solutions, like color-corrective lenses, are often **expensive** and **not universally effective**. There is a need for a more accessible, cost-effective digital solution.  

---

## Solution  
We propose **ClairVue**, a mobile application that enhances color differentiation in images for colorblind individuals.  

- **Backend :** Python-based image processing using the Daltonization algorithm  
- **Frontend :** Flutter for an intuitive user interface  
- **Deployment :** Seamlessly integrates with mobile devices for real-time processing  

Users can **scan or upload** images, select their color blindness type, and view a **real-time preview** of enhanced images with improved color perception.  

---

## Screenshots
<pre>
<img src = "https://github.com/ShruthiReddy-05/color/blob/main/assets/input.jpg" width = "250">  <img src = "https://github.com/ShruthiReddy-05/color/blob/main/assets/output.jpg" width = "250">
</pre>

## Key Features  

### 📷 Image Scanning & Uploading  
- Capture images using the camera or upload from the gallery  

### 🎨 Color Blindness Type Selection  
- Choose from **Protanopia, Deuteranopia, or Tritanopia** for customized color correction  

### 🖼 Real-time Preview  
- Instantly compare the **original** and **corrected** images side by side  

### 💾 Instant Save  
- Save the enhanced images **directly to your device** for future use  

---

## Impact  
ClairVue aims to **empower colorblind individuals** by improving their ability to:  
- Distinguish colors more effectively  
- Enhance daily interactions with digital and physical environments  
- Access a **free and efficient** alternative to expensive solutions  

With **ClairVue**, the world becomes more vivid, one image at a time.  

---

## 🛠️ Tech Stack  
- **Frontend :** Flutter  
- **Backend :** Python (Flask)  
- **Image Processing :** OpenCV, Daltonization Algorithm  
- **Storage & Deployment :** Render  

---

## 📥 Installation & Usage  
```sh
# Clone the repository
git clone https://github.com/ShruthiReddy-05/ClairVue.git
cd ClairVue

# Run Flask server
cd flask
python app.py

# Install Flutter dependencies
cd ..
cd clairvue
flutter pub get

# Run the app
flutter run
```

## 🔗 Future Enhancements  
- **Live Camera Preview :** Apply real-time color correction before capturing an image  
- **Custom Color Adjustment :** Allow users to fine-tune color enhancement levels   
- **Cloud Storage Integration :** Save processed images in the cloud for easy access   

---

## 🤝 Contributors  
| Name | GitHub Profile |  
|------|---------------|  
| **Shruthi Reddy** | [GitHub](https://github.com/ShruthiReddy-05) |  
| **Nikhil Parkar** | [GitHub](https://github.com/Nikhil-1426) |  

---

🚀 *Want to contribute? Fork the repo and submit a pull request!*  
