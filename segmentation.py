import cv2
from paddleocr import PaddleOCR

def crop_provisional_diagnosis(img, ocr_results):
    for line in ocr_results:
        for word_info in line:
            text = word_info[1][0].lower()
            if "provisional diagnosis" in text:
                bbox = word_info[0]
                x_min = int(min([point[0] for point in bbox])) + 100
                y_min = int(min([point[1] for point in bbox])) - 20
                x_max = int(max([point[0] for point in bbox])) + 1000
                y_max = int(max([point[1] for point in bbox])) + 30

                cropped_img = img[y_min:y_max, x_min:x_max]
                return cropped_img
    return None

def extract_provisional_diagnosis(image_path, save_path):
    img = cv2.imread(image_path)
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path, cls=True)
    cropped_img = crop_provisional_diagnosis(img, result)
    if cropped_img is not None:
        cv2.imwrite(save_path, cropped_img)
        return save_path
    else:
        return None
