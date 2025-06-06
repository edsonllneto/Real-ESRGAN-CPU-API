import base64
import time
import logging
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import uvicorn

from upscaler import RealESRGANUpscaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Real-ESRGAN CPU API",
    description="Image upscaling API using Real-ESRGAN optimized for CPU",
    version="1.0.0"
)

upscaler = RealESRGANUpscaler()

@app.on_event("startup")
async def startup_event():
    logger.info("Real-ESRGAN CPU API started")
    logger.info(f"Available models: {upscaler.get_available_models()}")

@app.get("/")
async def root():
    return {"message": "Real-ESRGAN CPU API", "models": upscaler.get_available_models()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": len(upscaler.get_available_models())}

def validate_image_size(image: Image.Image) -> None:
    """Validate image dimensions"""
    width, height = image.size
    if width > 2048 or height > 2048:
        raise HTTPException(
            status_code=400, 
            detail=f"Image too large. Maximum size is 2048x2048, got {width}x{height}"
        )

def validate_parameters(scale: int, model: str) -> None:
    """Validate upscaling parameters"""
    if scale not in [2, 4]:
        raise HTTPException(status_code=400, detail="Scale must be 2 or 4")
    
    available_models = upscaler.get_available_models()
    if model not in available_models:
        raise HTTPException(
            status_code=400, 
            detail=f"Model '{model}' not available. Available models: {available_models}"
        )

@app.post("/upscale/binary")
async def upscale_binary(
    file: UploadFile = File(...),
    scale: int = Form(4),
    model: str = Form("realesrgan-x4plus")
):
    """
    Upscale image from binary upload
    
    Args:
        file: Image file to upscale
        scale: Scale factor (2 or 4)
        model: Model to use ('realesrgan-x4plus' or 'realesrgan-x4plus-anime')
    
    Returns:
        JSON with base64 encoded upscaled image and metadata
    """
    start_time = time.time()
    
    try:
        # Validate parameters
        validate_parameters(scale, model)
        
        # Read and validate image
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        validate_image_size(image)
        
        original_size = image.size
        logger.info(f"Processing image: {original_size} -> scale {scale}x with {model}")
        
        # Upscale image
        upscaled_image = upscaler.upscale_image(image, model, scale)
        
        # Convert to base64
        output_buffer = BytesIO()
        upscaled_image.save(output_buffer, format='JPEG', quality=95)
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        processing_time = time.time() - start_time
        
        return JSONResponse({
            "success": True,
            "image": output_base64,
            "metadata": {
                "original_size": original_size,
                "upscaled_size": upscaled_image.size,
                "scale_factor": scale,
                "model_used": model,
                "processing_time_seconds": round(processing_time, 2)
            }
        })
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/upscale/base64")
async def upscale_base64(
    image_data: str = Form(...),
    scale: int = Form(4),
    model: str = Form("realesrgan-x4plus")
):
    """
    Upscale image from base64 encoded data
    
    Args:
        image_data: Base64 encoded image
        scale: Scale factor (2 or 4)
        model: Model to use ('realesrgan-x4plus' or 'realesrgan-x4plus-anime')
    
    Returns:
        JSON with base64 encoded upscaled image and metadata
    """
    start_time = time.time()
    
    try:
        # Validate parameters
        validate_parameters(scale, model)
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        validate_image_size(image)
        
        original_size = image.size
        logger.info(f"Processing base64 image: {original_size} -> scale {scale}x with {model}")
        
        # Upscale image
        upscaled_image = upscaler.upscale_image(image, model, scale)
        
        # Convert to base64
        output_buffer = BytesIO()
        upscaled_image.save(output_buffer, format='JPEG', quality=95)
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        processing_time = time.time() - start_time
        
        return JSONResponse({
            "success": True,
            "image": output_base64,
            "metadata": {
                "original_size": original_size,
                "upscaled_size": upscaled_image.size,
                "scale_factor": scale,
                "model_used": model,
                "processing_time_seconds": round(processing_time, 2)
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing base64 image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info"
    )