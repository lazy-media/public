# Authentik Installation Instructions
## Notice
Please note my installation setup before continuing.

This is created in a Proxmox LXC Container running Ubuntu 22.04.4

This also assumes you have docker and docker-compose installed. If not, install it.

## Original Documentation

https://goauthentik.io/docs/installation/docker-compose#preparation

## Authentik Installation Steps

Download Docker Compose File for Authentik
```
wget https://goauthentik.io/docker-compose.yml
```

Install additional dependencies
```
sudo apt-get install -y pwgen
```

Create Authentik folder
```
mkdir -p docker/authentik
```
Change Directory into Authentik Folder
```
cd docker/authentik
```
Create Persistant directories for Authentik
```
mkdir certs
```
```
mkdir custom-templates
```
```
mkdir database
```
```
mkdir geoip
```
```
mkdir media
```
```
mkdir redis
```

Key Generation & .env file creation
```
echo "PG_PASS=$(pwgen -s 40 1)" >> .env
```
```
echo "AUTHENTIK_SECRET_KEY=$(pwgen -s 50 1)" >> .env
```
## Creating Authentik Docker Compose, .env, and GeoIP Override Files

Make sure you are still in the folder ```docker/authentik```
You should be since we have only created folders above.

## Example Docker Compose File to persist data in the directories created above

Create this file if needed, with ```nano docker-compose.yml``` and paste the following into this file.

```
version: "3.4"

services:
  postgresql:
    image: docker.io/library/postgres:12-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 5s
    volumes:
      - ./database:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${PG_PASS:?database password required}
      POSTGRES_USER: ${PG_USER:-authentik}
      POSTGRES_DB: ${PG_DB:-authentik}
    env_file:
      - .env
  redis:
    image: docker.io/library/redis:alpine
    command: --save 60 1 --loglevel warning
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 3s
    volumes:
      - ./redis:/data
  server:
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2024.2.2}
    restart: unless-stopped
    command: server
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${PG_USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${PG_DB:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${PG_PASS}
    volumes:
      - ./media:/media
      - ./custom-templates:/templates
    env_file:
      - .env
    ports:
      - "${COMPOSE_PORT_HTTP:-9000}:9000"
      - "${COMPOSE_PORT_HTTPS:-9443}:9443"
      - "${COMPOSE_PORT_METRICS:-9300}:9300"
    depends_on:
      - postgresql
      - redis
  worker:
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2024.2.2}
    restart: unless-stopped
    command: worker
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${PG_USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${PG_DB:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${PG_PASS}
    # `user: root` and the docker socket volume are optional.
    # See more for the docker socket integration here:
    # https://goauthentik.io/docs/outposts/integrations/docker
    # Removing `user: root` also prevents the worker from fixing the permissions
    # on the mounted folders, so when removing this make sure the folders have the correct UID/GID
    # (1000:1000 by default)
    user: root
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./media:/media
      - ./certs:/certs
      - ./custom-templates:/templates
    env_file:
      - .env
    depends_on:
      - postgresql
      - redis

volumes:
  database:
    driver: local
  redis:
    driver: local
```

## EXAMPLE Docker Environment Variables File (.env)
This is the ```.env``` file
```
# Authentik Postgres Settings
# Uncomment any lines below to match your Postgres Server

# AUTHENTIK_POSTGRESQL__HOST=
# AUTHENTIK_POSTGRESQL__NAME=
# AUTHENTIK_POSTGRESQL__USER=
# AUTHENTIK_POSTGRESQL__PORT=
# AUTHENTIK_POSTGRESQL__PASSWORD=
# AUTHENTIK_POSTGRESQL__USE_PGBOUNCER=
# AUTHENTIK_POSTGRESQL__USE_PGPOOL=
# AUTHENTIK_POSTGRESQL__SSLMODE=
# AUTHENTIK_POSTGRESQL__SSLROOTCERT=
# AUTHENTIK_POSTGRESQL__SSLCERT=
# AUTHENTIK_POSTGRESQL__SSLKEY=


# Authentik REDIS Settings
# Uncomment any lines below to match your REDIS Server
# AUTHENTIK_REDIS__HOST=
# AUTHENTIK_REDIS__PORT=
# AUTHENTIK_REDIS__PASSWORD=
# AUTHENTIK_REDIS__TLS=
# AUTHENTIK_REDIS__TLS_REQS=
# AUTHENTIK_REDIS__DB=
# AUTHENTIK_REDIS__CACHE_TIMEOUT=
# AUTHENTIK_REDIS__CACHE_TIMEOUT_FLOWS=
# AUTHENTIK_REDIS__CACHE_TIMEOUT_POLICIES=
# AUTHENTIK_REDIS__CACHE_TIMEOUT_REPUTATION=


# Authentik Listen Settings (Set server address and Port number, eg 0.0.0.0:9000 0.0.0.0:9443)
# AUTHENTIK_LISTEN__HTTP=
# AUTHENTIK_LISTEN__HTTPS=

# Authentik LDAP Listen Settings (Set server address and Port number, eg 0.0.0.0:3389 0.0.0.0:6636)
# AUTHENTIK_LISTEN__LDAP=
# AUTHENTIK_LISTEN__LDAPS=

# Authentik Prometheus Metrics Settings (Set server address and port number, eg 0.0.0.0:9300)
# COMPOSE_PORT_METRICS=9300

# Go Debugging Settings (Set server address and port number, eg 0.0.0.0:9900
# AUTHENTIK_LISTEN__DEBUG=

# Trusted Proxies settings
# Defaults to 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, fe80::/10, ::1/128
# AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS=
```

## Example GEOIP Override file
Name this file ```docker-compose.override.yml```

```
version: "3.2"

services:
    server:
        volumes:
            - geoip:/geoip
    worker:
        volumes:
            - geoip:/geoip
    geoipupdate:
        image: "maxmindinc/geoipupdate:latest"
        volumes:
            - "./geoip:/usr/share/GeoIP"
        environment:
            GEOIPUPDATE_EDITION_IDS: "GeoLite2-City GeoLite2-ASN"
            GEOIPUPDATE_FREQUENCY: "8"
            GEOIPUPDATE_ACCOUNT_ID: "YOUR_MAXMIND_ID"
            GEOIPUPDATE_LICENSE_KEY: "YOUR_MAXMIND_KEY"
volumes:
    geoip:
        driver: local
```

# Launch and run Authentik

Run the following command to download and launch Authentik

```
docker-compose up -d
```

## Conclusion

With this setup method, the container will create folders under the ```docker/authentik``` directory for ```certs```, ```custom-templates```, ```database```, ```geoip```, ```media``` and ```redis``` and persist data into these folders.

When updating Authentik, you just need to edit the ```docker-compose.yml``` file and update the server tag for authentik server and authentik worker, and then run ```docker-compose up -d``` again.
