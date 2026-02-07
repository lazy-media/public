---
description: An example of how Lazy Media has their Authentik Installation Setup.
---

# Authentik Installation

## Authentik Installation & Cloudflare Setup Instructions

### Notice

Please note my installation setup before continuing.

This is created in a Proxmox LXC Container running Ubuntu 22.04.4

This also assumes you have docker and docker compose installed. If not, install it.

You can follow this Guide [Docker Installation](../docker/installation.md)

### Original Documentation

[https://goauthentik.io/docs/installation/docker-compose#preparation](https://goauthentik.io/docs/installation/docker-compose#preparation)

### Authentik Prerequisites & Environment Setup

#### Infrastructure Details

* **Host Environment:** Proxmox LXC container (Ubuntu 22.04)
* **Deployment Model:** Isolated standalone installation
* **Reverse Proxy:** Authentik-only solution (no NPM/Traefik/Caddy)

#### Authentik Deployment Overview

My Authentik implementation uses the official Docker Compose file from Authentik's documentation with the following customizations:

* Volume persistence modifications for all data stores
* Additional port exposures for service integration

#### Network Configuration

* **Port Mapping:**
  * Internal: 443/80 (Docker environment variables)
  * External: 9443:9443, 9000:9000 (Docker Compose)
* **Security Infrastructure:**
  * Cloudflare certificates (directly installed in Authentik)
  * No Cloudflare Tunnels (alternative Cloudflare security measures)
  * ISP modem in bridge mode
  * UniFi Security Gateway handling all traffic
    * Port 443 forwarded to Authentik

**Support Scope:**\
Please note that I can only provide support for products and services documented in this repository. Undocumented items indicate either:

* The service is not in use
* Not configured with Authentik integration
* Outside my support capabilities

### Other Requirements

* Some knowledge of basic commands in Ubuntu and Docker are recommended.
* Docker and Docker Compose must be installed.
  * You can follow this guide if you need help. [Docker Engine and Docker Compose Installation](../Docker/Installation/)

***

### Resources

#### Official Documentation

* [Authentik Product Documentation](https://docs.goauthentik.io/docs)
* [GitHub Issue Tracker](https://github.com/goauthentik/authentik/issues)
* [Official Discord Server](https://goauthentik.io/discord)

#### Recommended Learning Resources

[Cooptonian - Authentik Setup Video Series](https://youtube.com/playlist?list=PLH73rprBo7vSkDq-hAuXOoXx2es-1ExOP\&si=Y0byly0a4PmfdxkR)

***

### Authentik Installation Steps

Login to root user of Proxmox LXC

#### (Recommended) Create Authentik Machine User

Create a user for Authentik to run as instead of root with no password enabled

```
adduser authentik --disabled-password
```

Add user to Docker Group

```
usermod -aG docker authentik
```

Switch to newly created Authentik User

```
su - authentik
```

All commands should still run fine below, if not, add `sudo` to the beginning of each line.

***

### Authentik Setup

Install additional dependencies for key generation

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

Download Docker Compose File for Authentik

{% hint style="warning" %}
This will download the latest version of the Authentik compose file, but the version below contains Redis, which does not exist in the latest version of Authentik. Please be cautious of this when following this guide.
{% endhint %}

```
wget https://goauthentik.io/docker-compose.yml
```

Create Persistant directories for Authentik

```bash
mkdir -p {certs, custom-templates, database, geoip, media, redis}
```

Or you can make them one at a time.

```bash
mkdir certs
```

```bash
mkdir custom-templates
```

```bash
mkdir database
```

```bash
mkdir geoip
```

```bash
mkdir media
```

```bash
mkdir redis
```

Key Generation & .env file creation

```bash
echo "PG_PASS=$(pwgen -s 40 1)" >> .env
```

```bash
echo "AUTHENTIK_SECRET_KEY=$(pwgen -s 50 1)" >> .env
```

***

## Authentik Docker Compose, .env, and GeoIP Override Files

{% hint style="danger" %}
PLEASE NOTE THAT THE INFORMATION PAST THIS POINT IS GOOD UP TO VERSION 2025.8.5 DUE TO REDIS BEING REMOVED.

IN VERSIONS NEWER THAN 2025.8.5, REDIS IS REMOVED, AND I NEED TO FIGURE OUT HOW TO UPGRADE PROPERLY AND DOCUMENT IT.
{% endhint %}

### Example Docker Compose File to persist data in the directories created above

Edit this file if needed, with `nano docker-compose.yml` and paste the following into this file, or edit to your preference.

> This docker-compose.yml file also contains compose information for the Radius and LDAP Outposts.

> When creating these outposts in Authentik Admin Dashboard, I recommend setting them as `No Itegration` before activating them in the docker-compose.yml file.

{% hint style="warning" %}
THIS DOCKER COMPOSE FILE NEEDS TO BE UPDATED TO REMOVE REDIS
{% endhint %}

{% code title="docker-compose.yml" expandable="true" %}
```yml
# version: "3.4"

services:

  postgresql:
    image: docker.io/library/postgres:16-alpine
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
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2025.8.5}
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

########################################################################
##### CREATE THE OUTPOSTS BELOW IN AUTHENTIK FIRST!                #####
##### SET THEM AS `NO INTEGRATION`                                 #####
##### SELECTING DOCKER INTEGRATION WILL CREATE A DUPLICATE OUTPOST #####
##### GRAB THE TOKEN FROM THE OUTPOST INFORMATION.                 #####
##### PASTE INTO ENV FILE INTO APPROPRIATE LOCATION.               #####
##### UNCOMMENT OUTPOST TO ACTIVATE, RESTART AUTHENTIK.            #####
########################################################################

#  ldap_outpost:
#      image: ${AUTHENTIK_IMAGE_LDAP:-ghcr.io/goauthentik/ldap}:${AUTHENTIK_TAG:-2025.8.5}
#      restart: unless-stopped
#      env_file:
#        - .env
#      ports:
#      - "${COMPOSE_PORT_LDAP:-6389}:3389"
#      - "${COMPOSE_PORT_LDAPS:-6636}:6636"
#      environment:
#          AUTHENTIK_HOST: "${AUTHENTIK_HOST}"
#          AUTHENTIK_INSECURE: "${AUTHENTIK_INSECURE}"
#          AUTHENTIK_TOKEN: "${AUTHENTIK_LDAP_TOKEN}"

#  radius_outpost:
#    image: ${AUTHENTIK_IMAGE_RADIUS:-ghcr.io/goauthentik/radius}:${AUTHENTIK_TAG:-2025.8.5}
#    restart: unless-stopped
#    ports:
#      - "${COMPOSE_PORT_RADIUS:-1812}:1812"
#      - "${COMPOSE_PORT_ACCOUNTING:-1813}:1813"
#    env_file:
#      - .env
#    environment:
#      AUTHENTIK_HOST: "${AUTHENTIK_HOST}"
#      AUTHENTIK_INSECURE: "${AUTHENTIK_INSECURE}"
#      AUTHENTIK_TOKEN: "${AUTHENTIK_RADIUS_TOKEN}"

#  rac_outpost:
#      image: ${AUTHENTIK_IMAGE_RAC:-ghcr.io/goauthentik/rac}:${AUTHENTIK_TAG:-2025.8.5}
#        # Optionally specify the container's network, which must be able to reach the core authentik server.
#        # networks:
#        #   - foo
#      environment:
#        AUTHENTIK_HOST: "${AUTHENTIK_HOST}"
#        AUTHENTIK_INSECURE: "${AUTHENTIK_INSECURE}"
#        AUTHENTIK_TOKEN: "${AUTHENTIK_RAC_TOKEN}"

#######################################
##### END OF OUTPOST INTEGRATIONS #####
#######################################

  worker:
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2025.8.5}
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
{% endcode %}

### EXAMPLE Docker Environment Variables File (.env)

This is the `.env` file

{% hint style="warning" %}
THIS ENV FILE NEEDS TO BE UPDATED TO REMOVE REDIS.D
{% endhint %}

{% code title=".env" expandable="true" %}
```dotenv
##############################################################################################
### Default Authentik Environment Variables.                                               ###
### Be sure to name this file to .env and place in same location as docker compose file.   ###
### These env Variables came directly from Authentik's Documentation Website and were all  ###
### copied into this file. Some of these Variables may not apply to all setups.            ###
### Main settings required are left uncommented. You must look through this entire ENV     ###
### file to verify everything applies to your particular setup.                            ###
### Uncomment any lines below with a single hastag to match your situation                 ###
##############################################################################################
### If you had default Variables in this file,                  ###
### Such as `AUTHENTIK_SECRET_KEY`, `PG_PASS`, etc...           ###
### you MUST remove or comment out the matching Variables BELOW ###
### so it does not conflict with your setup!!                   ###
###################################################################

########################################
########## AUTHENTIK SETTINGS ##########
########################################

### Authentik Secret Key
### REQUIRED
AUTHENTIK_SECRET_KEY=THIS SHOULD HAVE BEEN GENERATED FROM THE PREVIOUS STEP!

### Result Backend Settings
# AUTHENTIK_RESULT_BACKEND__URL=

### Authentik Server Image and Version Number
### REQUIRED
AUTHENTIK_TAG=2025.8.5 ## <-- UPDATE THIS TO LATEST VERSION NUMBER!!! ##
AUTHENTIK_IMAGE=ghcr.io/goauthentik/server

### User Settings
AUTHENTIK_DEFAULT_USER_CHANGE_NAME=false
AUTHENTIK_DEFAULT_USER_CHANGE_EMAIL=false
AUTHENTIK_DEFAULT_USER_CHANGE_USERNAME=false

### GDPR Compliance Settings
AUTHENTIK_GDPR_COMPLIANCE=true

### Update Check Settings
# AUTHETNIK_DISABLE_UPDATE_CHECK=false

### Cookie Domain Settings
# AUTHENTIK_COOKIE_DOMAIN=

### Outpost Settings
# AUTHENTIK_OUTPOSTS__CONTAINER_IMAGE_BASE=
# AUTHENTIK_OUTPOSTS__DISCOVER=

### Reputation Expiry
# AUTHENTIK_REPUTATION_EXPIRY=86400

### Session Storage (allows cache or db)
# AUTHENTIK_SESSION_STORAGE=cache

### Worker Web Threads
# AUTHENTIK_WEB__THREADS=4
# AUTHENTIK_WORKER__CONCURRENCY=2

########################################
########## POSTGRES SETTINGS ###########
########################################

### Internal Postgres Server Settings
### REQUIRED
PG_USER=authentik
PG_PASS=THIS SHOULD HAVE BEEN AUTOMATICALLY GENERATED FROM THE PREVIOUS STEP

### External Postgres Server Settings
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

### External Postgres Read Only Replicas Settings
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__HOST=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__NAME=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__USER=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__PORT=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__PASSWORD=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__SSLMODE=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__SSLROOTCERT=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__SSLCERT=
# AUTHENTIK_POSTGRESQL__READ_REPLICAS__0__SSLKEY=

########################################
############ REDIS SETTINGS ############
########################################

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

### Authentik Channel Layer Settings
# AUTHENTIK_CHANNEL__URL=

### Broker Settings
# AUTHENTIK_BROKER__URL=
# AUTHENTIK_BROKER__TRANSPORT_OPTIONS=

########################################
############ CACHE SETTINGS ############
########################################

### Authentik Cache Settings
# AUTHENTIK_CACHE__URL=
# AUTHENTIK_CACHE__TIMEOUT=
# AUTHENTIK_CACHE__TIMEOUT_FLOWS=
# AUTHENTIK_CACHE__TIMEOUT_POLICIES=
# AUTHENTIK_CACHE__TIMEOUT_REPUTATION=

########################################
########### LISTEN SETTINGS ############
########################################

### Authentik Listen Settings (Set server address and Port number, eg 0.0.0.0:9000 0.0.0.0:9443)
### SET THESE TO THE PORTS YOU WANT TO USE FOR AUTHENTIK ###
COMPOSE_PORT_HTTP=80
COMPOSE_PORT_HTTPS=443

### Authentik LDAP Listen Settings (Set server address and Port number, eg 0.0.0.0:3389 0.0.0.0:6636)
### UNCOMMENT TO USE LDAP ###
# COMPOSE_PORT_LDAP=3389
# COMPOSE_PORT_LDAPS=6636

### Authentik Prometheus Metrics Listen Settings (Set server address and port number, eg 0.0.0.0:9300)
### UNCOMMENT TO USE PROMETHEUS METRICS ###
# COMPOSE_PORT_METRICS=9300

### Go Debugging Listen Settings (Set server address and port number, eg 0.0.0.0:9900
# AUTHENTIK_LISTEN__DEBUG=0.0.0.0:9900

### Trusted Proxies Listen Settings
### Defaults to 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, fe80::/10, ::1/128
# AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS=

#########################################
##### LDAP & RADIUS SHARED SETTINGS #####
#########################################

# AUTHENTIK_HOST="https://auth.your.domain/"
# AUTHENTIK_INSECURE="true"

########################################
############ LDAP SETTINGS #############
########################################

### LDAP Container Settings
# AUTHENTIK_IMAGE_LDAP=ghcr.io/goauthentik/ldap
# AUTHENTIK_LDAP_TOKEN=[GET THIS FROM YOUR OUTPOST DEPLOYMENT INFORMATION]

### LDAP Settings
# AUTHENTIK_LDAP__TASK_TIMEOUT_HOURS=
# AUTHENTIK_LDAP__PAGE_SIZE=
# AUTHENTIK_LDAP__TLS__CIPHERS=

########################################
########### RADIUS SETTINGS ############
########################################

### RADIUS Container Settings
# AUTHENTIK_IMAGE_RADIUS=ghcr.io/goauthentik/radius
# AUTHENTIK_RADIUS_TOKEN=[GET THIS FROM YOUR OUTPOST DEPLOYMENT INFORMATION]

### RADIUS Settings
# COMPOSE_PORT_RADIUS=1812
# COMPOSE_PORT_ACCOUNTING=1813

########################
##### RAC SETTINGS #####
########################

# AUTHENTIK_RAC_TOKEN=

########################################
########### STORAGE SETTINGS ###########
########################################

### Media Storage Settings
# AUTHENTIK_STORAGE__MEDIA__BACKEND=
# AUTHENTIK_STORAGE__MEDIA__S3__REGION=
# AUTHENTIK_STORAGE__MEDIA__S3__USE_SSL=
# AUTHENTIK_STORAGE__MEDIA__S3__ENDPOINT=
# AUTHENTIK_STORAGE__MEDIA__S3__SESSION_PROFILE=
# AUTHENTIK_STORAGE__MEDIA__S3__ACCESS_KEY=
# AUTHENTIK_STORAGE__MEDIA__S3__SECRET_KEY=
# AUTHENTIK_STORAGE__MEDIA__S3__SECURITY_TOKEN=
# AUTHENTIK_STORAGE__MEDIA__S3__BUCKET_NAME=
# AUTHENTIK_STORAGE__MEDIA__S3__CUSTOM_DOMAIN=
# AUTHENTIK_STORAGE__MEDIA__S3__SECURE_URLS=

########################################
############ GEOIP SETTINGS ############
########################################

### GeoIP Settings
### UNCOMMENT BOTH LINES BELOW TO USE GEOIP
# AUTHENTIK_EVENTS__CONTEXT_PROCESSORS__GEOIP=./geoip/GeoLite2-City.mmdb
# AUTHENTIK_EVENTS__CONTEXT_PROCESSORS__ASN=./geoip/GeoLite2-ASN.mmdb

########################################
########### LOGGING SETTINGS ###########
########################################

### Log Level Settings (Supports debug, info, warning, error, trace)
# AUTHENTIK_LOG_LEVEL=info

### Error Reporting Settings
AUTHENTIK_ERROR_REPORTING__ENABLED=true
# AUTHENTIK_ERROR_REPORTING__SENTRY_DSN=
# AUTHENTIK_ERROR_REPORTING__ENVIRONMENT=
# AUTHENTIK_ERROR_REPORTING__SEND_PII=

###############################################
############ EMAIL / SMTP SETTINGS ############
###############################################

AUTHENTIK_EMAIL__HOST=smtp.gmail.com
AUTHENTIK_EMAIL__PORT=587
AUTHENTIK_EMAIL__USERNAME=email@address.example
AUTHENTIK_EMAIL__PASSWORD=google-app-password
AUTHENTIK_EMAIL__USE_TLS=true
AUTHENTIK_EMAIL__USE_SSL=false
AUTHENTIK_EMAIL__TIMEOUT=10
AUTHENTIK_EMAIL__FROM=noreply@authentik.domain
```
{% endcode %}

### Example GEOIP Override file

Name this file `docker-compose.override.yml`

{% code title="docker-compose.override.yml" expandable="true" %}
```yml
version: "3.2"

services:
    server:
        volumes:
            - ./geoip:/geoip
    worker:
        volumes:
            - ./geoip:/geoip
    geoipupdate:
        image: "maxmindinc/geoipupdate:latest"
        restart: unless-stopped
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
{% endcode %}

***

## Launch and run Authentik

Run the following command to download and launch Authentik

```bash
docker-compose up -d
```

### Authentik User Setup

Navigate to

```html
https://auth.domain.example/if/flow/initial-setup/
```

or

```html
http://IP.ADDRESS.OF.AUTHENTIK:9000/if/flow/initial-setup/
```

This should ask you to setup your Authentik admin (if setup correctly)

***

### Initial Setup Flow Not Showing Up after creation.

If for some reason the initial setup flow doesn't show up, Authentik might have already created the user and deleted the initial setup flow automatically. If this happened to you, you should be able to gain access to the default Authentik Admin by using the following command by logging into the terminal of the host for Authentik.

* Login to root user of Proxmox LXC
* Navigate to `cd docker/authentik`
* Enter the following command:

```bash
docker-compose run --rm server create_recovery_key 1 akadmin
```

This should output a link that you can copy and paste into your web browser to login to the default Authentik Admin. Be sure to change the url to point to your local Authentik IP Address or the Domain name of your Authentik Instance before navigating to it, if it didn't generate correctly.

***

### Updating Authentik

Edit the `.env` file and update the `AUTHENTIK_TAG` to the latest version and then run `docker-compose down && docker-compose pull && docker-compose up -d` or just `docker-compose down && docker-compose up -d`.

***

Edit Docker env File

```bash
cd docker/authentik && nano .env
```

Restart Authentik

```bash
docker-compose down && docker-compose pull && docker-compose up -d
```

or

```bash
docker-compose down && docker-compose up -d
```

or if you prefer not to stop the container

```bash
docker-compose pull && docker-compose up -d
```

***

## Cloudflare Setup

1. Login to your Cloudflare Account.
2. Navigate to the DNS Records section of your domain you want attached to Authentik.
3. Create 3 Proxied DNS records.
   1. Set one `DNS A Record` that is set for `your domain` to your `Public IP Address`. (Root Domain (i.e. domain.example))
   2. Set one `CNAME Record` with an asterisk (`*`) for a wildcard with the destination of `@` for root domain. (Wildcard Entry)
   3. Set the last one as a `CNAME Record` for `auth` and destination of `@` for root domain. (Authentik)
4. In your Cloudflare Account, navigate to SSL/TLS > Overview
   1. Set your `Encryption Mode` to `Full (Strict)`
   2. (Optional) Enable `SSL/TLS Recommender`
5. Navigate to SSL/TLS > Edge Certificates
   1. (Recommended) Enable `Always Use HTTPS`
   2. Configure `HTTP Strict Transport Security (HSTS)`
      1. (Recommended) **Enable** `HSTS`
      2. (Recommended) `Set Max Age Header` to `6 Months`
      3. (Recommended) **Enable** `Apply HSTS Policy to subdomains`
      4. (Recommended) **Disable** `Preload`
      5. (Recommended) **Enable** `No-Sniff Header`
   3. Set `Minimum TLS Version` to `TLS 1.3`
   4. (Recommended) **Enable** `Opportunistic Encryption`
   5. **Enable** `TLS 1.3`
   6. (Recommended) **Enable** `Automatic HTTPS Rewrites`
6. Navigate to SSL/TLS > Origin Server
   1. Create an `Origin Certificate` if one does not exist already.
      1. If one exists, `Revoke` and `Create` a new one.
   2. Create your Certificate with `RSA (2048)`
   3. Your hostnames should include the wildcard ( \* ) entry and the root domain name at least.
   4. Choose your `Certificate Validity` Length
   5. Copy the contents of both boxes on the next screen into a word or text document temporarily. There should be a `Certificate Key` and a `Private Key`. **DO NOT EVER SHARE THIS INFORMATION WITH ANYONE, IT IS THE KEY TO YOUR DOMAIN CONNECTED TO CLOUDFLARE**

***

## Authentik Certificate Setup

1. Login to your Authentik Admin Account
2. Navigate to `System > Certificates`
   1. Click on `Create` to Import the Cloudflare Origin Certificate we just created.
   2. Name the Certificate whatever you want
   3. Paste the `Certificate Key` into the `Certificate` box
   4. Paste the `Private Key` into the `Private Key` box
   5. Click `Create`
3. Navigate to `System > Brands`
   1. Click the `Edit` button under `Actions`
   2. Scroll to the bottom of the Window and `Expand Other Global Settings`
   3. Under `Web Certificate`, choose your Cloudflare Certificate we just imported.
   4. Click `Update`
4. Navigate to `Applications > Outposts`
   1. Click the `Edit` button under `Actions`
   2. Scroll to the bottom and `Expand Advanced Settings`
      1. Make sure your `authentik_host:` is set to the CNAME you created in Cloudflare. (i.e. `https://auth.domain.example`)
   3. Click `Update`

***

### Conclusion

If everything went according to plan, the Authentik container will persist all data for Authentik under the `docker/authentik` directory for `certs`, `custom-templates`, `database`, `geoip`, `media` and `redis`. This will make it much easier to upgrade Authentik in the future. This should also enable HTTPS connections to Authentik and allow the use of a custom Cloudflare Origin Certificate using Cloudflare's Strict SSL mode with other Cloudflare security measures enabled.

***

### Application and Provider Setup

Please refer to [Authentik Application and Provider Setup](applications-and-providers.md)
