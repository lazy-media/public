# Authentik Installation & Cloudflare Setup Instructions
## Notice
Please note my installation setup before continuing.

This is created in a Proxmox LXC Container running Ubuntu 22.04.4

This also assumes you have docker and docker-compose installed. If not, install it.

You can follow this Guide [Docker Installation](Installation-Instructions/Docker/Readme.md)

## Original Documentation

https://goauthentik.io/docs/installation/docker-compose#preparation

## Authentik Setup

- I currently have Authentik installed alone on a Proxmox LXC container using Ubuntu 22.04, and separate from any other services.
- My Authentik Ports get set to 443 and 80 within the Docker Environment Variables File, but set to the standard ports in the Docker Compose File as 9443:9443 and 9000:9000.
- I currently ONLY run Authentik as my Reverse Proxy, no middle man like NPM, Traefik, Caddy, etc.
- I use Cloudflare Certificates installed into Authentik, not provided by any other reverse proxy or created by Let's Encrypt.
- I do not use Cloudflare Tunnels, I use other security measures provided by Cloudflare to protect my domain.
- I have my ISP Modem in bridge mode and have a Unifi Security Gateway handling all internet traffic.
    - I have port 443 forwarded to Authentik
- For Installation Instructions on how I setup my Authentik, visit [Authentik Installation](Installation-Instructions/Authentik/Readme.md)

## Other Requirements

Make sure you have Docker and Docker compose installed. You can follow this guide if you need help. [Docker Engine and Docker Compose Installation](Installation-Instructions/Docker/Readme.md)

## Authentik Installation Steps

Login to root user of Proxmox LXC

---

Install additional dependencies
```
apt-get install -y pwgen
```

Create Authentik folder
```
mkdir -p docker/authentik
```
Change Directory into Authentik Folder
```
cd docker/authentik
```
Download Docker Compose File for Authentik
```
wget https://goauthentik.io/docker-compose.yml
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
# Authentik Docker Compose, .env, and GeoIP Override Files

Make sure you are still in the folder `docker/authentik`
You should be since we have only created folders above.

## Example Docker Compose File to persist data in the directories created above

Edit this file if needed, with `nano docker-compose.yml` and paste the following into this file, or edit to your preference.

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
      - "${COMPOSE_PORT_LDAPS:-6636}:6636"
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
This is the `.env` file
```
### Authentik Postgres Settings
### Uncomment any lines below to match your Postgres Server

### Authentik Secret Key
### REQUIRED
AUTHENTIK_SECRET_KEY=SHOULD HAVE BEEN GENERATED ABOVE AND MAYBE ONLY THING ORIGINALLY IN THIS FILE.

### Internal Postgres Server Settings
### REQUIRED
PG_USER=authentik
PG_PASS=SOME RANDOM PASSWORD

### External Postgres Server Settings Settings
# AUTHENTIK_POSTGRESQL__HOST=
# AUTHENTIK_POSTGRESQL__NAME=
# AUTHENTIK_POSTGRESQL__USER=authentik
# AUTHENTIK_POSTGRESQL__PORT=
# AUTHENTIK_POSTGRESQL__PASSWORD=SOME RANDOM PASSWORD
# AUTHENTIK_POSTGRESQL__USE_PGBOUNCER=
# AUTHENTIK_POSTGRESQL__USE_PGPOOL=
# AUTHENTIK_POSTGRESQL__SSLMODE=
# AUTHENTIK_POSTGRESQL__SSLROOTCERT=
# AUTHENTIK_POSTGRESQL__SSLCERT=
# AUTHENTIK_POSTGRESQL__SSLKEY=


### Authentik External REDIS Settings
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

### Authentik Server Image and Version Number
### REQUIRED
AUTHENTIK_TAG=2024.2.3
AUTHENTIK_IMAGE=ghcr.io/goauthentik/server

### User Settings
AUTHENTIK_DEFAULT_USER_CHANGE_NAME=false
AUTHENTIK_DEFAULT_USER_CHANGE_EMAIL=false
AUTHENTIK_DEFAULT_USER_CHANGE_USERNAME=false

### Authentik Listen Settings (Set server address and Port number, eg 0.0.0.0:9000 0.0.0.0:9443)
### SET THESE TO THE PORTS YOU WANT TO USE FOR AUTHENTIK ###
COMPOSE_PORT_HTTP=80
COMPOSE_PORT_HTTPS=443

### Authentik LDAP Listen Settings (Set server address and Port number, eg 0.0.0.0:3389 0.0.0.0:6636)
### UNCOMMENT TO USE LDAP ###
# COMPOSE_PORT_LDAP=
# COMPOSE_PORT_LDAPS=6636

### Authentik Prometheus Metrics Settings (Set server address and port number, eg 0.0.0.0:9300)
### UNCOMMENT TO USE PROMETHEUS METRICS ###
# COMPOSE_PORT_METRICS=9300

### GDPR Compliance Settings
AUTHENTIK_GDPR_COMPLIANCE=true

### Log Level Settings (Supports debug, info, warning, error, trace)
# AUTHENTIK_LOG_LEVEL=info

### Go Debugging Settings (Set server address and port number, eg 0.0.0.0:9900
# AUTHENTIK_LISTEN__DEBUG=

### Error Reporting Settings
AUTHENTIK_ERROR_REPORTING__ENABLED=true

### Cookie Domain Settings
# AUTHENTIK_COOKIE_DOMAIN=

### Trusted Proxies settings
### Defaults to 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, fe80::/10, ::1/128
# AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS=

### GeoIP Settings
### UNCOMMENT BOTH LINES BELOW TO USE GEOIP
# AUTHENTIK_EVENTS__CONTEXT_PROCESSORS__GEOIP=./geoip/GeoLite2-City.mmdb
# AUTHENTIK_EVENTS__CONTEXT_PROCESSORS__ASN=./geoip/GeoLite2-ASN.mmdb

### GMAIL EMAIL / SMTP Settings
AUTHENTIK_EMAIL__HOST=smtp.gmail.com
AUTHENTIK_EMAIL__PORT=587
AUTHENTIK_EMAIL__USERNAME=email@address.example
AUTHENTIK_EMAIL__PASSWORD=google-app-password
AUTHENTIK_EMAIL__USE_TLS=true
AUTHENTIK_EMAIL__USE_SSL=false
AUTHENTIK_EMAIL__TIMEOUT=10
AUTHENTIK_EMAIL__FROM=noreply@authentik.domain

### Update Check Settings
# AUTHETNIK_DISABLE_UPDATE_CHECK=false
```

## Example GEOIP Override file
Name this file `docker-compose.override.yml`

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

### Authentik User Setup
Navigate to

```
https://auth.domain.example/if/flow/initial-setup/
```
or
```
http://IP.ADDRESS.OF.AUTHENTIK:9000/if/flow/initial-setup/
```

This should ask you to setup your Authentik admin (if setup correctly)

## Initial Setup Flow Not Showing Up after creation.

If for some reason the initial setup flow doesn't show up, Authentik might have already created the user and deleted the initial setup flow automatically. If this happened to you, you should be able to gain access to the default Authentik Admin by using the following command by logging into the terminal of the host for Authentik.

- Login to root user of Proxmox LXC
- Navigate to `cd docker/authentik`
- Enter the following command:

```
docker-compose run --rm server create_recovery_key 1 akadmin
```
This should output a link that you can copy and paste into your web browser to login to the default Authentik Admin. Be sure to change the url to point to your local Authentik IP Address or the Domain name of your Authentik Instance before navigating to it, if it didn't generate correctly.

# Cloudflare Setup

1. Login to your Cloudflare Account.
2. Navigate to the DNS Records section of your domain you want attached to Authentik.
3. Create 3 DNS records.
    - Set one `DNS A Record` that is set for `your domain` to your `Public IP Address`. (Root Domain (i.e. domain.example))
    - Set one `CNAME Record` with an `*` for a wildcard with the destination of `@` for root domain. (Wildcard Entry)
    - Set the last one as a `CNAME Record` for `auth` and destination of `@` for root domain. (Authentik)
4. In your Cloudflare Account, navigate to SSL/TLS > Overview
    - Set your `Encryption Mode` to `Full (Strict)`
    - (Optional) Enable `SSL/TLS Recommender`
5. Navigate to SSL/TLS > Edge Certificates
    - (Recommended) Enable `Always Use HTTPS`
    - Configure `HTTP Strict Transport Security (HSTS)`
        - (Recommended) **Enable** `HSTS`
        - (Recommended) `Set Max Age Header` to `6 Months`
        - (Recommended) **Enable** `Apply HSTS Policy to subdomains`
        - (Recommended) **Disable** `Preload`
        - (Recommended) **Enable** `No-Sniff Header`
    - Set `Minimum TLS Version` to `TLS 1.3`
    - (Recommended) **Enable** `Opportunistic Encryption`
    - **Enable** `TLS 1.3`
    - (Recommended) **Enable** `Automatic HTTPS Rewrites`
6. Navigate to SSL/TLS > Origin Server
    - Create an `Origin Certificate` if one does not exist already.
        - If one exists, `Revoke` and `Create` a new one.
    - Create your Certificate with `RSA (2048)`
    - Your hostnames should include the wildcard ( * ) entry and the root domain name at least.
    - Choose your `Certificate Validity` Length
    - Copy the contents of both boxes on the next screen into a word or text document temporarily. There should be a `Certificate Key` and a `Private Key`. **DO NOT EVER SHARE THIS INFORMATION WITH ANYONE, IT IS THE KEY TO YOUR DOMAIN CONNECTED TO CLOUDFLARE**

# Authentik Certificate Setup

1. Login to your Authentik Admin Account
2. Navigate to `System > Certificates`
    - Click on `Create` to Import the Cloudflare Origin Certificate we just created.
    - Name the Certificate whatever you want
    - Paste the `Certificate Key` into the `Certificate` box
    - Paste the `Private Key` into the `Private Key` box
    - Click `Create`
3. Navigate to `System > Brands`
    - Click the `Edit` button under `Actions`
    - Scroll to the bottom of the Window and `Expand Other Global Settings`
    - Under `Web Certificate`, choose your Cloudflare Certificate we just imported.
    - Click `Update`
4. Navigate to `Applications > Outposts`
    - Click the `Edit` button under `Actions`
    - Scroll to the bottom and `Expand Advanced Settings`
        - Make sure your `authentik_host:` is set to the CNAME you created in Cloudflare. (i.e. `https://auth.domain.example`)
    - Click `Update`

## Conclusion

If everything went according to plan, the Authentik container will persist all data for Authentik under the `docker/authentik` directory for `certs`, `custom-templates`, `database`, `geoip`, `media` and `redis`. This will make it much easier to upgrade Authentik in the future. This should also enable HTTPS connections to Authentik and allow the use of a custom Cloudflare Origin Certificate using Cloudflare's Stict SSL mode with other Cloudflare security measures enabled.

## Updating

Edit the `.env` file and update the `AUTHENTIK_TAG` to the latest version and then run `docker-compose down && docker-compose pull && docker-compose up -d` or just `docker-compose down && docker-compose up -d`.

---

Edit Docker env File
```
cd docker/authentik && nano .env
```
Restart Authentik
```
docker-compose down && docker-compose pull && docker-compose up -d
```
or
```
docker-compose down && docker-compose up -d
```

## Application and Provider Setup

Please refer to [Authentik Application and Provider Setup](Authentik/Applications-&-Providers/Readme.md)
