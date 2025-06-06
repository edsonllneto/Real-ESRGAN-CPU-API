# Models Directory

This directory should contain the Real-ESRGAN model files required for the API to function.

## Required Models

### 1. realesrgan-x4plus
- Best for: Real photos and general images
- Files needed:
  - `realesrgan-x4plus.param`
  - `realesrgan-x4plus.bin`

### 2. realesrgan-x4plus-anime
- Best for: Anime and illustrations
- Files needed:
  - `realesrgan-x4plus-anime.param`
  - `realesrgan-x4plus-anime.bin`

## Download Instructions

You can download the model files from the official Real-ESRGAN repository:

```bash
# Download realesrgan-x4plus
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O realesrgan-x4plus.pth
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -O realesrgan-x4plus-anime.pth

# Convert to ncnn format (requires conversion tools)
# Or download pre-converted ncnn models:
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
```

## Alternative Download Script

Create a `download_models.sh` script:

```bash
#!/bin/bash
cd models/

# Download Real-ESRGAN x4plus
echo "Downloading Real-ESRGAN x4plus model..."
wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
unzip -q realesrgan-ncnn-vulkan-20220424-ubuntu.zip
cp realesrgan-ncnn-vulkan-20220424-ubuntu/models/realesrgan-x4plus.param .
cp realesrgan-ncnn-vulkan-20220424-ubuntu/models/realesrgan-x4plus.bin .
cp realesrgan-ncnn-vulkan-20220424-ubuntu/models/realesrgan-x4plus-anime.param .
cp realesrgan-ncnn-vulkan-20220424-ubuntu/models/realesrgan-x4plus-anime.bin .

# Cleanup
rm -rf realesrgan-ncnn-vulkan-20220424-ubuntu realesrgan-ncnn-vulkan-20220424-ubuntu.zip

echo "Models downloaded successfully!"
```

## File Structure After Download

```
models/
├── README.md
├── realesrgan-x4plus.param
├── realesrgan-x4plus.bin
├── realesrgan-x4plus-anime.param
└── realesrgan-x4plus-anime.bin
```

## Notes

- Model files are not included in the repository due to their large size
- Total size: ~65MB for both models
- Models are loaded once and cached in memory for performance
- The API will fail to start if required model files are missing