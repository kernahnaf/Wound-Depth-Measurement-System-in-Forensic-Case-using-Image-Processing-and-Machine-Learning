# 🧬 Forensic Wound Measurement System using Computer Vision and Machine Learning

<p align="center">
  <img src="Picture1.jpg" width="15%" />
  <img src="Picture2.jpg" width="15%" />
  <img src="Picture3.png" width="15%" />
  <br>
  <img src="Picture4.jpg" width="15%" />
  <img src="Picture5.png" width="15%" />
  <img src="Picture6.jpg" width="15%" />
</p>

A Python-based system developed as a final year undergraduate thesis (2023–2024), focusing on wound measurement in forensic cases using image processing and machine learning.

## 📄 Journal Publication of The Research Project
[![Read Journal](https://img.shields.io/badge/Journal-Read-blue)](https://www.researchsquare.com/article/rs-5406106/latest)

## 🎥 Project Demo Video
[![Watch on YouTube](https://img.shields.io/badge/YouTube-Video-red?logo=youtube)](https://youtu.be/_fo2EKS3LKY)

## 🔍 Project Overview

This project aims to measure wound dimensions (length, width, and depth) from forensic imagery in collaboration with Bhayangkara Hospital Yogyakarta. It consists of two main measurement components:

- **Length & Width Estimation:**  
  Utilizes ArUco markers to convert image pixels into metric units. Two modes are available:  
  - **Manual Mode:** Users draw a line across the wound to get the measurements.  
  - **Automatic Mode:** Measurements are detected automatically without user input.

    <img src="Picture8.jpg" width="300" alt="Drawing lines">

- **Depth Estimation:**  
  Uses Pressure Ulcer classification standards and applies Support Vector Machine (SVM) algorithms for classifying wound depth based on image features.
  **Note:** Feature extraction in this model can be expanded further by incorporating additional visual features such as color histograms, texture descriptors (e.g., LBP, GLCM), edge sharpness, and shape metrics to improve classification accuracy.

    <img src="Picture7.jpg" width="800" alt="Pressure Ulcer Classification">

### 🎯 Key Features:
- **Collaboration:** Developed with support from Bhayangkara Hospital, Yogyakarta.
- **Measurement Modes:**
  - Manual interaction (drawing line annotations)
  - Fully automatic wound detection
- **Reference Calibration:** Aruco markers used for real-world scaling
- **Machine Learning:**
  - Depth classification using SVM based on Pressure Ulcer stages
- **Practical Application:** Forensic and medical investigation aid

⚠️ **Note on Data Privacy:**  
The dataset used in this project **cannot be shared** due to **ethical and medical privacy regulations** regarding sensitive patient data.

## 🛠️ Technical Implementation

| 🔧 Component            | 💻 Implementation                          |
|-------------------------|-------------------------------------------|
| Image Processing        | OpenCV, Aruco Marker Detection            |
| Automatic Measurement   | Contour Detection, Object Detection        |
| Depth Classification    | scikit-learn (SVM model)                  |
| Data Labeling           | Pressure Ulcer Stage Classification       |
| Visualization           | real-world scaled outputs     |
