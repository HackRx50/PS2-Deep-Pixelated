<div align = "center">
<h1> OCRxAI <h1>
</div>

## Installation
To set up the project and install all required libraries, follow these steps:
### 1. Clone the Repository
   git clone https://github.com/IVAVI17/OCRxAI.git
### 2. Install the dependencies
   pip install -r requirements.txt
### 3. Setting Up Tesseract-OCR
   The Tesseract-OCR libraries needed have been included in the repository. However, if you encounter any errors or if the files are corrupted during cloning, please follow these steps to set up Tesseract manually:
   1. Download the Tesseract-OCR libraries from the following link: [Tesseract OCR Download](https://github.com/UB-Mannheim/tesseract/wiki)
   2. Install the Tesseract-OCR libraries by following the installation instructions for your operating system
   3. After installation, add the installed Tesseract folder to the main project directory
   4. Open main.py and update the Tesseract command path by modifying the following line: pytesseract.pytesseract.tesseract_cmd = r'C:/Users/DELL/Downloads/tesseract_trial/Tesseract-OCR/tesseract.exe'
   5. Replace <path_to_your_tesseract_executable> with the full path to the tesseract.exe file in your system
   6. To ensure everything is set up correctly, run the following command to check the Tesseract version: tesseract --version     

### 4. Running the project
Once everything is set up, you can run the project using:
python main.py "path of the data set folder"

## Table of Contents
1. [Overview](#1-overview)
2. [Problem Statement](#2-problem-statement)
3. [Architecture](#3-architecture)
4. [Implementation](#4-implementation)
    1. [Understanding the problem statement and research](#41-understanding-the-problem-statement-and-research)
    2. [Understanding the OCR model](#42-understanding-the-ocr-model)
    3. [Extraction and cropping of only the Region of Interest (ROI)](#43-extraction-and-cropping-of-only-the-region-of-interest-roi)
    4. [Processing of the image](#44-processing-of-the-image)
    5. [Extracting the text, and storing it in an Excel file](#45-extracting-the-text-and-storing-it-in-an-excel-file)
    6. [Additional feature](#46-additional-feature)
5. [USP of Our Solution](#5-usp-of-our-solution)
6. [Future Enhancements ](#6-future-enhancements)

9. [About the team ](#6-about-the-team)

## 1. Overview
1. Automation of Diagnosis Extraction: OCRxAI automates the process of extracting medical diagnoses from handwritten forms, enhancing efficiency and accuracy in healthcare.
2. Advanced OCR Techniques: The solution leverages state-of-the-art OCR technology to accurately recognize and extract handwritten text, including complex medical diagnoses.
3. Streamlined Output: Extracted diagnoses are compiled into an Excel file, making it easy to integrate the data into existing healthcare systems.
4. Improved Claims Processing: By digitizing handwritten medical forms, OCRxAI streamlines the claims processing workflow, reducing manual errors and enhancing operational efficiency.

## 2. Problem Statement
Develop a solution to accurately extract medical diagnoses from handwritten medical forms to digitize medical forms and improve the efficiency as well as accuracy of claims processing.
Requirements: Implement a system to recognize and identify medical diagnoses from handwritten input medical forms.
Extract the value of each identified diagnosis on the handwritten form.

## 3. Architecture
![Architecturelayer2](https://drive.google.com/uc?export=view&id=1748qd6EcLlCqy1GXyywNhxXWn1-vtBrA)
![Architecturelayer1](https://drive.google.com/uc?export=view&id=1KPa05D9YxIrpItTig69nGsAl4TqTQ7nK)

## 4. Implementation
### 4.1 Understanding the problem statement and research 
Firstly, we start by inspecting the data set, to find out the text to be extracted and all the different scenarios, and then we started doing research on the models which we can be used to extract the handwritten text accurately 
![step1](https://drive.google.com/uc?export=view&id=1s41N5rUp4vjnjwyp23-e1R-8KUQIISs3)

### 4.2 Understanding the OCR model 
On doing research, and going through various models, we found out that the pytessaract library of python, which runs the OCR model, can be used to extract the text, and hence we did a sample run of it on few of the sample images, but we did not get the expected result
![step2](https://drive.google.com/uc?export=view&id=1s2yW_WFP1BaudWfFuYJa_Qk2DKhB9jUc)
![stp2.1](https://drive.google.com/uc?export=view&id=18d3WHA8iZD5byOA06Lcv_hDpji-qu-m-)

### 4.3 Extraction and cropping of only the Region of Interest (ROI)
And to further improve the accuracy, we decided to alter our model such that it will first detect the ROI using the EasyOCR model, and then will crop that from the image

![step3](https://drive.google.com/uc?export=view&id=1JF_N8Yud9enriZedtlcqrPwpP0DfHms4)
![step3.1](https://drive.google.com/uc?export=view&id=1_OlX27CMdk0Z0BLxKtFYTb5nBPaSEsvh)

### 4.4 Processing of the image
Then the cropped image is further cleaned, by making it grayscale, enhancing it’s contrast, and also by binarization 
![step4](https://drive.google.com/uc?export=view&id=1ehqmaxXqbYyfQ9LbV1rUn1wVmpqiHp93)

### 4.5 Extracting the text, and storing it in excel file
After the cleaning, the handwritten text is being extracted using the TrOCR model, and then we further clean the extracted text as well, and then save them all in the excel file, in the required format

![step5](https://drive.google.com/uc?export=view&id=1_QSLINjJTSPAP7p7dBEB7GmsMYDynTTt)

### 4.6 Additional feature 
We have also added a function, which converts the image of any format (png/jpeg) into jpg, so that the user can directly upload it, and not worry about it’s format 

![step6](https://drive.google.com/uc?export=view&id=1izCBZ4EQJrdncYxGzHHUAg3vr4jeTC_G)

## 5. USP of Our Solution
1. High-Precision Extraction
2. Automated “Region of Interest” Detection
3. Scalable Solution
4. Comprehensive Image Preprocessing
5. High Accuracy
6. Seamless Data Compilation

## 6. Future Enhancements
1. Multi-Language Support
2. Dynamic Prescription Format Handling
3. Advanced Data Analytics for Hospitals
4. Contextual Understanding
5. Efficient Large Document Processing
6. Improved Text Extraction Accuracy

## 9. About The Team
1. We are Team Deep Pixelated, a group of tech enthusiasts united by our passion for innovation. Comprising [Avi Gupta](https://github.com/IVAVI17), [Kartikey Bhatnagar](https://github.com/kartikey-codes), and [Vaishali Singh](https://github.com/Vaishaliii25), we met during a college club event and quickly bonded over our shared interest in technology and solving real-world problems.
2. Each of us is pursuing a degree in Computer Science with different specializations. We’ve participated in several hackathons, including the Innovation X Hackathon at our college, where we secured third place.
3. Our past projects, like Shift Buddy, MedTalk AI, Signature Verification reflect our commitment to creating solutions that make a real impact. Through these projects, we’ve honed our ability to innovate and deliver practical applications that make a difference.
4. With OCRxAI, we're excited to further innovate in the healthcare sector, aiming to digitize and enhance medical processes. This project not only allows us to apply our technical knowledge to a critical industry but also provides us with the opportunity to learn, innovate.

