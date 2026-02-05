---
description: Information on self hosted Faster Whisper Wyoming Protocol Installation
---

# Faster Whisper Wyoming Installation

## Documentation / References

* [Docker Hub](https://github.com/lazy-media/public/blob/main/Artificial-Intelligence/Faster-Whisper/README.md)

## Prerequisites

* Ubuntu Server 24.04
* Docker Installed
  * Need to install Docker? Visit [Docker Installation](https://github.com/lazy-media/public/blob/main/Artificial-Intelligence/Faster-Whisper/Installation-Instructions/Docker/README.md)
* (Optional) Interface for managing Docker Containers, such as Portainer

## Make Directory for Whisper

```
sudo mkdir wyoming-whisper
```

## Change to Directory

```
cd wyoming-whisper
```

## Docker Run Command

Be sure to change the path on the left side of the colon `:` to your appropriate path if needed.

```
docker run -it -p 10300:10300 -v ./data:/data rhasspy/wyoming-whisper \
    --model tiny-int8 --language en
```

## Success

You should now have Wyoming Faster Whisper Installed and running

## BONUS

If you already have NVIDIA Graphics installed, adding the following Environment Variables _should_ enable the use of your NVIDIA GPU, even though for me, it doesn't show using `nvidia-smi`.

```
-e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all
```

so your run command should look something like this:

```
docker run -it -p 10300:10300 -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all -v ./data:/data rhasspy/wyoming-whisper \
    --model tiny-int8 --language en
```
