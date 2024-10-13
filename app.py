from fastapi import FastAPI, UploadFile, File, HTTPException, Form
import shutil
import os
import pandas as pd
from segmentation import extract_provisional_diagnosis
from ocr import extract_text_from_image
from typing import List
import glob
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime
from abbreviation import replace_abbreviations, load_abbreviations
from masking import detect_and_blur_details


app = FastAPI()

# Temporary directories to save uploaded files and cropped images
UPLOAD_DIR = "uploads/"
CROPPED_DIR = "cropped/"
EXCEL_FILE = "diagnosis_output.xlsx"
ABBREVIATION_FILE_PATH = 'Datasets/medical_terms_abbreviations.txt'


# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)

# Initialize or load existing Excel file
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Image Name", "Provisional Diagnosis"])
    df.to_excel(EXCEL_FILE, index=False)

def clean_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Apply Gaussian Blur to remove noise
    img = img.filter(ImageFilter.GaussianBlur(radius=1))

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Increase contrast

    # Save the cleaned image to a temporary location
    cleaned_image_path = image_path.replace(".jpg", "_cleaned.jpg")  # Change extension as needed
    img.save(cleaned_image_path)

    return cleaned_image_path



@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        start_time = datetime.now()  # Start time recording

        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        blurred_image_path = detect_and_blur_details(file_path)
        


        # Step 1: Crop the "Provisional Diagnosis" section
        cropped_path = os.path.join(CROPPED_DIR, f"cropped_{file.filename}")
        # cropped_image = extract_provisional_diagnosis(file_path, cropped_path)
        cropped_image = extract_provisional_diagnosis(blurred_image_path, cropped_path)

        if cropped_image is None:
            raise HTTPException(status_code=404, detail="No 'Provisional Diagnosis' section found.")
        
        
        # Step 2: Clean the cropped image
        # cleaned_image_path = clean_image(cropped_image)

        # (Optional) Set DPI if needed before sending to Qwen2 (handled in the clean_image function if applicable)
        # # You can also save the cleaned image with specified DPI settings if necessary.
        # cleaned_image = Image.open(cleaned_image_path)
        # cleaned_image.save(cleaned_image_path, dpi=(300, 300))

        # Step 2: Extract the text from the cropped image using Qwen2
        extracted_text = extract_text_from_image(cropped_image)
        # extracted_text = extract_text_from_image(cleaned_image_path)
        abbreviations_dict = load_abbreviations(ABBREVIATION_FILE_PATH)
        refined_text = replace_abbreviations(extracted_text[0], abbreviations_dict)


        # Load existing Excel file
        df = pd.read_excel(EXCEL_FILE)
        end_time = datetime.now()
        process_time = (end_time - start_time).total_seconds()
        print("processing time", process_time)


        # Create a new entry as a DataFrame
        new_entry = pd.DataFrame({"Image Name": [file.filename], "Provisional Diagnosis": [extracted_text[0]]})

        # Concatenate the new entry with the existing DataFrame
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save the updated DataFrame to the Excel file
        df.to_excel(EXCEL_FILE, index=False)

        # Return the extracted text
        return {"extracted_text": extracted_text, "refined_text": refined_text, "processed time": process_time}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-folder/")
async def process_folder(folder_path: str = Form(...)):
    try:
        # Get all image files from the folder
        image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + \
                      glob.glob(os.path.join(folder_path, "*.jpeg")) + \
                      glob.glob(os.path.join(folder_path, "*.png"))  # Add more extensions as needed

        if not image_files:
            raise HTTPException(status_code=404, detail="No images found in the folder.")

        # Load existing Excel file
        df = pd.read_excel(EXCEL_FILE)

        # Process each image
        for image_file in image_files:
            # Step 1: Crop the "Provisional Diagnosis" section
            cropped_path = os.path.join(CROPPED_DIR, f"cropped_{os.path.basename(image_file)}")
            cropped_image = extract_provisional_diagnosis(image_file, cropped_path)

            if cropped_image is None:
                continue  # Skip if no "Provisional Diagnosis" section found   
            
            extracted_text = extract_text_from_image(cropped_image)
            abbreviations_dict = load_abbreviations(ABBREVIATION_FILE_PATH)
            refined_text = replace_abbreviations(extracted_text[0], abbreviations_dict)



            # extracted_text = extract_text_from_image(cleaned_image_path)
            
            # new_entry = pd.DataFrame({"Image Name": [os.path.basename(image_file)], "Provisional Diagnosis": [extracted_text[0]]})
            new_entry = pd.DataFrame({"Image Name": [os.path.basename(image_file)], "Provisional Diagnosis": refined_text})

            df = pd.concat([df, new_entry], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False)

        return {"message": f"Processed {len(image_files)} images from the folder successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI app, use: uvicorn app:app --reload
