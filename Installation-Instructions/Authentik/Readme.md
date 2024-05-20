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

### (Optional) Create Authentik Machine User
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

## Authentik Setup

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

[Example Docker Compose File for Persistant Data](Installation-Instructions/Authentik/docker-compose.yml)

## EXAMPLE Docker Environment Variables File (.env)
This is the `.env` file

[Example Docker Compose Environment Variables File](Installation-Instructions/Authentik/docker-compose.env.yml)

## Example GEOIP Override file
Name this file `docker-compose.override.yml`

[Example Docker Compose Override File for GeoIP](Installation-Instructions/Authentik/docker-compose.override.yml)

# Launch and run Authentik

Run the following command to download and launch Authentik

```
docker-compose up -d
```

## Authentik User Setup
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

## Updating Authentik

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

# Cloudflare Setup

1. Login to your Cloudflare Account.
2. Navigate to the DNS Records section of your domain you want attached to Authentik.
3. Create 3 Proxied DNS records.
    - Set one `DNS A Record` that is set for `your domain` to your `Public IP Address`. (Root Domain (i.e. domain.example))
    - Set one `CNAME Record` with an asterisk (`*`) for a wildcard with the destination of `@` for root domain. (Wildcard Entry)
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

## Application and Provider Setup

Please refer to [Authentik Application and Provider Setup](Authentik/Applications-&-Providers/Readme.md)
