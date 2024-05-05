# OpenAI Installation

## Installation Setup

- Installed on Ubuntu 22.04

## Original Documentation

- [NetworkChuck YouTube Video](https://www.youtube.com/watch?v=Wjrdr0NU4Sk)
- [Ollama Download](https://ollama.com/download/linux)
- [Ollama Models](https://ollama.com/library)
- [OpenWeb UI](https://docs.openwebui.com/getting-started/)

# NOTICE
This guide is not complete, please follow the NetworkChuck Video for best results.

## Installing Ollama

Install Ollama according to Ollama Documentation

## Installing Ollama Models

```
ollama pull MODEL-NAME
```

## Run Ollama in Command Line

```
ollama run MODEL-NAME
```

# OpenWeb UI Installation
## Install Docker

Install Docker and Docker Compose Plugin

## Run OpenWeb UI Docker

```
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name openweb-ui --restart unless-stopped ghcr.io/open-webui/open-webui:main
```

## Good Models to use
`codegemma`
`llama2`
`llava` # Generates Info based off Image

# Stable Diffusion Installation

```
apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
```

```
curl https://pyenv.run | bash
```

```
pyenv install 3.10
```

```
pyenv global 3.10
```

```
wget -q https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh
```

```
chmod +x webui.sh
```

```
./webui.sh --listen --api
```

