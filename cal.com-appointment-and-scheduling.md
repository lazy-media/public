---
description: >-
  Information on how to install and setup a Self Hosted Version of Cal.com
  Scheduling.
---

# Cal.com Appointment & Scheduling

## Cal.com Appointment & Scheduling

### Introduction

> This documentation is still being revised. USE AT OWN RISK!

I made this documentation because I could not find enough information on how to set this up correctly to work with certain things I wanted to work. After doing a lot of research and digging online, I was able to figure some of this out. This documentation is only for reference.

> **NOTICE:**
>
> If you want the full functionality of this program, it takes up A LOT of space. I gave this a 100 GB ssd and it took up almost half just to run everything I have figured out in this guide.

#### Referenced Documentation

* [Awesome Open Source YouTube Video](https://www.youtube.com/watch?v=Niep6YkrkXA)
* [Cal.com Official Documentation (Followed this for Install)](https://cal.com/docs/self-hosting/docker)
* [Cal.com GitHub Documentation](https://github.com/calcom/docker)
* [Google Integration](https://cal.com/docs/self-hosting/apps/install-apps/google)
* [Stripe Proper ENV Vars Location](https://github.com/calcom/cal.com/issues/11582#issuecomment-1742909210)
* [Stripe Integration Bug Fix](https://github.com/calcom/cal.com/issues/9699#issuecomment-1606171203)
* [API - Some useful information found here](https://github.com/calcom/cal.com/discussions/19313)

#### Assumptions

* You have a fresh copy of Ubuntu Server 24.04 installed on a VM or LXC or whatever you choose.
* You have `docker` and `docker compose` installed
* You are using the files provided in this documentation (if you want the best results)

***

### Cal.com Installation

#### Prerequisites

1. Docker and Docker Compose already installed
2. Fresh install of Ubuntu Server 24.04
3. You already have a way to remote into this machine or ssh into it.

***

#### Installation

> Recommend following official Documentation for install, if different from this documentation.

**Clone Cal.com GitHub Repository**

```
git clone --recursive https://github.com/calcom/docker.git calcom-docker
```

**Change into new directory**

```
cd docker
```

**Prepare Configuration and ENV File**

```
cp .env.example .env
```

> Edit your .env file to fit your needs. Use the examples as a reference.

**Errors**

> I was personally getting errors when running the build command below saying it was missing files. Since I had a previous working copy, I copied the files from that config.

The files that were needed were:

{% tabs %}
{% tab title="git-init.sh" %}
```sh
#!/bin/sh
# Skip if `.gitmodules` exists
[ -f .gitmodules ] && {
  echo ".gitmodules already initialized"
  exit 0
}

./git-setup.sh website console
```
{% endtab %}

{% tab title="git-setup.sh" %}
{% code expandable="true" %}
```sh
#!/bin/sh
# If no project name is given
if [ $# -eq 0 ]; then
  # Display usage and stop
  echo "Usage: git-setup.sh <console,website>"
  exit 1
fi
# Get remote url to support either https or ssh
remote_url=$(echo $(git config --get remote.origin.url) | sed 's![^/]*$!!')
# Loop through the requested modules
for module in "$@"; do
  echo "Setting up '$module' module..."
  # Set the project git URL
  project=$remote_url$module.git
  # Check if we have access to the module
  if [ "$(git ls-remote "$project" 2>/dev/null)" ]; then
    echo "You have access to '${module}'"
    # Create the .gitmodules file if it doesn't exist
    ([ -e ".gitmodules" ] || touch ".gitmodules") && [ ! -w ".gitmodules" ] && echo cannot write to .gitmodules && exit 1
    # Prevents duplicate entries
    git config -f .gitmodules --unset-all "submodule.apps/$module.branch"
    # Add the submodule
    git submodule add --force $project "apps/$module"
    
    # Determine the branch based on module
    branch="main"
    if [ "$module" = "website" ]; then
      branch="production"
    fi

    # Set the default branch
    git config -f .gitmodules --add "submodule.apps/$module.branch" ${branch}
    
    # Update to the latest of branch in that submodule
    cd apps/$module && git pull origin ${branch} && cd ../..

    # We forcefully added the subdmoule which was in .gitignore, so unstage it.
    git restore --staged apps/$module
  else
    echo "You don't have access to: '${module}' module."
  fi
done
git restore --staged .gitmodules

```
{% endcode %}
{% endtab %}
{% endtabs %}

**Build CalCom**

* Change directories (if not already) into the root calcom directory.
* Pull docker images with

```
docker compose pull
```

* Start the database server

```
docker compose up -d database
```

* Run

```
docker compose up --build
```

* Let this run

***

#### Example Docker Compose File

{% code expandable="true" %}
```yml
# file location: root directory of calcom docker (etc. /home/user/docker/docker-compose.yml)

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
# Uncomment all the lines below until END SECTION if you want to enable this.
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
{% endcode %}

***

#### ENV Example File

Use the following example file as a starting point. Be sure to change what is needed for it to fit your needs.

```dotenv
THIS WILL BE FILLED IN AT A LATER TIME!!!
```

***

#### Example `.env.appStore` File

This file is needed for some integrations to work correctly, like Google and Stripe.

```dotenv
# file location: root directory of calcom docker (etc. /home/user/docker/.env.appStore)

{GOOGLE OAUTH JSON FILE CONTENTS}

NEXT_PUBLIC_STRIPE_PUBLIC_KEY=
STRIPE_PRIVATE_KEY=
STRIPE_CLIENT_ID=
STRIPE_WEBHOOK_SECRET=
```

***

#### Stripe Setup

This will help you with getting the proper keys for Stripe Integration

**Getting Stripe Private & Public API Keys**

<details>

<summary>How to get the Stripe Public Key</summary>

* Navigate to [Stripe API Keys Dashboard](https://dashboard.stripe.com/apikeys)
  * You should see a `Publishable Key` with the token starting with `pk_live_`
  * Copy this key and paste it into the `.env` and `.env.appStore` files for `NEXT_PUBLIC_STRIPE_PUBLIC_KEY=`
* On the same Stripe page, we are going to get a Private Key
  * In the `Standard Keys` Section, click on `Create Secret Key` in the top right
  * Select `Building your own integration`, and click `Create Secret Key`
  * Give the Key a name like `Calcom Integration`
  * Copy this Private key, it should start with `sk_live_`
  * Paste this into the `.env` and `.env.appStore` files for `STRIPE_PRIVATE_KEY`

</details>

**How to get Stripe Client ID**

<details>

<summary>How to get Stripe Client ID</summary>

* Navigate to [Stripe Connected Accounts Dashboard](https://dashboard.stripe.com/connect/accounts)
  * **If this is not already setup, YOU need to set this up according to your company, business or individual use case. I cannot recommend on how to set this up.**
  * If you need to set this up, come back after you are done.
* Click on `+Create` in the top right corner.
  * Verify information is correct in the pop-up.
* Click on `Create` in the bottom right corner
* Copy the given created `setup` link, and open in a browser window.
  * I recommend opening an incognito window to complete this, but it's your choice.
  * Go through the setup of the integration to your needs.
  * Again, I cannot recommend how to set this up as it pertains to your use case.
* Navigate to [Stripe Connect Onboarding OAuth Settings](https://dashboard.stripe.com/settings/connect/onboarding-options/oauth)
  * Make sure to `Enable OAuth` if it is not already.
  * Under the `Redirects` section, enter in `https://calcom.example.com/api/integrations/stripepayment/callback`, changing the domain as needed.
  * Find `Live Client ID`, it should start with `ca_`, copy this.
  * Paste this into the `.env` and `.env.appStore` files for `STRIPE_CLIENT_ID`.

</details>

**How to get Stripe Webhook Key**

<details>

<summary>How to get Stripe Webhook Key</summary>

* Navigate to [Stripe Developer Dashboard](https://dashboard.stripe.com/webhooks)
  * Click on `+ Add Endpoint` in the top right corner.
  * For Enpoint URL, enter in `https://calcom.example.com/api/integrations/stripepayment/webhook`, changing the domain as needed.
  * For `Events to Listen to`, select all of them.
  * Click `Create`
* You should now see the webhook listed on the main [Stripe Webhooks Dashboard](https://dashboard.stripe.com/webhooks).
  * Click on it to view information about it.
  * Under the Webhook URL displayed at the top of the page, you should see `Signing Secret`, click to Reveal.
  * The secret should start with `whsec_`, copy this.
  * Paste this into the `.env` and `.env.appStore` files for `STRIPE_WEBHOOK_SECRET`

</details>

**Complete Stripe Setup**

* Save the file and do a `docker compose down && docker compose up -d` to restart calcom, or restart it how you restart it.
* Open Your Cal.com site and go to Apps. Find and Install Stripe.

***

#### Google OAuth Setup

> I recommend you follow the directions on the main website found [here](https://cal.com/docs/self-hosting/apps/install-apps/google).

> I will update this section at a later date, if I see fit, as the official documentation is good enough.

***

#### Nextcloud Talk Setup

> Still trying to figure this out.

***

#### OpenID / OAuth Setup

> **MUST HAVE A COMMERCIAL SUBSCRIPTION FOR THIS TO WORK!**

> Visit the link [Cal.com Self Hosted - Purchase Commercial License](http://go.cal.com/self-hosted) to purchase a 7-day Free Trial and a commercial License Key.

> You will receive your keys needed after sucessful purchase.

Your keys should look like:

```yml
CALCOM_LICENSE_KEY=
CAL_SIGNATURE_TOKEN=
CALCOM_PRIVATE_API_ROUTE=
```

* Copy these and paste them at the bottom of your `.env` file.
* Save the file and restart calcom.
* Open Calcom in your web browser and navigate to `Settings > Single sign-on`
* You should now see options for `SSO with OIDC` or `SSO with SAML`.

***

#### Authentik Basic OpenID / OAuth Setup

> To learn how to setup an OpenID/OAuth Provider with Authentik, click here
