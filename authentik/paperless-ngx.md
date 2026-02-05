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

{% include "../.gitbook/includes/paperless-ngx-basic-docker-compose-file.md" %}

### For OpenID/OAuth Authentication

Your `docker-compose.yml` file should look something like this

{% include "../.gitbook/includes/paperless-ngx-with-openid-docker-compose-file.md" %}

### Docker Compose Environment File

#### Original Paperless Documentation

Visit [Paperless NGX Full Docker Environment Variables List](https://github.com/lazy-media/public/blob/main/Paperless-NGX/.env/README.md) for all the Paperless-NGX Environment Variables. Make sure to refer to Paperless-NGX Website for use of each Variable.

### Example Environment Variables File

This contains all Environment Variables available from Paperless-NGX documentation site.

{% include "../.gitbook/includes/paperless-ngx-example-environment-variables-file.md" %}
