# 🐍 n8n Enhanced with Python Toolkit

This Docker image extends the official [n8n](https://n8n.io) workflow automation platform with a comprehensive Python environment for advanced data processing, AI integration, and multimedia operations.

## 🌟 Key Features

- **Pre-loaded Python Ecosystem**: Ready-to-use Python 3 with essential data science packages
- **Multimedia Processing**: FFmpeg, OpenCV, and audio processing libraries
- **AI Integration**: Hugging Face Hub and Gradio client pre-installed
- **Optimized Size**: Build tools removed after installation for smaller footprint
- **Security Conscious**: Runs as non-root `node` user by default

## 🛠️ Included Tools

### 📊 Data Processing
- Pandas, NumPy, Requests, BeautifulSoup4

### 🎥 Multimedia
- FFmpeg, yt-dlp, OpenCV, Pillow

### 🤖 AI/ML
- HuggingFace Hub, Gradio Client

### 🎧 Audio
- Soundfile, Audioread, PortAudio

## 🚀 Deployment Guide

<details>
<summary><strong>📋 Prerequisites</strong></summary>

- [ ] Docker Engine 20.10+
- [ ] Minimum 2GB RAM allocated to Docker
- [ ] 1vCPU minimum (2+ recommended for AI workflows)
</details>

### 🐳 Running the Container

<details>
<summary><strong>Basic Execution</strong></summary>

```bash
docker run -d \
  --name n8n-enhanced \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  ghcr.io/your-username/n8n-python:latest
```

</details><details> <summary><strong>Production Deployment</strong></summary>

```bash
docker run -d \
  --name n8n-production \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=securepassword \
  -v n8n_data:/home/node/.n8n \
  -v /etc/localtime:/etc/localtime:ro \
  --restart unless-stopped \
  --memory 2g \
  --cpus 1.5 \
  ghcr.io/your-username/n8n-python:latest
```

</details>

## 🔧 Customization Options

<details>
<summary><strong>Environment Variables</strong></summary>

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_PORT` | Web UI port | 5678 |
| `N8N_BASIC_AUTH_ACTIVE` | Enable basic auth | false |
| `PYTHON_UNBUFFERED` | Python output settings | 1 |
| `TZ` | Timezone | UTC |
</details>

<details>
<summary><strong>Volume Mounts</strong></summary>

- `/home/node/.n8n`: n8n configuration and workflows
- `/home/node/app`: Custom node scripts
- `/tmp`: Temporary processing files
</details>

## 🏗️ Build Process
<details> <summary><strong>Local Image Building</strong></summary>

1. Clone the repository
2. Navigate to Dockerfile directory
3. Execute build command:

```bash
docker build -t n8n-custom:latest \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') .
```

4. Verify Image:

```bash
docker inspect n8n-custom:latest
```

</details>

## � Security Considerations
<details> <summary><strong>Hardening Measures</strong></summary>

- Non-root execution context
- Build-time toolchain removed
- Alpine Linux base for smaller attack surface
- Regular base image updates
- Virtual environment isolation

### Recommendations:

- Use secrets management for credentials
- Enable HTTPS reverse proxy
- Restrict network access

</details>

## 🐞 Debugging Tips

<details> <summary><strong>Troubleshooting Guide</strong></summary>

### Python Packages Not Found

```bash
docker exec -it n8n-enhanced /home/node/.n8nvenv/bin/pip list
```

### Missing Dependencies

```bash
docker exec -u root -it n8n-enhanced apk info
```

### FFmpeg Verification

```bash
docker exec -it n8n-enhanced ffmpeg -version
```

</details>

## 📈 Performance Notes

 - Initial Load: 2-3 seconds slower than vanilla n8n due to Python env
 - Memory Usage: ~200MB overhead for Python runtime
 - Cold Start: AI workflows may have 5-10s delay on first run

## 🤝 Contributing

To add additional Python packages:

 1. Edit the pip install section in Dockerfile
 2. Document new dependencies in this README
 3. Submit a pull request

## 📜 License

Same as upstream n8n (Fair-code License) with additional Python package licenses applying to their respective components.