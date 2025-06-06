import io
import base64
import time
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import Response
from PIL import Image
from upscaler import RealESRGANUpscaler
from pydantic import BaseModel


app = FastAPI(
    title="Real-ESRGAN CPU API",
    description="AI Image Upscaling API using Real-ESRGAN optimized for CPU",
    version="1.0.0"
)

upscaler = RealESRGANUpscaler()


class UpscaleResponse(BaseModel):
    success: bool
    processing_time: float
    input_dimensions: tuple[int, int]
    output_dimensions: tuple[int, int]
    model_used: str
    scale_factor: int


class Base64UpscaleRequest(BaseModel):
    image_data: str
    model: str = "realesrgan-x4plus"
    scale: int = 4


class Base64UpscaleResponse(BaseModel):
    success: bool
    image_data: str
    processing_time: float
    input_dimensions: tuple[int, int]
    output_dimensions: tuple[int, int]
    model_used: str
    scale_factor: int


@app.get("/")
async def root():
    return {
        "message": "Real-ESRGAN CPU API",
        "available_models": upscaler.get_available_models(),
        "supported_scales": [2, 4],
        "max_input_size": "2048x2048"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/upscale/binary", response_model=UpscaleResponse)
async def upscale_binary(
    file: UploadFile = File(...),
    model: str = Form("realesrgan-x4plus"),
    scale: int = Form(4)
):
    start_time = time.time()
    
    if not upscaler.validate_model(model):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model. Available models: {upscaler.get_available_models()}"
        )
    
    if not upscaler.validate_scale(scale):
        raise HTTPException(
            status_code=400,
            detail="Invalid scale. Supported scales: 2, 4"
        )
    
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        input_dimensions = (image.width, image.height)
        
        upscaled_image = upscaler.upscale_image(image, model, scale)
        
        output_dimensions = (upscaled_image.width, upscaled_image.height)
        
        img_buffer = io.BytesIO()
        upscaled_image.save(img_buffer, format='PNG', optimize=True)
        img_buffer.seek(0)
        
        processing_time = time.time() - start_time
        
        response = Response(
            content=img_buffer.getvalue(),
            media_type="image/png",
            headers={
                "X-Processing-Time": str(processing_time),
                "X-Input-Dimensions": f"{input_dimensions[0]}x{input_dimensions[1]}",
                "X-Output-Dimensions": f"{output_dimensions[0]}x{output_dimensions[1]}",
                "X-Model-Used": model,
                "X-Scale-Factor": str(scale)
            }
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/upscale/base64", response_model=Base64UpscaleResponse)
async def upscale_base64(request: Base64UpscaleRequest):
    start_time = time.time()
    
    if not upscaler.validate_model(request.model):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model. Available models: {upscaler.get_available_models()}"
        )
    
    if not upscaler.validate_scale(request.scale):
        raise HTTPException(
            status_code=400,
            detail="Invalid scale. Supported scales: 2, 4"
        )
    
    try:
        image_data = base64.b64decode(request.image_data)
        image = Image.open(io.BytesIO(image_data))
        
        input_dimensions = (image.width, image.height)
        
        upscaled_image = upscaler.upscale_image(image, request.model, request.scale)
        
        output_dimensions = (upscaled_image.width, upscaled_image.height)
        
        img_buffer = io.BytesIO()
        upscaled_image.save(img_buffer, format='PNG', optimize=True)
        img_buffer.seek(0)
        
        output_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        processing_time = time.time() - start_time
        
        return Base64UpscaleResponse(
            success=True,
            image_data=output_base64,
            processing_time=processing_time,
            input_dimensions=input_dimensions,
            output_dimensions=output_dimensions,
            model_used=request.model,
            scale_factor=request.scale
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/models")
async def get_models():
    return {
        "available_models": upscaler.get_available_models(),
        "model_descriptions": {
            "realesrgan-x4plus": "Best for real photos and general images",
            "realesrgan-x4plus-anime": "Optimized for anime and illustrations"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)