# Models Directory

This directory should contain the Real-ESRGAN model files required for the API to function.

## Required Models

### 1. realesrgan-x4plus
- Best for: Real photos and general images
- Files needed:
  - `realesrgan-x4plus.pth`

### 2. realesrgan-x4plus-anime
- Best for: Anime and illustrations
- Files needed:
  - `realesrgan-x4plus-anime.pth`

## Download Instructions

You can download the model files from the official Real-ESRGAN repository:

```bash
# Download realesrgan-x4plus models
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O realesrgan-x4plus.pth
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -O realesrgan-x4plus-anime.pth
```

## Alternative Download Script

Create a `download_models.sh` script:

```bash
#!/bin/bash
cd models/

# Download Real-ESRGAN models
echo "Downloading Real-ESRGAN models..."
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O realesrgan-x4plus.pth
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -O realesrgan-x4plus-anime.pth

echo "Models downloaded successfully!"
```

## File Structure After Download

```
models/
├── README.md
├── realesrgan-x4plus.pth
└── realesrgan-x4plus-anime.pth
```

## Notes

- Model files are not included in the repository due to their large size
- Total size: ~130MB for both models
- Models are loaded once and cached in memory for performance
- The API will fail to start if required model files are missing