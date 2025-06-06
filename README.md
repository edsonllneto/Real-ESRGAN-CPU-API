# Real-ESRGAN CPU API

A high-performance REST API for AI image upscaling using Real-ESRGAN models, optimized for CPU-only environments. This project provides a simple, scalable solution for enhancing image resolution without requiring GPU hardware.

## 🚀 Features

- **Multiple AI Models**: Support for 4 Real-ESRGAN models with different specializations
- **CPU Optimized**: Efficient processing using PyTorch CPU backend with tile-based processing
- **RESTful API**: Clean FastAPI endpoints with comprehensive documentation
- **Multiple Input Formats**: Support for both binary file uploads and base64 JSON requests
- **Docker Ready**: Multi-stage Dockerfile for production deployment
- **Memory Efficient**: Optimized for low-resource environments with intelligent image preprocessing
- **Real-time Metadata**: Processing time, dimensions, and model information in responses

## 📋 Supported Models

| Model | Size | Best For | Performance |
|-------|------|----------|-------------|
| `realesr-general-x4v3` | 16MB | General purpose, production use | ⚡ Fastest |
| `realesr-general-wdn-x4v3` | 16MB | Images with noise (includes denoising) | ⚡ Fast |
| `realesrgan-x4plus-anime` | 18MB | Anime and illustrations | 🎨 Specialized |
| `realesrgan-x4plus` | 67MB | High-quality real photos | 📸 Premium |

## 🏗️ Architecture

```
real-esrgan-cpu-api/
├── main.py              # FastAPI application with endpoints
├── upscaler.py          # Real-ESRGAN wrapper with singleton pattern
├── models/              # Pre-included AI models
├── requirements.txt     # Python dependencies
├── Dockerfile           # Multi-stage container build
├── docker-compose.yml   # Production deployment
└── README.md           # Documentation
```

## 🔧 Installation & Usage

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd real-esrgan-cpu-api

# Build and run with Docker Compose
docker-compose up --build

# API available at http://localhost:8000
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# API available at http://localhost:8000
```

## 📡 API Endpoints

### Binary Upload
```bash
curl -X POST "http://localhost:8000/upscale/binary" \
  -F "file=@image.jpg" \
  -F "model=realesr-general-x4v3" \
  -F "scale=4"
```

### Base64 JSON
```bash
curl -X POST "http://localhost:8000/upscale/base64" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "base64_encoded_image_here",
    "model": "realesr-general-x4v3",
    "scale": 4
  }'
```

### Available Models
```bash
curl http://localhost:8000/models
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 📊 Performance

- **Processing Time**: 2-8 seconds for 1024x1024 images
- **Memory Usage**: ~1-2GB RAM depending on model
- **Max Input Size**: 2048x2048 pixels
- **Automatic Optimization**: Images >1024px are pre-resized for faster processing
- **Tile Processing**: 400px tiles for memory efficiency

## 🔨 Technical Details

### Stack
- **Framework**: FastAPI + Uvicorn
- **AI Engine**: Real-ESRGAN v0.3.0
- **Image Processing**: Pillow + NumPy
- **ML Backend**: PyTorch CPU
- **Container**: Multi-stage Docker with Debian slim

### Optimizations
- **Singleton Pattern**: Models loaded once and cached in memory
- **Tile-based Processing**: Memory-efficient processing for large images
- **CPU Threading**: Multi-worker setup for concurrent requests
- **Image Preprocessing**: Smart resizing and format conversion
- **Response Caching**: Optimized for repeated requests

## 📖 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔍 Example Responses

### Successful Processing
```json
{
  "success": true,
  "processing_time": 3.45,
  "input_dimensions": [512, 512],
  "output_dimensions": [2048, 2048],
  "model_used": "realesr-general-x4v3",
  "scale_factor": 4
}
```

### Error Response
```json
{
  "detail": "Input image too large. Maximum size: 2048x2048"
}
```

## 🔧 Configuration

### Environment Variables
- `PYTHONUNBUFFERED=1`: For proper logging in containers
- `ANTHROPIC_MODEL`: Model configuration (if using external model management)

### Docker Resources
- **Memory Limit**: 2GB (configurable in docker-compose.yml)
- **CPU Cores**: 2-4 recommended
- **Storage**: 2GB+ for container and models

## 🤝 Credits & Acknowledgments

This project builds upon the excellent work of several open-source projects and researchers:

### Core AI Technology
- **Real-ESRGAN**: [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
  - *Xintao Wang, Liangbin Xie, Chao Dong, Ying Shan*
  - "Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data"

### Framework & Libraries
- **FastAPI**: [tiangolo/fastapi](https://github.com/tiangolo/fastapi) - Modern web framework
- **PyTorch**: [pytorch/pytorch](https://github.com/pytorch/pytorch) - ML framework
- **Pillow**: [python-pillow/Pillow](https://github.com/python-pillow/Pillow) - Image processing
- **Uvicorn**: [encode/uvicorn](https://github.com/encode/uvicorn) - ASGI server

### Development Tools
- **Claude Code**: AI-assisted development and optimization
- **Docker**: Containerization and deployment

## 📄 License

This project is open source and available under the MIT License. Please note that the Real-ESRGAN models may have their own licensing terms.

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the API documentation at `/docs`
2. Verify model files are properly loaded
3. Check Docker container logs
4. Open an issue in the repository

## 🔮 Roadmap

- [ ] Support for additional Real-ESRGAN models
- [ ] Batch processing endpoints
- [ ] Async processing with job queues
- [ ] Model auto-downloading
- [ ] Custom tile size configuration
- [ ] WebSocket support for real-time updates

---

**Built with ❤️ for the AI community**