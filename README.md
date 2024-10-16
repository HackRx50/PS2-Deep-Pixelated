<div align="center">
  <h1 style="font-size: 3.5em;">OCRxAI</h1>
  <h2 style="font-size: 2em;">Team Deep Pixelated</h2>
  <p>Team Members:</p>
  <p>Avi Gupta, Kartikey Bhatnagar, Vaishali Singh</p>
</div>

## Installation
To set up the project and install all required libraries, follow these steps:
### 1. Clone the Repository
   `git clone https://github.com/IVAVI17/OCRxAI.git`
### 2. Install the dependencies
  `pip install --default-timeout=100 -r requirements.txt`
### 3. Running the project
Once everything is set up, you can run the project using:
`uvicorn app:app --reload`

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
7. [About the team ](#6-about-the-team)

## 1. Overview
1. Automation of Diagnosis Extraction: OCRxAI automates the process of extracting medical diagnoses from handwritten forms, enhancing efficiency and accuracy in healthcare.
2. Advanced OCR Techniques: The solution leverages state-of-the-art OCR technology to accurately recognize and extract handwritten text, including complex medical diagnoses.
3. Streamlined Output: Extracted diagnoses are compiled into an Excel file, making it easy to integrate the data into existing healthcare systems.
4. Improved Claims Processing: By digitizing handwritten medical forms, OCRxAI streamlines the claims processing workflow, reducing manual errors and enhancing operational efficiency.

## 2. Problem Statement
Develop a solution to accurately extract medical diagnoses from handwritten medical forms to digitize medical forms and improve the efficiency as well as accuracy of claims processing.
LEVEL:1
Requirements: Implement a system to recognize and identify medical diagnoses from handwritten input medical forms.
Extract the value of each identified diagnosis on the handwritten form.
LEVEL:2
Requirements: Develop a post-extraction correction system to identify and fix any inaccuracies or errors in the extracted values. This is particularly important for handwritten values, which can be prone to misinterpretation.

## 3. Architecture
![Architecturelayer2](https://drive.google.com/uc?export=view&id=1cqx_fN69-DPOeEr1F5kVtqrHnswNA-yI)
![Architecturelayer1](https://drive.google.com/uc?export=view&id=12Q9p0B21xqDHYlzpV8PNLWsNx664sfKV)

## 4. Implementation
### 4.1 Understanding the problem statement and research 
Firstly, we start by inspecting the data set, to find out the text to be extracted and all the different scenarios, and then we started doing research on the models which we can be used to extract the handwritten text accurately 
![step1](https://drive.google.com/uc?export=view&id=1s41N5rUp4vjnjwyp23-e1R-8KUQIISs3)

### 4.2 Understanding the OCR model 
On doing research, and going through various models, we found out that the pytessaract library of python, which runs the OCR model, can be used to extract the text, and hence we did a sample run of it on few of the sample images, but we did not get the expected result

![step2](https://drive.google.com/uc?export=view&id=1s2yW_WFP1BaudWfFuYJa_Qk2DKhB9jUc)
![stp2.1](https://drive.google.com/uc?export=view&id=18d3WHA8iZD5byOA06Lcv_hDpji-qu-m-)

### 4.3 Extraction and cropping of only the Region of Interest (ROI)
And to further improve the accuracy, we decided to alter our model such that it will first detect the ROI using the PeddalOCR model, and then will crop that from the image, giving us just the provisional diagnosis

![step3](https://drive.google.com/uc?export=view&id=1WQEA6wOKb4AvEtWH48W_6aUm11SG29Vl)
![step3.1](https://drive.google.com/uc?export=view&id=1-N0cH-U_I1yO-oAG4iF8MNs9eXUlk3fI)

### 4.4 Processing of the image
Then the cropped image is further cleaned, by making it grayscale, enhancing it’s contrast, and also by binarization 
![step4](https://drive.google.com/uc?export=view&id=1VuJzKD6AprVM3n8fWK3BP4ow0Co351L3)

### 4.5 Extracting the text
After the cleaning, the handwritten text is being extracted using the Qwen/Qwen2-VL-2B-Instruct model

![step5](https://drive.google.com/uc?export=view&id=1_QSLINjJTSPAP7p7dBEB7GmsMYDynTTt)

### 4.6 Preprocessing of extracted text 
The extracted text is further cleaned and preprocessed
One key challenge we address is the use of abbreviations in medical terminology. To resolve this, we implement fuzzy matching against a curated dataset of medical terms, and then the text is stored into the excel file


## 5. USP of Our Solution
1. High-Precision Extraction
2. Automated “Region of Interest” Detection
3. Accurate identification of ICD10 codes using knowledge graphs.
4. Scalable Solution
5. Comprehensive Image Preprocessing
6. High Accuracy
7. Seamless Data Compilation

## 7. About The Team
1. We are Team Deep Pixelated, a group of tech enthusiasts united by our passion for innovation. Comprising [Avi Gupta](https://github.com/IVAVI17), [Kartikey Bhatnagar](https://github.com/kartikey-codes), and [Vaishali Singh](https://github.com/Vaishaliii25), we met during a college club event and quickly bonded over our shared interest in technology and solving real-world problems.
2. Each of us is pursuing a degree in Computer Science with different specializations. We’ve participated in several hackathons, including the Innovation X Hackathon at our college, where we secured third place.
3. Our past projects, like Shift Buddy, MedTalk AI, Signature Verification reflect our commitment to creating solutions that make a real impact. Through these projects, we’ve honed our ability to innovate and deliver practical applications that make a difference.
4. With OCRxAI, we're excited to further innovate in the healthcare sector, aiming to digitize and enhance medical processes. This project not only allows us to apply our technical knowledge to a critical industry but also provides us with the opportunity to learn, innovate.

