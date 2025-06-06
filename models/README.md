# Models Directory

This directory should contain the Real-ESRGAN model files required for the API to function.

## Required Models

### 1. realesrgan-x4plus
- Best for: Real photos and general images
- Size: ~67MB
- Files needed: `realesrgan-x4plus.pth`

### 2. realesrgan-x4plus-anime
- Best for: Anime and illustrations  
- Size: ~18MB
- Files needed: `realesrgan-x4plus-anime.pth`

### 3. realesr-general-x4v3 (NEW)
- Best for: Fast general purpose upscaling
- Size: ~16MB (smaller and faster)
- Files needed: `realesr-general-x4v3.pth`

### 4. realesr-general-wdn-x4v3 (NEW)
- Best for: Images with noise (includes denoising)
- Size: ~16MB
- Files needed: `realesr-general-wdn-x4v3.pth`

## Download Instructions

You can download the model files from the official Real-ESRGAN repository:

```bash
# Download original models
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O realesrgan-x4plus.pth
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -O realesrgan-x4plus-anime.pth

# Download new v3 models (smaller and faster)
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth -O realesr-general-x4v3.pth
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth -O realesr-general-wdn-x4v3.pth
```

## Alternative Download Script

Create a `download_models.sh` script:

```bash
#!/bin/bash
cd models/

echo "Downloading Real-ESRGAN models..."

# Original models
echo "Downloading original models..."
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O realesrgan-x4plus.pth
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -O realesrgan-x4plus-anime.pth

# New v3 models (smaller and faster)
echo "Downloading v3 models (smaller and faster)..."
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth -O realesr-general-x4v3.pth
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth -O realesr-general-wdn-x4v3.pth

echo "All models downloaded successfully!"
```

## File Structure After Download

```
models/
├── README.md
├── realesrgan-x4plus.pth          (67MB - photos)
├── realesrgan-x4plus-anime.pth    (18MB - anime)
├── realesr-general-x4v3.pth       (16MB - fast general)
└── realesr-general-wdn-x4v3.pth   (16MB - with denoising)
```

## Notes

- Model files are not included in the repository due to their large size
- Total size: ~117MB for all 4 models
- Models are loaded once and cached in memory for performance
- The API will fail to start if required model files are missing