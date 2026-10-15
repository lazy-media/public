---
description: >-
  Portainer is a way to manage a docker server with a web-ui. It includes many
  features to manage docker.
---

# Portainer Docker Management

### Overview

Portainer CE is a web UI for managing Docker. It lets you manage containers, images, networks, volumes, and stacks from a browser.

This guide installs **Portainer Community Edition (CE)** on a single Docker host. It assumes Docker is already installed and working.

### Official documentation (recommended)

> [Portainer Documentation](https://docs.portainer.io/start/install-ce/server/docker/linux)

### Authentik OpenID / OAuth Setup

> [Authentik OpenID / OAuth Setup](../../authentik/portainer.md)

{% hint style="warning" %}
Portainer is an admin tool. Anyone with access can control your Docker host.
{% endhint %}

### What you’ll end up with

* A persistent Portainer install (data stored in a Docker volume)
* A web UI available on:
  * `https://<docker-host>:9443` (recommended)
  * `http://<docker-host>:9000` (optional/insecure)

### Prerequisites

* A running Docker Engine
* A user that can run Docker commands (`docker ps` works)
* A free TCP port on the host for:
  * `9443` (Portainer HTTPS UI)
  * `9000` (Portainer HTTP UI, optional)
  * `8000` (Edge Agent tunnel, optional)

{% hint style="info" %}
If you already use a reverse proxy, you can publish only `9443` (or even skip host ports and proxy directly). This guide keeps it simple and publishes ports explicitly.
{% endhint %}

***

### Install (Docker volume + `docker run`)

#### 1) Create the Portainer data volume

```bash
docker volume create portainer_data
```

#### 2) Start Portainer

This is the standard “single server” install.

```bash
docker run -d \
  --name portainer \
  --restart=always \
  -p 8000:8000 \
  -p 9000:9000 \
  -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

#### 3) Open the UI

* Go to `https://<docker-host>:9443`

If you can’t use HTTPS yet, you can use:

* `http://<docker-host>:9000`

***

### Install (Docker Compose)

Use this if you prefer managing Portainer as a stack.

{% tabs %}
{% tab title="Option A (recommended): download" %}
**1) Download the Docker Compose file**

```bash
curl -L https://downloads.portainer.io/ce-lts/portainer-compose.yaml -o portainer-compose.yaml
```

**2) Launch Portainer**

```bash
docker compose -f portainer-compose.yaml up -d
```

**3) Open the UI**

* `https://<docker-host>:9443`

{% hint style="info" %}
If you don’t know what ports were published by the downloaded Compose file, run `docker ps` and check the Portainer container’s port mappings.
{% endhint %}
{% endtab %}

{% tab title="Option B: create your own" %}
**1) Create `docker-compose.yml`**

```yml
services:
  portainer:
    container_name: portainer
    image: portainer/portainer-ce:lts
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    ports:
      - 9443:9443
      - 8000:8000  # Remove if you do not intend to use Edge Agents

volumes:
  portainer_data:
    name: portainer_data

networks:
  default:
    name: portainer_network
```

**2) Start it**

```bash
docker compose up -d
```

**3) Open the UI**

* `https://<docker-host>:9443`
{% endtab %}
{% endtabs %}

***

### First-time setup (in the UI)

#### 1) Create the initial admin user

On first launch, Portainer prompts you to create an admin user. Use a strong password and store it in your password manager.

#### 2) Connect your local Docker environment

For a single-host install, choose:

* **Get Started** → **Local** (or “Docker” local environment)

Portainer will use the Docker socket you mounted:

* `/var/run/docker.sock:/var/run/docker.sock`

#### 3) Sanity check

In Portainer:

* Check **Environments** shows your local Docker host
* Check **Containers** lists your running containers

***

### Post-install hardening (recommended)

* Prefer `https://<host>:9443` over `http://<host>:9000`
* Restrict network access to Portainer:
  * LAN-only access, or
  * VPN-only access, or
  * reverse proxy with authentication
* Disable or firewall port `9000` if you don’t need it

***

### Backups

Portainer stores state in `portainer_data`.

Back up options:

* **Recommended**: back up the Docker volume `portainer_data`
* **Also acceptable**: use Portainer’s built-in backup feature (if enabled in your version/config)

{% hint style="info" %}
If you run Portainer on production systems, test restores. Don’t just “set and forget” backups.
{% endhint %}

***

### Updating Portainer

#### Docker run installs

```bash
docker pull portainer/portainer-ce:latest
docker rm -f portainer
```

Re-run the same `docker run ...` command you used originally.

#### Docker Compose installs

From the folder containing `docker-compose.yml`:

```bash
docker compose pull
docker compose up -d
```

***

### Troubleshooting

#### Portainer won’t start

* Check logs:

```bash
docker logs -f portainer
```

* Verify your ports are free:
  * `8000`, `9000`, `9443`

#### UI loads, but no containers show up

* Confirm the Docker socket mount exists:

```bash
ls -la /var/run/docker.sock
```

* Confirm Portainer has the mount:

```bash
docker inspect portainer --format '{{ json .Mounts }}'
```
