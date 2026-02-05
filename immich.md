---
description: Information on how to setup Immich; A self hosted Google Photos alternative.
---

# Immich

## Immich Installation

### Original Documentation / Website

> [Immich Website](https://immich.app/)

### Docker Compose Installation with Persistant Storage for all Volumes

#### Installation Requirements / Setup

* Installed in a Proxmox LXC
* Installed on Ubuntu 22.04
* Installed Docker Compose

#### Assumptions

* Basic understanding of Docker and Docker Compose

## Docker Compose File

> [Example Docker Compose File](https://github.com/lazy-media/public/blob/main/Immich/docker-compose.yml)

### Example Docker Compose Env File

> [Example Docker Compose ENV File](https://github.com/lazy-media/public/blob/main/Immich/.env/README.md)

## Immich Hardware Acceleration Files

> [Example `hwaccel.ml.yml`](https://github.com/lazy-media/public/blob/main/Immich/hwaccel.ml.yml)

> [Example `hwaccel.transcoding.yml`](https://github.com/lazy-media/public/blob/main/Immich/hwaccel.transcoding.yml)

## Start and Run Immich

Run the following command

```
docker compose pull && docker compose up -d
```

## Updating Immich

Run

```
docker compose down && docker compose pull && docker compose up -d
```

## Immich OAuth / OpenID Setup

[Immich OAuth / OpenID Setup](https://github.com/lazy-media/public/blob/main/Authentik/Immich/README.md)

## Google Photo Takeout Conversion Helpers

Use either of these scripts to convert your Google Photos Takeout to Immich compatible format.

[Google Photo Takeout Helpers](https://github.com/lazy-media/public/blob/main/Google-Photos-Takeout/README.md)
