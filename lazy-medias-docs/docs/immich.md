---
description: Information on how to setup Immich; A self hosted Google Photos alternative.
---

# Immich

### Overview

Immich is a self-hosted Google Photos alternative. This page provides a Docker Compose-based setup with persistent storage, plus optional hardware acceleration files.

### Official site / docs

> [Immich Website](https://immich.app/)

{% hint style="info" %}
This page assumes you already have Docker + Docker Compose installed and working.
{% endhint %}

### Environment used (example)

* Installed in a Proxmox LXC
* Installed on Ubuntu 22.04
* Installed Docker Compose

### Assumptions

* Basic understanding of Docker and Docker Compose

***

### 1) Create the required files

You’ll create:

* `docker-compose.yml` (Immich stack)
* `.env` (stack configuration)

#### Docker Compose file

{% code expandable="true" %}
```yml
#
# WARNING: Make sure to use the docker-compose.yml of the current release:
#
# https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
#
# The compose file on main may not be compatible with the latest release.
#

name: immich

services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    # extends:
    #   file: hwaccel.transcoding.yml
    #   service: cpu # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    volumes:
      # Do not edit the next line. If you want to change the media storage location on your system, edit the value of UPLOAD_LOCATION in the .env file
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    ports:
      - '2283:2283'
    depends_on:
      - redis
      - database
    restart: always
    healthcheck:
      disable: false

  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, openvino] to the image tag.
    # Example tag: ${IMMICH_VERSION:-release}-cuda
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    # extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/ml-hardware-acceleration
    #   file: hwaccel.ml.yml
    #   service: cpu # set to one of [armnn, cuda, openvino, openvino-wsl] for accelerated inference - use the `-wsl` version for WSL2 where applicable
    volumes:
      - model-cache:/cache
    env_file:
      - .env
    restart: always
    healthcheck:
      disable: false

  redis:
    container_name: immich_redis
    image: docker.io/redis:6.2-alpine@sha256:2ba50e1ac3a0ea17b736ce9db2b0a9f6f8b85d4c27d5f5accc6a416d8f42c6d5
    healthcheck:
      test: redis-cli ping || exit 1
    restart: always

  database:
    container_name: immich_postgres
    image: docker.io/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:90724186f0a3517cf6914295b5ab410db9ce23190a2d9d0b9dd6463e3fa298f0
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
      POSTGRES_INITDB_ARGS: '--data-checksums'
    volumes:
      # Do not edit the next line. If you want to change the database storage location on your system, edit the value of DB_DATA_LOCATION in the .env file
      - ${DB_DATA_LOCATION}:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready --dbname='${DB_DATABASE_NAME}' --username='${DB_USERNAME}' || exit 1; Chksum="$$(psql --dbname='${DB_DATABASE_NAME}' --username='${DB_USERNAME}' --tuples-only --no-align --command='SELECT COALESCE(SUM(checksum_failures), 0) FROM pg_stat_database')"; echo "checksum failure count is $$Chksum"; [ "$$Chksum" = '0' ] || exit 1
      interval: 5m
      start_interval: 30s
      start_period: 5m
    command:
      [
        'postgres',
        '-c',
        'shared_preload_libraries=vectors.so',
        '-c',
        'search_path="$$user", public, vectors',
        '-c',
        'logging_collector=on',
        '-c',
        'max_wal_size=2GB',
        '-c',
        'shared_buffers=512MB',
        '-c',
        'wal_compression=on',
      ]
    restart: always

volumes:
  model-cache:

```
{% endcode %}

#### Example `.env` file

{% code expandable="true" %}
```dotenv
# You can find documentation for all the supported env variables at https://immich.app/docs/install/environment-variables

# The location where your uploaded files are stored
UPLOAD_LOCATION=./library

# The Immich version to use. You can pin this to a specific version like "v1.71.0"
IMMICH_VERSION=release

# Connection secret for postgres. You should change it to a random password
DB_PASSWORD=SOME RANDOM PASSWORD

# The values below this line do not need to be changed
###################################################################################
DB_HOSTNAME=immich_postgres
DB_USERNAME=postgres
DB_DATABASE_NAME=immich
DB_DATA_LOCATION=./pgdata

REDIS_HOSTNAME=immich_redis
```
{% endcode %}

***

### 2) Optional: hardware acceleration files

Only use these if you plan to enable hardware acceleration. Keep them next to your `docker-compose.yml` if you plan to reference them with `extends`.

{% tabs %}
{% tab title="hwaccel.ml.yml" %}
{% code expandable="true" %}
````yml
```
version: "3.8"

# Configurations for hardware-accelerated machine learning

# If using Unraid or another platform that doesn't allow multiple Compose files,
# you can inline the config for a backend by copying its contents 
# into the immich-machine-learning service in the docker-compose.yml file.

# See https://immich.app/docs/features/ml-hardware-acceleration for info on usage.

services:
  armnn:
    devices:
      - /dev/mali0:/dev/mali0
    volumes:
      - /lib/firmware/mali_csffw.bin:/lib/firmware/mali_csffw.bin:ro # Mali firmware for your chipset (not always required depending on the driver)
      - /usr/lib/libmali.so:/usr/lib/libmali.so:ro # Mali driver for your chipset (always required)

  cpu: {}

  cuda:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities:
                - gpu
                - compute
                - video

  openvino:
    device_cgroup_rules:
      - "c 189:* rmw"
    devices:
      - /dev/dri:/dev/dri
    volumes:
      - /dev/bus/usb:/dev/bus/usb

  openvino-wsl:
    devices:
      - /dev/dri:/dev/dri
      - /dev/dxg:/dev/dxg
    volumes:
      - /dev/bus/usb:/dev/bus/usb
      - /usr/lib/wsl:/usr/lib/wsl
````
{% endcode %}
{% endtab %}

{% tab title="hwaccel.transcoding.yml" %}
{% code expandable="true" %}
```yml
version: "3.8"

# Configurations for hardware-accelerated transcoding

# If using Unraid or another platform that doesn't allow multiple Compose files,
# you can inline the config for a backend by copying its contents
# into the immich-microservices service in the docker-compose.yml file.

# See https://immich.app/docs/features/hardware-transcoding for more info on using hardware transcoding.

services:
  cpu: {}

  nvenc:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities:
                - gpu
                - compute
                - video

  quicksync:
    devices:
      - /dev/dri:/dev/dri

  rkmpp:
    security_opt: # enables full access to /sys and /proc, still far better than privileged: true
      - systempaths=unconfined
      - apparmor=unconfined
    group_add:
      - video
    devices:
      - /dev/rga:/dev/rga
      - /dev/dri:/dev/dri
      - /dev/dma_heap:/dev/dma_heap
      - /dev/mpp_service:/dev/mpp_service
      #- /dev/mali0:/dev/mali0 # only required to enable OpenCL-accelerated HDR -> SDR tonemapping
    volumes:
      #- /etc/OpenCL:/etc/OpenCL:ro # only required to enable OpenCL-accelerated HDR -> SDR tonemapping
      #- /usr/lib/aarch64-linux-gnu/libmali.so.1:/usr/lib/aarch64-linux-gnu/libmali.so.1:ro # only required to enable OpenCL-accelerated HDR -> SDR tonemapping

  vaapi:
    devices:
      - /dev/dri:/dev/dri

  vaapi-wsl: # use this for VAAPI if you're running Immich in WSL2
    devices:
      - /dev/dri:/dev/dri
    volumes:
      - /usr/lib/wsl:/usr/lib/wsl
    environment:
      - LD_LIBRARY_PATH=/usr/lib/wsl/lib
      - LIBVA_DRIVER_NAME=d3d12
```
{% endcode %}
{% endtab %}
{% endtabs %}

***

### 3) Start Immich

Run the following command

```bash
docker compose pull && docker compose up -d
```

***

### Updating Immich

Run

```bash
docker compose down && docker compose pull && docker compose up -d
```

or

```bash
docker compose pull && docker compose up -d
```

***

### Immich OAuth / OpenID Setup

[Immich OAuth / OpenID Setup](authentik/immich.md)

***

### Google Photo Takeout Conversion Helpers

Use either of these scripts to convert your Google Photos Takeout to Immich compatible format.

[Google Photo Takeout Helpers](google-photos-takeout/)
