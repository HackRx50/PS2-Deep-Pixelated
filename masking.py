from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFilter
import os
import shutil

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # You can adjust the language as needed

def blur_section(image, coordinates):
    """
    Blurs a section of the image based on the given coordinates.
    :param image: PIL Image object.
    :param coordinates: Coordinates of the section to blur (x_min, y_min, x_max, y_max).
    """
    x_min, y_min, x_max, y_max = coordinates
    section = image.crop((x_min, y_min, x_max, y_max))
    blurred_section = section.filter(ImageFilter.GaussianBlur(radius=10))
    image.paste(blurred_section, (x_min, y_min, x_max, y_max))
    return image

def crop_and_blur_details(img, ocr_results):
    """
    Detects 'name', 'phone', 'email' in the OCR results, crops their bounding box, and blurs them.
    :param img: PIL Image object.
    :param ocr_results: OCR result from PaddleOCR.
    :return: PIL Image object with blurred sections.
    """
    keywords = ["name", "phone", "email"]
    
    for line in ocr_results:
        for word_info in line:
            text = word_info[1][0].lower()

            # Check if the text contains any keyword
            if any(keyword in text for keyword in keywords):
                bbox = word_info[0]
                
                # Get the bounding box for blurring
                x_min = int(min([point[0] for point in bbox]))
                y_min = int(min([point[1] for point in bbox]))
                x_max = int(max([point[0] for point in bbox])) + 1000
                y_max = int(max([point[1] for point in bbox]))
                # Blur the section in the image
                img = blur_section(img, (x_min, y_min, x_max, y_max))

    return img


def detect_and_blur_details(image_path):
    """
    Detects personal details like name, email, and phone number, and blurs them in the image.
    :param image_path: Path to the image file.
    :return: Path to the updated image file with blurred details.
    """
    # Run OCR on the image
    ocr_results = ocr.ocr(image_path)

    # Open the image with PIL
    img = Image.open(image_path)

    # Crop and blur sections containing sensitive details
    blurred_img = crop_and_blur_details(img, ocr_results)

    # Save the modified image
    blurred_image_path = image_path.replace(".jpg", "_blurred.jpg")
    blurred_img.save(blurred_image_path)

    return blurred_image_path
