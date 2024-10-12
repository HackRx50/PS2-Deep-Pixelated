import os
import sys
import glob
import pandas as pd
from PIL import Image, ImageFilter, ImageEnhance
from segmentation import extract_provisional_diagnosis
from ocr import extract_text_from_image

# Temporary directories to save cropped images
CROPPED_DIR = "cropped/"
EXCEL_FILE = "diagnosis_output.xlsx"

# Ensure the cropped directory exists
os.makedirs(CROPPED_DIR, exist_ok=True)

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Image Name", "Provisional Diagnosis"])
    df.to_excel(EXCEL_FILE, index=False)

def clean_image(image_path):

    img = Image.open(image_path)

    img = img.convert("L")

    img = img.filter(ImageFilter.GaussianBlur(radius=1))

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  

    cleaned_image_path = image_path.replace(".jpg", "_cleaned.jpg")  # Change extension as needed
    img.save(cleaned_image_path)

    return cleaned_image_path

def process_folder(folder_path):
    try:
        # Get all image files from the folder
        image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + \
                      glob.glob(os.path.join(folder_path, "*.jpeg")) + \
                      glob.glob(os.path.join(folder_path, "*.png"))  # Add more extensions as needed

        if not image_files:
            print("No images found in the folder.")
            return

        # Load existing Excel file
        df = pd.read_excel(EXCEL_FILE)

        # Process each image
        for image_file in image_files:
            # Step 1: Crop the "Provisional Diagnosis" section
            cropped_path = os.path.join(CROPPED_DIR, f"cropped_{os.path.basename(image_file)}")
            cropped_image = extract_provisional_diagnosis(image_file, cropped_path)

            if cropped_image is None:
                continue   
            
            cleaned_image_path = clean_image(cropped_image)

            cleaned_image = Image.open(cleaned_image_path)
            cleaned_image.save(cleaned_image_path, dpi=(300, 300))      

            extracted_text = extract_text_from_image(cleaned_image_path)

            new_entry = pd.DataFrame({"Image Name": [os.path.basename(image_file)], "Provisional Diagnosis": [extracted_text[0]]})

            df = pd.concat([df, new_entry], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False)

        print(f"Processed {len(image_files)} images from the folder successfully.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)

if __name__ == "__main__":
    main()
