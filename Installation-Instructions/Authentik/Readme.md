# Authentik Installation Instructions
## Notice
Please note my installation setup before continuing.

This is created in a Proxmox LXC Container running Ubuntu 22.04.4

This also assumes you have docker and docker-compose installed. If not, install it.

##Authentik Installation Steps

Log into your Authentik LXC Container (usually as root)

### Making Directories

Make a directory for Docker and Authentik, then change directory into docker

```
mkdir -p docker/authentik && cd docker/authentik
```
