# Immich Installation

## Original Documentation
[Immich Website](https://immich.app/)

## Docker Compose Installation with Persistant Storage for all Volumes

### Installation Requirements / Setup
- Installed in a Proxmox LXC
- Installed on Ubuntu 22.04
- Installed Docker Compose

### Assumptions
- Basic understanding of Docker and Docker Compose

# Docker Compose File
```
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
    command: ['start.sh', 'immich']
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    ports:
      - 2283:3001
    depends_on:
      - redis
      - database
    restart: always

  immich-microservices:
    container_name: immich_microservices
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    # extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/hardware-transcoding
    #   file: hwaccel.transcoding.yml
    #   service: cpu # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    command: ['start.sh', 'microservices']
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    depends_on:
      - redis
      - database
    restart: always

  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, openvino] to the image tag.
    # Example tag: ${IMMICH_VERSION:-release}-cuda
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    # extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/ml-hardware-acceleration
    #   file: hwaccel.ml.yml
    #   service: cpu # set to one of [armnn, cuda, openvino, openvino-wsl] for accelerated inference - use the `-wsl` version for WSL2 where applicable
    volumes:
      - ./model-cache:/cache
    env_file:
      - .env
    restart: always

  redis:
    container_name: immich_redis
    image: registry.hub.docker.com/library/redis:6.2-alpine@sha256:51d6c56749a4243096327e3fb964a48ed92254357108449cb6e23999c37773c5
    restart: always

  database:
    container_name: immich_postgres
    image: registry.hub.docker.com/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:90724186f0a3517cf6914295b5ab410db9ce23190a2d9d0b9dd6463e3fa298f0
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
    volumes:
      - ${DB_DATA_LOCATION}:/var/lib/postgresql/data
    restart: always

volumes:
  model-cache:
```

## Example Docker Compose Env File
```
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
# Immich Hardware Acceleration Files
name this `hwaccel.ml.yml`
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
```

Name this `hwaccel.transcoding.yml`
```
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

# Start and Run Immich
Run the following command
```
docker compose pull && docker compose up -d
```

# Updating Immich
Run
```
docker compose down && docker compose pull && docker compose up -d
```

# Immich OAuth / OpenID Setup
[Immich OAuth / OpenID Setup](Authentik/Immich/Readme.md)
