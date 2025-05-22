# Introduction

> This documentation is still being revised.

I made this documentation because I could not find enough information on how to set this up correctly to work with certain things I wanted to work. After doing a lot of research and digging online, I was able to figure some of this out. This documentation is only for reference.

# Referenced Documentation

- [Awesome Open Source YouTube Video](https://www.youtube.com/watch?v=Niep6YkrkXA)

- [Cal.com Official Documentation](https://cal.com/docs/self-hosting/docker)

- [Cal.com GitHub Documentation (Followed this for Install)](https://github.com/calcom/docker)

- [Google Integration](https://cal.com/docs/self-hosting/apps/install-apps/google)

- [Stripe Proper ENV Vars Location](https://github.com/calcom/cal.com/issues/11582#issuecomment-1742909210)

- [Stripe Integration Bug Fix](https://github.com/calcom/cal.com/issues/9699#issuecomment-1606171203)


# Cal.com Installation

## Prerequisites

> Docker and Docker Compose already installed

> Fresh install of Ubuntu Server 24.04

> You already have a way to remote into this machine or ssh into it.

## Installation

> Recommend following official Documentation for install, if different from this documentation.

### Clone Cal.com GitHub Repository

```
git clone --recursive https://github.com/calcom/docker.git calcom-docker
```

### Change into new directory

```
cd docker
```

### Prepare Configuration and ENV File

```
cp .env.example .env
```

### Example Docker Compose File

- [docker-compose.yml file](docker-compose.yml)

<details>
<summary>Example Docker Compose File</summary>

```
# Use postgres/example user/password credentials

networks:
  stack:
    name: stack
    external: false

services:
  database:
    container_name: database
    image: postgres
    restart: always
    ports:
      - 5432:5432
    volumes:
      - ./database-data:/var/lib/postgresql/data/
    env_file: .env
    networks:
      - stack

  calcom:
    image: calcom.docker.scarf.sh/calcom/cal.com
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_WEBAPP_URL: ${NEXT_PUBLIC_WEBAPP_URL}
        NEXT_PUBLIC_API_V2_URL: ${NEXT_PUBLIC_API_V2_URL}
        NEXT_PUBLIC_LICENSE_CONSENT: ${NEXT_PUBLIC_LICENSE_CONSENT}
        CALCOM_TELEMETRY_DISABLED: ${CALCOM_TELEMETRY_DISABLED}
        NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
        CALENDSO_ENCRYPTION_KEY: ${CALENDSO_ENCRYPTION_KEY}
        DATABASE_URL: ${DATABASE_URL}
        DATABASE_DIRECT_URL: ${DATABASE_URL}
        SAML_DATABASE_URL: ${DATABASE_URL_SAML}
      network: stack
    restart: always
    networks:
      - stack
    ports:
      - 3000:3000
    env_file: .env
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
      - DATABASE_DIRECT_URL=${DATABASE_URL}
      - SAML_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
    depends_on:
      - database

# Optional use of Prisma Studio. In production, comment out or remove the section below to prevent unwanted access to your database.
#  studio:
#    image: calcom.docker.scarf.sh/calcom/cal.com
#    restart: always
#    networks:
#      - stack
#    ports:
#      - 5555:5555
#    env_file: .env
#    environment:
#      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
#      - DATABASE_DIRECT_URL=${DATABASE_URL}
#      - SAML_DATABASE_URL=${DATABASE_URL_SAML}
#    depends_on:
#      - database
#    command:
#      - npx
#      - prisma
#      - studio
# END SECTION: Optional use of Prisma Studio.

```
</details>


### ENV Example File

Use the following example file as a starting point. Be sure to change what is needed for it to fit your needs.

- [.env File](.env)

<details>
    <summary>Cal.com Example ENV File</summary>
        
```
# Set this value to 'agree' to accept our license:
# LICENSE: https://github.com/calendso/calendso/blob/main/LICENSE
#
# Summary of terms:
# - The codebase has to stay open source, whether it was modified or not
# - You can not repackage or sell the codebase
# - Acquire a commercial license to remove these terms by emailing: license@cal.com
NEXT_PUBLIC_LICENSE_CONSENT=true
LICENSE=agree

# BASE_URL and NEXT_PUBLIC_APP_URL are both deprecated. Both are replaced with one variable, NEXT_PUBLIC_WEBAPP_URL
# BASE_URL=http://localhost:3000
# NEXT_PUBLIC_APP_URL=http://localhost:3000

NEXT_PUBLIC_WEBAPP_URL=https://YOUR.CALCOM.DOMAIN.URL
NEXT_PUBLIC_API_V2_URL=https://YOUR.CALCOM.DOMAIN.URL/api/v2

# Configure NEXTAUTH_URL manually if needed, otherwise it will resolve to {NEXT_PUBLIC_WEBAPP_URL}/api/auth
# NEXTAUTH_URL=http://localhost:3000/api/auth

# It is highly recommended that the NEXTAUTH_SECRET must be overridden and very unique
# Use `openssl rand -base64 32` to generate a key
NEXTAUTH_SECRET=0BTFdtG8UOEemV53WZj/VYfd5Wa3NhuA4E2sclSpoFk=

# Encryption key that will be used to encrypt CalDAV credentials, choose a random string, for example with `dd if=/dev/urandom bs=1K count=1 | md5sum`
CALENDSO_ENCRYPTION_KEY=ac88411e4b1245453d7d8e7eafe25041

# WEBHOOK
CALCOM_WEBHOOK_SECRET=580/fwdH8B7u0UP3NCI5oYobxWhYUDu+ylWYq4kcSn4=
CALCOM_WEBHOOK_HEADER_NAME=calcom-lazymedia

# ENDPOINT SYNC
# CALCOM_CREDENTIAL_SYNC_ENDPOINT=
# CALCOM_APP_CREDENTIAL_ENCRYPTION_KEY=


# Postgres Information
POSTGRES_USER=calcom
POSTGRES_PASSWORD=x95jbBhY8PXq28cji8667ahajhfjLHHDS086y97HhySHd
POSTGRES_DB=calcom
POSTGRES_DB_SAML=calcomsaml
DATABASE_HOST=192.168.25.94:5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
DATABASE_URL_SAML=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
# Needed to run migrations while using a connection pooler like PgBouncer
# Use the same one as DATABASE_URL if you're not using a connection pooler
DATABASE_DIRECT_URL=${DATABASE_URL}

# Google Integration
GOOGLE_LOGIN_ENABLED=false
GOOGLE_API_CREDENTIALS={GOOGLE API JSON FILE CONTENTS}

# Stripe Integration
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=STRIPE PUBLIC KEY
STRIPE_PRIVATE_KEY=STRIPE PRIVATE KEY
STRIPE_CLIENT_ID=STRIPE CONNECT CLIENT ID
STRIPE_WEBHOOK_SECRET=STRIPE WEBHOOK SECRET
PAYMENT_FEE_FIXED=100
PAYMENT_FEE_PERCENTAGE=10

# Set this to '1' if you don't want Cal to collect anonymous usage
CALCOM_TELEMETRY_DISABLED=1

# Used for the Office 365 / Outlook.com Calendar integration
# MS_GRAPH_CLIENT_ID=
# MS_GRAPH_CLIENT_SECRET=

# Used for the Zoom integration
ZOOM_CLIENT_ID=ZOOM OAUTH CLIENT ID
ZOOM_CLIENT_SECRET=ZOOM OAUTH CLIENT SECRET

# SAML DATABASE SETTINGS
# SAML_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}/${POSTGRES_DB}
# SAML_ADMINS=email1@example.com,email2@example.com

# E-mail settings
# Configures the global From: header whilst sending emails.
EMAIL_FROM_NAME=
EMAIL_FROM=

# Configure SMTP settings (@see https://nodemailer.com/smtp/).
EMAIL_SERVER_HOST=smtp.gmail.com
EMAIL_SERVER_PORT=587
EMAIL_SERVER_USER=
EMAIL_SERVER_PASSWORD=

NODE_ENV=production

```
</details>

### Example `.env.appStore` File

This file is needed for some integrations to work correctly, like Google and Stripe.

- [.env.appStore File](.env.appStore)

<details>
<summary>Example .env.appStore File</summary>

```
{GOOGLE OAUTH JSON FILE CONTENTS}

NEXT_PUBLIC_STRIPE_PUBLIC_KEY=
STRIPE_PRIVATE_KEY=
STRIPE_CLIENT_ID=
STRIPE_WEBHOOK_SECRET=

```

</details>

---

## Stripe Setup

This will help you with getting the proper keys for Stripe Integration

### Getting Stripe API Keys

<details>
<summary>How to get the Stripe Public Key</summary>

- Navigate to [Stripe API Keys Dashboard](https://dashboard.stripe.com/apikeys)
  - You should see a `Publishable Key` with the token starting with `pk_live_`
  - Copy this key and paste it into the `.env` and `.env.appStore` files for `NEXT_PUBLIC_STRIPE_PUBLIC_KEY=`

- On the same screen, we are going to get a Private Key
  - In the `Standard Keys` Section, click on `Create Secret Key` in the top right
  - Select `Building your own integration`, and click `Create Secret Key`
  - Give the Key a name like `Calcom Integration`
  - Copy this Private key, it should start with `sk_live_`
  - Paste this into the `.env` and `.env.appStore` files for `STRIPE_PRIVATE_KEY`

</details>

### How to get Stripe Client ID

<details>
<summary>How to get Stripe Client ID</summary>

- Navigate to [Stripe Connected Accounts Dashboard](https://dashboard.stripe.com/connect/accounts)
  - **If this is not already setup, YOU need to set this up according to your company, business or individual use case. I cannot recommend on how to set this up.**
  - If you need to set this up, come back after you are done.
- Click on `+Create` in the top right corner.
  - Verify information is correct in the pop-up.
- Click on `Create` in the bottom right corner
- Copy the given created `setup` link, and open in a browser window.
  - I recommend opening an incognito window to complete this, but it's your choice.
  - Go through the setup of the integration to your needs.
  - Again, I cannot recommend how to set this up as it pertains to your use case.
- Navigate to [Stripe Connect Onboarding OAuth Settings](https://dashboard.stripe.com/settings/connect/onboarding-options/oauth)
  - Make sure to `Enable OAuth` if it is not already.
  - Under the `Redirects` section, enter in `https://calcom.example.com/api/integrations/stripepayment/callback`, changing the domain as needed.
  - Find `Live Client ID`, it should start with `ca_`, copy this.
  - Paste this into the `.env` and `.env.appStore` files for `STRIPE_CLIENT_ID`.

</details>

### How to get Stripe Webhook Key

<details>
<summary>How to get Stripe Webhook Key</summary>

- Navigate to [Stripe Developer Dashboard](https://dashboard.stripe.com/webhooks)
  - Click on `+ Add Endpoint` in the top right corner.
  - For Enpoint URL, enter in `https://calcom.example.com/api/integrations/stripepayment/webhook`, changing the domain as needed.
  - For `Events to Listen to`, select all of them.
  - Click `Create`
- You should now see the webhook listed on the main [Stripe Webhooks Dashboard](https://dashboard.stripe.com/webhooks).
  - Click on it to view information about it.
  - Under the Webhook URL displayed at the top of the page, you should see `Signing Secret`, click to Reveal.
  - The secret should start with `whsec_`, copy this.
  - Paste this into the `.env` and `.env.appStore` files for `STRIPE_WEBHOOK_SECRET`

</details>


### Complete Stripe Setup

- Save the file and do a `docker compose down && docker compose up -d` to restart calcom, or restart it how you restart it.

- Open Cal.com site and go to Apps. Find and Install Stripe.

## Google OAuth Setup

> I recommend you follow the directions on the main website found [here](https://cal.com/docs/self-hosting/apps/install-apps/google). 

> I will update this section at a later date, as the official documentation is good enough for this section.

## Nextcloud Talk Setup

Still trying to figure this out.

## OpenID / OAuth Setup

> ### MUST HAVE A COMMERCIAL SUBSCRIPTION FOR THIS TO WORK!

> Visit this link [Cal.com Self Hosted - Purchase Commercial License](http://go.cal.com/self-hosted) to purchase a 7-day Free Trial and a commercial License Key.

> You will receive your keys needs after sucessful purchase.

Your keys should look like:

```
CALCOM_LICENSE_KEY=
CAL_SIGNATURE_TOKEN=
CALCOM_PRIVATE_API_ROUTE=
```

Copy these and paste them at the bottom of your `.env` file.

Save the file and restart calcom.

Open Calcom in your web browser and navigate to `Settings > Single sign-on`

You should now see options for `SSO with OIDC` or `SSO with SAML`.