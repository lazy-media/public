---
description: Information on how to setup Paperless-NGX OpenID / OAuth with Authentik
---

# Paperless-NGX

## Original Documentation / Website

* [Paperless NGX](https://docs.paperless-ngx.com)
* [Docker Engine Installation](https://docs.docker.com/engine/install/ubuntu/)

### Prerequisites

* Installed in a Proxmox LXC with Ubuntu 22.04.4
* Assumes you followed instructions from [Paperless-NGX Installation](https://github.com/lazy-media/public/blob/main/Paperless-NGX/README.md)
* Assumes you have basic knowledge of how to setup an Authentik OAuth2/OpenID Provider. If not, you can follow this guide [Basic OAuth/OpenID Setup](applications-and-providers.md#authentik-basic-oauth2openid-setup)

## Adding Authentik OpenID / OAuth to Paperless-NGX

### Editing Docker Compose File

Login to root user of Proxmox LXC

### Switch to the user you installed Paperless with

```
su - YOURUSER
```

Change Directory to Paperless NGX

```
cd paperless-ngx/
```

```
nano docker-compose.yml
```

I personally went through and changed the directories to persist all data. This is my example docker compose file

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

### For OpenID/OAuth Authentication

Your `docker-compose.yml` file should look something like this

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

### Docker Compose Environment File

This file is named `docker-compose.env`

Visit [Paperless NGX Full Docker Environment Variables List](https://github.com/lazy-media/public/blob/main/Paperless-NGX/.env/README.md) for all the Paperless-NGX Environment Variables. Make sure to refer to Paperless-NGX Website for use of each Variable.
