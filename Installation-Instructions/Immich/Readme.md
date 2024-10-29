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

[Example Docker Compose File]

## Example Docker Compose Env File

[Example Docker Compose ENV File]

# Immich Hardware Acceleration Files

Example `hwaccel.ml.yml`


Example `hwaccel.transcoding.yml`


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
