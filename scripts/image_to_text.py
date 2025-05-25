# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 21:38:18 2025

@author: aleks
"""

import cv2
import glob
import numpy
import os


from transformers import pipeline
from diffusers import DiffusionPipeline
from PIL import Image


class image_to_text:

    def __init__(self, image_folder_path: str, model_path: str, new_folder_path: str):
        self.image_folder_path = image_folder_path
        self.model_path = model_path
        self.new_folder_path = new_folder_path

    
    def read_image_from_folder(self) -> list[tuple[str, numpy.array]]:
        images: list[tuple[str, numpy.array]]=[]
        for filename in glob.glob(self.image_folder_path):
            try:
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"Skipping non-image file: {filename}")
                    continue
                # Load the image using Pillow
                img = Image.open(filename).convert("RGB")
                images.append((filename, img))
            except Exception as e:
                print(f"Failed to load image {filename}: {e}")
        
        return images
    
    def create_text_from_image(self):
       # os.makedirs(self.new_folder_path, exist_ok=True)
        image_to_text = pipeline("image-to-text", model=self.model_path)
        #image_to_text = DiffusionPipeline.from_pretrained("zenless-lab/sdxl-aam-xl-anime-mix")
        for filename, _ in self.read_image_from_folder():
            result = image_to_text(filename, max_new_tokens=50)
            generated_text = result[0]['generated_text']
            print(f"Generated text for {filename}: {generated_text}")
            # Save the generated text to a file
            base_filename = os.path.basename(filename)
            text_filename = os.path.splitext(base_filename)[0] + ".txt"
            text_file_path = os.path.join(self.new_folder_path, text_filename)
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(generated_text)
            


image = image_to_text('T_Naoko_Face/*','Salesforce/blip-image-captioning-large', 'T_Naoko_Face')
list_of_image = image.read_image_from_folder()
image.create_text_from_image()
