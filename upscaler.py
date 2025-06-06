import os
import numpy as np
from PIL import Image
from realesrgan import RealESRGAN
import threading
from typing import Optional


class RealESRGANUpscaler:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.models = {}
            self.initialized = True
    
    def get_model(self, model_name: str) -> RealESRGAN:
        if model_name not in self.models:
            with self._lock:
                if model_name not in self.models:
                    model_path = f"models/{model_name}"
                    if not os.path.exists(f"{model_path}.param"):
                        raise FileNotFoundError(f"Model {model_name} not found in models directory")
                    
                    self.models[model_name] = RealESRGAN(
                        scale=4 if "x4" in model_name else 2,
                        model_path=model_path,
                        tile=400,
                        tile_pad=10,
                        pre_pad=0,
                        half=False,
                        gpu_id=None
                    )
        
        return self.models[model_name]
    
    def upscale_image(self, image: Image.Image, model_name: str, scale: int = 4) -> Image.Image:
        if image.width > 2048 or image.height > 2048:
            raise ValueError("Input image too large. Maximum size: 2048x2048")
        
        if image.width > 1024 or image.height > 1024:
            ratio = min(1024 / image.width, 1024 / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        model = self.get_model(model_name)
        
        img_array = np.array(image)
        result_array = model.enhance(img_array, outscale=scale)
        
        return Image.fromarray(result_array)
    
    @staticmethod
    def get_available_models():
        return ["realesrgan-x4plus", "realesrgan-x4plus-anime"]
    
    @staticmethod
    def validate_model(model_name: str) -> bool:
        return model_name in RealESRGANUpscaler.get_available_models()
    
    @staticmethod
    def validate_scale(scale: int) -> bool:
        return scale in [2, 4]