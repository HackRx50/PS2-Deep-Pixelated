import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from sklearn.preprocessing import binarize


# Load the model on the available device(s)
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")

def thinning(image):
    kernel = np.ones((3, 3), np.uint8)  # Use a larger kernel
    eroded_img = cv2.erode(image, kernel, iterations=1)
    dilated_img = cv2.dilate(eroded_img, kernel, iterations=1)  # Dilation after thinning
    return dilated_img

def clean_image(image, scale_factor=2.5):
    # Resize the image
    height, width = image.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    image = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)  # Interpolation to enlarge

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply the thinning process
    cleaned_image = thinning(gray_image)

    # Convert back to PIL Image
    cleaned_image = Image.fromarray(cleaned_image)
    return cleaned_image


def extract_text_from_image(image_path):
    # Prepare the messages input
    image = Image.open(image_path)
    cleaned_image = clean_image(np.array(image))

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": cleaned_image},
                {"type": "text", "text": "Extract provisional diagnosis from the image, and correct any inappropriate word based on contextual understanding"},
            ],
        }
    ]

    # Preparation for inference
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt")

    # inputs = inputs.to("cuda") 
    
    # Inference: Generate the output
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    print(output_text)

    # diagnosis_prefix = "is:"
    # diagnosis = None

    # if diagnosis_prefix in output_text:
    #     start_idx = output_text.index(diagnosis_prefix) + len(diagnosis_prefix)
    #     end_idx = output_text.find(".", start_idx)  # Find the first full stop after "is:"

    #     if end_idx == -1:  # No full stop found, extract till the end
    #         diagnosis = output_text[start_idx:].strip()
    #     else:
    #         diagnosis = output_text[start_idx:end_idx].strip()

    # return diagnosis if diagnosis else "Diagnosis not found in the extracted text."
    
    

    return output_text

