# run for fastAPI
# uvicon app:app --reload

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
import cv2
import os
import shutil
from io import BytesIO
import pandas as pd
from utils.segmentation import extract_provisional_diagnosis
from utils.ocr import extract_text_from_image
import glob
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime
from utils.abbreviation import replace_abbreviations, load_abbreviations
from fastapi.responses import JSONResponse
from utils.rag import get_icd10_code



app = FastAPI()

UPLOAD_DIR = "uploads/"
CROPPED_DIR = "cropped/"
EXCEL_FILE = "diagnosis_output.xlsx"
ABBREVIATION_FILE_PATH = 'Dataset/medical_terms_abbreviations.txt'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Image Name", "Provisional Diagnosis"])
    df.to_excel(EXCEL_FILE, index=False)
    


@app.post("/extract_diagnosis")
async def extract_diagnosis(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        cropped_img = extract_provisional_diagnosis(image_bytes)
        if cropped_img is not None:
            cropped_image_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
            # cropped_image_pil = Image.open(BytesIO(image_bytes))

            extracted_diagnosis = extract_text_from_image(cropped_image_pil)
            if isinstance(extracted_diagnosis, list):
                extracted_diagnosis = ' '.join(extracted_diagnosis)

            abbreviations_dict = load_abbreviations(ABBREVIATION_FILE_PATH)            
            extracted_abbreviated_diagnosis = replace_abbreviations(extracted_diagnosis, abbreviations_dict)

            icd10_result = get_icd10_code(extracted_abbreviated_diagnosis)
            print(get_icd10_code(extracted_abbreviated_diagnosis))
            if icd10_result is not None:
               
                data = {
                    "Extracted Text": extracted_abbreviated_diagnosis,
                    "orgininal": extracted_diagnosis,
                    "ICD-10 Code": icd10_result.get("icd10_code"),
                    "Description": icd10_result.get("description")
                }
                if os.path.exists(EXCEL_FILE):
                    df = pd.read_excel(EXCEL_FILE)
                else:
                    df = pd.DataFrame(columns=["Extracted Text", "Refined Diagnosis", "ICD-10 Code", "Description"])
                new_entry = pd.DataFrame([data])
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                # Return the results
                return data
            else:
                return JSONResponse(content={"error": "Could not retrieve ICD-10 code"}, status_code=500)
        else:
            return JSONResponse(content={"error": "Could not extract provisional diagnosis section"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/process-folder/")
async def process_folder(folder_path: str = Form(...)):
    try:

        os.makedirs(CROPPED_DIR, exist_ok=True)

        image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + \
                      glob.glob(os.path.join(folder_path, "*.jpeg")) + \
                      glob.glob(os.path.join(folder_path, "*.png"))

        if not image_files:
            raise HTTPException(status_code=404, detail="No images found in the folder.")

        processing_results = []

        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
        else:
            df = pd.DataFrame(columns=["Image Name", "Extracted Text", "Refined Diagnosis", "ICD-10 Code", "Description"])


        for image_file in image_files:
            with open(image_file, 'rb') as f:
                image_bytes = f.read()

            # Process the image (e.g., crop diagnosis area, extract text)
            cropped_image = extract_provisional_diagnosis(image_bytes)

            if cropped_image is None:
                processing_results.append({
                    "image_name": os.path.basename(image_file),
                    "error": "Could not extract provisional diagnosis section"
                })
                continue  

            cropped_image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

            extracted_text = extract_text_from_image(cropped_image_pil)
            if isinstance(extracted_diagnosis, list):
                extracted_diagnosis = ' '.join(extracted_diagnosis)
            abbreviations_dict = load_abbreviations(ABBREVIATION_FILE_PATH)
            extracted_abbreviated_diagnosis = replace_abbreviations(extracted_text, abbreviations_dict)

            icd10_result = get_icd10_code(extracted_abbreviated_diagnosis)

            new_entry = {
                "Image Name": os.path.basename(image_file),
                "Extracted Text": extracted_abbreviated_diagnosis,
                "ICD-10 Code": icd10_result.get("icd10_code") if icd10_result else None,
                "Description": icd10_result.get("description") if icd10_result else None
            }

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

            processing_results.append(new_entry)

        df.to_excel(EXCEL_FILE, index=False)

        return JSONResponse(content={"processed_images": processing_results}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

