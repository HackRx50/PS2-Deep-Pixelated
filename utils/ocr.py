import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from sklearn.preprocessing import binarize
from io import BytesIO

def read_image_from_bytes(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")

def process_vision_info(messages):
    image_inputs = []
    for message in messages:
        for content in message["content"]:
            if content["type"] == "image":
                # content["image"] is a PIL Image
                image_inputs.append(content["image"])
    return image_inputs, None


def thinning(image):
    kernel = np.ones((3, 3), np.uint8)  # Use a larger kernel
    eroded_img = cv2.erode(image, kernel, iterations=1)
    dilated_img = cv2.dilate(eroded_img, kernel, iterations=1)  # Dilation after thinning
    return dilated_img

def clean_image(image, scale_factor=2.5):
  
    height, width = image.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    image = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)  # Interpolation to enlarge

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    cleaned_image = thinning(gray_image)

    cleaned_image = Image.fromarray(cleaned_image)
    return cleaned_image


def extract_text_from_image(image_path):
    # image = Image.open(image_path)
    cleaned_image = clean_image(np.array(image_path))

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": cleaned_image},
                {"type": "text", "text": "Extract provisional diagnosis from the image, and correct any inappropriate word based on contextual understanding"},
            ],
        }
    ]

    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt")

    # inputs = inputs.to("cuda")  uncomment to run on gpu with cuda enabled
    
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    print(output_text)
    
    return output_text

