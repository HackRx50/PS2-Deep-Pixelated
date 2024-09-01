import os
import sys
import cv2
import pytesseract
import pandas as pd
import re
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from io import BytesIO

# Initialize the OCR model and processor
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
# pytesseract.pytesseract.tesseract_cmd = r'"C:/Program Files/Tesseract-OCR/tesseract.exe"'
# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/DELL/Downloads/ocrx.ai/Tesseract-OCR/tesseract.exe'


def convert_to_jpg(image: Image.Image) -> Image.Image:
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def process_image_and_generate_excel(image: Image.Image, image_name: str) -> dict:
    # Convert image to JPG
    image = convert_to_jpg(image)

    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert image to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to detect the position of the text "Provisional Diagnosis"
    custom_config = r'--oem 3 --psm 6'
    detection_data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)

    # Initialize variables for cropping
    start_y = 10
    end_x = end_y = 0
    start_x = 0

    # Look for the words "Provisional" and "Diagnosis" in the detection data
    for i, word in enumerate(detection_data['text']):
        if "Provisional" in word:
            start_x = detection_data['left'][i] + 300
            start_y = detection_data['top'][i]
            end_x = 1000 + start_x + detection_data['width'][i]
            end_y = 50 + start_y + detection_data['height'][i]
            break

    if start_x != 0 and end_x != 0:
        for i, word in enumerate(detection_data['text']):
            if "Diagnosis" in word:
                end_x = detection_data['left'][i] + detection_data['width'][i]
                end_y = max(end_y, detection_data['top'][i] + detection_data['height'][i])
                break

        # Define a margin to include more context if needed
        margin = 20
        roi = image_cv[start_y-margin:end_y+margin, start_x-margin:end_x+margin]

        # Save the cropped image temporarily
        cropped_image_path = "cropped_provisional_diagnosis.jpg"
        cv2.imwrite(cropped_image_path, roi)

        # Preprocess the cropped image
        image = Image.open(cropped_image_path).convert("RGB")
        image = ImageOps.grayscale(image)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image = image.filter(ImageFilter.SHARPEN)
        image = image.resize((1000, 1000), Image.LANCZOS)
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
        image = image.convert("RGB")

        # Prepare pixel values
        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        # Generate text
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Clean the extracted text
        cleaned_text = re.sub(r'[^A-Za-z]', ' ', generated_text).upper()
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return {
            'Image Name': image_name,
            'Provisional Diagnosis': cleaned_text
        }
    else:
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    results = []
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            result = process_image_and_generate_excel(image, filename)
            if result:
                results.append(result)

    # Create a DataFrame with the results
    df = pd.DataFrame(results)

    # Save the DataFrame to an Excel file
    with pd.ExcelWriter("provisional_diagnoses.xlsx", engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    print("Excel file generated: provisional_diagnoses.xlsx")

if __name__ == "__main__":
    main()
