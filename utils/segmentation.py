import cv2
from paddleocr import PaddleOCR
import torch
import time
import numpy as np
import difflib
from PIL import Image


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ocr_device = 'gpu' if torch.cuda.is_available() else 'cpu'
ocr = PaddleOCR(use_angle_cls=True, lang='en', device=ocr_device)



def crop_provisional_diagnosis(img, result):
    target_text = "provisional diagnosis"

    for line in result:
        for word_info in line:
            text = word_info[1][0].lower()

            
            similarity = difflib.SequenceMatcher(None, text, target_text).ratio() * 100

            if similarity >= 90:  # Accepting similarity of 90% and above
                bbox = word_info[0]
                x_min = int(min([point[0] for point in bbox])) + 100
                y_min = int(min([point[1] for point in bbox])) - 20
                x_max = int(max([point[0] for point in bbox])) + 1000
                y_max = int(max([point[1] for point in bbox])) + 30

                cropped_img = img[y_min:y_max, x_min:x_max]
                return cropped_img
    return None

def extract_provisional_diagnosis(image_bytes):
    start_time = time.time()
  
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    if isinstance(img, Image.Image):  
        img = np.array(img)  

    result = ocr.ocr(img, cls=True)
    cropped_img = crop_provisional_diagnosis(img, result)
    print(result)
    elapsed_time = time.time() - start_time
    print(f"Time taken for extract_provisional_diagnosis: {elapsed_time:.2f} seconds")
    return cropped_img