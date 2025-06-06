# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-ESRGAN CPU API is an image upscaling service optimized for CPU-only VPS environments. It provides HTTP endpoints for upscaling images using Real-ESRGAN models with ncnn backend for better CPU performance.

## Architecture

**Core Components:**
- `app/main.py`: FastAPI application with two endpoints (`/upscale/binary`, `/upscale/base64`)
- `app/upscaler.py`: Singleton wrapper for Real-ESRGAN models with memory management
- `app/models/`: Directory for .pth model files (auto-downloaded in Docker build)

**Key Design Patterns:**
- Singleton pattern for model loading (loaded once, cached in memory)
- Tile-based processing (400px tiles) for memory efficiency
- Pre-resize logic for inputs > 1024px to prevent memory issues
- Multi-worker Uvicorn setup (4 workers) for concurrent processing

## Development Commands

**Local Development:**
```bash
cd app
pip install -r requirements.txt
python main.py
```

**Docker Build:**
```bash
docker build -t realesrgan-cpu-api .
docker run -p 8000:8000 realesrgan-cpu-api
```

**API Testing:**
```bash
curl -X POST "http://localhost:8000/upscale/binary" \
  -F "file=@image.jpg" \
  -F "scale=4" \
  -F "model=realesrgan-x4plus"
```

## Configuration

**Models Available:**
- `realesrgan-x4plus`: For real photos (general purpose)
- `realesrgan-x4plus-anime`: For anime/illustrations

**Constraints:**
- Max input size: 2048x2048
- Scale factors: 2x or 4x
- Tile size: 400px (optimized for CPU/RAM usage)
- Expected processing time: 2-8 seconds for 1024x1024 images

## Performance Optimizations

- ncnn backend instead of PyTorch for better CPU performance
- Models loaded once at startup and cached
- Automatic pre-resizing for large inputs
- Alpine-based Docker image for smaller footprint
- 4 Uvicorn workers for concurrent request handling