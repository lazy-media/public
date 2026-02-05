---
description: Information on how to setup a self hosted Ollama Instance
---

# Ollama Installation

### Sources

* [Ollama Website](https://ollama.com/download/linux)
* [Forum for Fix](https://github.com/ollama/ollama/issues/703)

## Prerequisites

* Fresh Install of Ubuntu 24.04 with OpenSSH installed

## Installation

### System Update & Upgrade

* SSH into your AI Server
* Make sure everything is up to date

```
sudo apt udpate && sudo apt upgrade -y
```

### Install Ollama

* Run the Following command:

```
curl -fsSL https://ollama.com/install.sh | sh
```

NOTE: If you have a NVIDIA Graphics Card installed into your AI Server, this script will install all the required files and set the GPU to default. You MUST restart after this script is installed if it needs to install NVIDIA Drivers.

### Ollama Accessible from Local Network

* SSH into your AI Server, if not already.
* Edit the File `/etc/systemd/system/ollama.service`

```
sudo nano /etc/systemd/system/ollama.service
```

Add the following line under the current `Environment` Variable

```
Environment="OLLAMA_HOST=0.0.0.0"
```

* Apply the new Daemon Setup

```
sudo systemctl daemon-reload
```

* Restart Ollama

```
sudo systemctl restart ollama
```
