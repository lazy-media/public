---
description: A Docker Management Interface
---

# Dockhand Docker Management

## Resources

* [Official Site](https://dockhand.pro/)
* [Official Documentation](https://dockhand.pro/manual/)

_For best results, always reference the official documentation._

### Quickstart (Docker Run Command)

```bash
docker run -d \
  --name dockhand \
  --restart unless-stopped \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v dockhand_data:/app/data \
  fnsys/dockhand:latest
```

### Docker Compose

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

### Docker Compose with PostgreSQL

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
