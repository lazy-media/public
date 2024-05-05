# OpenAI Installation

## Installation Setup

- Installed on Ubuntu 22.04

## Original Documentation

- [NetworkChuck YouTube Video](https://www.youtube.com/watch?v=Wjrdr0NU4Sk)
- [Ollama Download](https://ollama.com/download/linux)
- [OpenWeb UI]()

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