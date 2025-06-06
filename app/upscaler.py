import os
import numpy as np
from PIL import Image
from realesrgan_ncnn_py import RealESRGAN
import threading
import logging

logger = logging.getLogger(__name__)

class RealESRGANUpscaler:
    _instance = None
    _lock = threading.Lock()
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._load_models()
    
    def _load_models(self):
        """Load Real-ESRGAN models into memory"""
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        
        # RealESRGAN_x4plus for photos
        try:
            self._models['realesrgan-x4plus'] = RealESRGAN(
                model_name='RealESRGAN_x4plus',
                scale=4,
                tile_size=400,
                pre_pad=10,
                half=False,
                device='cpu'
            )
            logger.info("Loaded RealESRGAN_x4plus model")
        except Exception as e:
            logger.error(f"Failed to load RealESRGAN_x4plus: {e}")
        
        # RealESRGAN_x4plus_anime for illustrations
        try:
            self._models['realesrgan-x4plus-anime'] = RealESRGAN(
                model_name='RealESRGAN_x4plus_anime_6B',
                scale=4,
                tile_size=400,
                pre_pad=10,
                half=False,
                device='cpu'
            )
            logger.info("Loaded RealESRGAN_x4plus_anime model")
        except Exception as e:
            logger.error(f"Failed to load RealESRGAN_x4plus_anime: {e}")
    
    def upscale_image(self, image: Image.Image, model_name: str = 'realesrgan-x4plus', scale: int = 4) -> Image.Image:
        """
        Upscale image using specified model
        
        Args:
            image: PIL Image to upscale
            model_name: Model to use ('realesrgan-x4plus' or 'realesrgan-x4plus-anime')
            scale: Scale factor (2 or 4)
        
        Returns:
            Upscaled PIL Image
        """
        if model_name not in self._models:
            raise ValueError(f"Model {model_name} not available")
        
        # Convert PIL to numpy array
        input_array = np.array(image)
        
        # Pre-resize if input is too large
        height, width = input_array.shape[:2]
        if max(height, width) > 1024:
            ratio = 1024 / max(height, width)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            input_array = np.array(image)
        
        # Handle scale factor
        model = self._models[model_name]
        if scale == 2 and model.scale == 4:
            # Upscale to 4x then downscale to 2x
            output_array = model.process(input_array)
            output_image = Image.fromarray(output_array)
            original_height, original_width = input_array.shape[:2]
            target_width = original_width * 2
            target_height = original_height * 2
            output_image = output_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            # Direct upscaling
            output_array = model.process(input_array)
            output_image = Image.fromarray(output_array)
        
        return output_image
    
    def get_available_models(self):
        """Get list of available models"""
        return list(self._models.keys())