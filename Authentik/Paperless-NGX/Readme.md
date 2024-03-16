# Original Documentation / Website

- [Paperless NGX](https://docs.paperless-ngx.com)
- [Docker Engine Installation](https://docs.docker.com/engine/install/YOURUSER/)

## Prerequisites

- Installed in a Proxmox LXC with YOURUSER 22.04.4

# Installation Process

## Login

Login as root user

## Update System

```
apt update && apt dist-upgrade -y
```

### Install CA-Certificates and Curl

```
sudo apt-get install -y ca-certificates curl
```

## Install Docker and Docker Compose Plugin
Setup Docker's Official GPG Key:
```
apt-get update
```
```
install -m 0755 -d /etc/apt/keyrings 
```
```
curl -fsSL https://download.docker.com/linux/YOURUSER/gpg -o /etc/apt/keyrings/docker.asc
```
```
chmod a+r /etc/apt/keyrings/docker.asc
```
Add Docker Repository to APT Sources:

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/YOURUSER \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
Run an Update
```
apt-get update
```
Install Docker
```
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


## Create Non-Root User with no password with Docker Privledges
Replace 'YOURUSER' with the name of a user you want
```
adduser YOURUSER --disabled-password
```
Fill in your information if you want or just press ENTER until the end then press Y to Confirm account creation

Now Add this user to the docker group
```
usermod -aG docker YOURUSER
```

## Switch to new User

```
su - YOURUSER
```

## Install Paperless-NGX using Easy Install

```
bash -c "$(curl --location --silent --show-error https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/install-paperless-ngx.sh)"
```

Fill out the information as told in the setup steps.

# Editing Docker Compose File

Change Directory to Paperless NGX

```
cd paperless-ngx/
```
```
nano docker-compose.yml
```
I personally went through and changed the directories to persist all data.
This is my example docker compose file
```
version: "3.4"
services:
  broker:
    image: docker.io/library/redis:7
    restart: unless-stopped
    volumes:
      - /home/YOURUSER/paperless-ngx/redisdata:/data

  db:
    image: docker.io/library/postgres:15
    restart: unless-stopped
    volumes:
      - /home/YOURUSER/paperless-ngx/database:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: paperless

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    restart: unless-stopped
    depends_on:
      - db
      - broker
      - gotenberg
      - tika
    ports:
      - "8000:8000"
    volumes:
      - /home/YOURUSER/paperless-ngx/data:/usr/src/paperless/data
      - /home/YOURUSER/paperless-ngx/media:/usr/src/paperless/media
      - /home/YOURUSER/paperless-ngx/export:/usr/src/paperless/export
      - /home/YOURUSER/paperless-ngx/consume:/usr/src/paperless/consume
    env_file: docker-compose.env
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998

  gotenberg:
    image: docker.io/gotenberg/gotenberg:7.10
    restart: unless-stopped

    # The gotenberg chromium route is used to convert .eml files. We do not
    # want to allow external content like tracking pixels or even javascript.
    command:
      - "gotenberg"
      - "--chromium-disable-javascript=true"
      - "--chromium-allow-list=file:///tmp/.*"

  tika:
    image: ghcr.io/paperless-ngx/tika:latest
    restart: unless-stopped

volumes:
  redisdata:
```

## For OpenID/OAuth Authentication

Your ```docker-compose.yml``` file should look something like this

```
version: "3.4"
services:
  broker:
    image: docker.io/library/redis:7
    restart: unless-stopped
    volumes:
      - /home/YOURUSER/paperless-ngx/redisdata:/data

  db:
    image: docker.io/library/postgres:15
    restart: unless-stopped
    volumes:
      - /home/YOURUSER/paperless-ngx/database:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: paperless

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    restart: unless-stopped
    depends_on:
      - db
      - broker
      - gotenberg
      - tika
    ports:
      - "8000:8000"
    volumes:
      - /home/YOURUSER/paperless-ngx/data:/usr/src/paperless/data
      - /home/YOURUSER/paperless-ngx/media:/usr/src/paperless/media
      - /home/YOURUSER/paperless-ngx/export:/usr/src/paperless/export
      - /home/YOURUSER/paperless-ngx/consume:/usr/src/paperless/consume
    env_file: docker-compose.env
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      PAPERLESS_APPS: allauth.socialaccount.providers.openid_connect
      PAPERLESS_SOCIALACCOUNT_PROVIDERS: >
          {
            "openid_connect": {
              "APPS": [
                {
                  "provider_id": "authentik",
                  "name": "AUTHENTIK",
                  "client_id": "YOUR-AUTHENTIK-OAUTH-CLIENT-ID",
                  "secret": "YOUR-AUTHENTIK-OAUTH-CLIENT-SECRET",
                  "settings": {
                    "server_url": "https://YOUR-AUTHENTIK-URL/application/o/PAPERLESS-OAUTH-SLUG/.well-known/openid-configuration"
                  }
                }
              ],
              "OAUTH_PKCE_ENABLED": "True"
            }
          }

  gotenberg:
    image: docker.io/gotenberg/gotenberg:7.10
    restart: unless-stopped

    # The gotenberg chromium route is used to convert .eml files. We do not
    # want to allow external content like tracking pixels or even javascript.
    command:
      - "gotenberg"
      - "--chromium-disable-javascript=true"
      - "--chromium-allow-list=file:///tmp/.*"

  tika:
    image: ghcr.io/paperless-ngx/tika:latest
    restart: unless-stopped

volumes:
  redisdata:
```

## Docker Compose Environment File
This file is named ```docker-compose.env```

Input any environment files you want added into Paperless NGX