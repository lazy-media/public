---
description: A Docker Management Interface
---

# Dockhand Docker Management

### Overview

Dockhand is a lightweight web UI for managing Docker. This page gives copy/paste install examples for common setups.

{% hint style="warning" %}
Mounting `/var/run/docker.sock` gives Dockhand **full control** of the Docker host. Treat access to Dockhand as admin/root-level access.
{% endhint %}

### Prerequisites

* Docker Engine installed and running
* Network access to the host port you publish (examples use `3000`)

### Which install option should you use?

* **Docker Run Command**: fastest to test.
* **Docker Run with Persistent Data**: uses a host folder. Easiest to back up.
* **Docker Compose**: easiest to maintain long-term.
* **Docker Compose with PostgreSQL**: useful for more durable storage and easier migrations.

## Resources

* [Official Site](https://dockhand.pro/)
* [Official Documentation](https://dockhand.pro/manual/)

_For best results, always reference the official documentation._

### Quickstart (Docker Run Command)

This runs Dockhand on port `3000` and stores data in a Docker named volume.

```bash
docker run -d \
  --name dockhand \
  --restart unless-stopped \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v dockhand_data:/app/data \
  fnsys/dockhand:latest
```

Open:

* `http://<docker-host>:3000`

### Quickstart (Docker Run Command)

With Persistent Data

This stores data in `/opt/dockhand` on the host. It is easier to back up and inspect.

```bash
# Create the directory on the host
mkdir -p /opt/dockhand
```

```bash
# Use matching paths with DATA_DIR
docker run -d \
  --name dockhand \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /opt/dockhand:/opt/dockhand \
  -e DATA_DIR=/opt/dockhand \
  fnsys/dockhand:latest
```

Open:

* `http://<docker-host>:3000`

### Docker Compose

This is the same as the first quickstart, but easier to update and manage.

```yml
services:
  dockhand:
    image: fnsys/dockhand:latest
    container_name: dockhand
    restart: unless-stopped
    ports:
      - 3000:3000
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dockhand_data:/app/data

volumes:
  dockhand_data:
```

Open:

* `http://<docker-host>:3000`

### Docker Compose with Persistent Data

Use this when you want the benefits of Compose plus persistent storage you can back up.

```yml
services:
  dockhand:
    image: fnsys/dockhand:latest
    container_name: dockhand
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dockhand_data:/app/data

volumes:
  dockhand_data:
```

Open:

* `http://<docker-host>:3000`

### Docker Compose with PostgreSQL

Use this if you prefer Postgres over file-based storage.

{% hint style="info" %}
Change `changeme` before deploying, and keep the Postgres volume (`postgres_data`) backed up.
{% endhint %}

```yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dockhand
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: dockhand
    volumes:
      - postgres_data:/var/lib/postgresql/data

  dockhand:
    image: fnsys/dockhand:latest
    ports:
      - 3000:3000
    environment:
      DATABASE_URL: postgres://dockhand:changeme@postgres:5432/dockhand
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dockhand_data:/app/data
    depends_on:
      - postgres

volumes:
  postgres_data:
  dockhand_data:
```

Open:

* `http://<docker-host>:3000`

### Backups

Back up based on the storage method you chose:

* **Named volume**: back up `dockhand_data`
* **Bind mount**: back up the host directory you mounted (example: `/opt/dockhand`)
* **PostgreSQL**: back up `postgres_data` (and keep your Postgres credentials safe)

### Troubleshooting / common tweaks

* **Port `3000` already in use**
  * Docker run: change `-p 3000:3000` to `-p 3080:3000`
  * Docker Compose: change `ports: - "3000:3000"` to `ports: - "3080:3000"`

### Conclusion

Dockhand should now be reachable on the port you published (commonly `http://<host>:3000`) and able to manage containers on the Docker host. Keep it protected, since access to Dockhand effectively grants admin-level control of Docker.
