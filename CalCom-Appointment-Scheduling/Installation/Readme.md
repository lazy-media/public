# Introduction

> This documentation is still being revised. USE AT OWN RISK!

I made this documentation because I could not find enough information on how to set this up correctly to work with certain things I wanted to work. After doing a lot of research and digging online, I was able to figure some of this out. This documentation is only for reference.

> ## NOTICE:
> If you want the full functionality of this program, it takes up A LOT of space. I gave this a 100 GB ssd and it took up almost half just to run everything I have figured out in this guide.

## Referenced Documentation

- [Awesome Open Source YouTube Video](https://www.youtube.com/watch?v=Niep6YkrkXA)

- [Cal.com Official Documentation](https://cal.com/docs/self-hosting/docker)

- [Cal.com GitHub Documentation (Followed this for Install)](https://github.com/calcom/docker)

- [Google Integration](https://cal.com/docs/self-hosting/apps/install-apps/google)

- [Stripe Proper ENV Vars Location](https://github.com/calcom/cal.com/issues/11582#issuecomment-1742909210)

- [Stripe Integration Bug Fix](https://github.com/calcom/cal.com/issues/9699#issuecomment-1606171203)

- [API - Some useful information found here](https://github.com/calcom/cal.com/discussions/19313)

## Assumptions

- You have a fresh copy of Ubuntu Server 24.04 installed on a VM or LXC or whatever you choose.
- You have `docker` and `docker compose` installed
- You are using the files provided in this documentation (if you want the best results)

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

> Edit your .env file to fit your needs. Use the examples as a reference.

### Build CalCom

- Change directories (if not already) into the root calcom directory.

- Pull docker images with
```
docker compose pull
```

- Start the database server
```
docker compose up -d database
```

- Run
```
docker compose up --build
```
  - Let this run


## Example Docker Compose File

- [Example docker-compose.yml file](docker-compose.yml)


## ENV Example File

Use the following example file as a starting point. Be sure to change what is needed for it to fit your needs.

- [Example .env File](.env)

## Example `.env.appStore` File

This file is needed for some integrations to work correctly, like Google and Stripe.

- [Example .env.appStore File](.env.appStore)

## Stripe Setup

This will help you with getting the proper keys for Stripe Integration

### Getting Stripe Private & Public API Keys

<details>
<summary>How to get the Stripe Public Key</summary>

- Navigate to [Stripe API Keys Dashboard](https://dashboard.stripe.com/apikeys)
  - You should see a `Publishable Key` with the token starting with `pk_live_`
  - Copy this key and paste it into the `.env` and `.env.appStore` files for `NEXT_PUBLIC_STRIPE_PUBLIC_KEY=`

- On the same Stripe page, we are going to get a Private Key
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

- Open Your Cal.com site and go to Apps. Find and Install Stripe.

## Google OAuth Setup

> I recommend you follow the directions on the main website found [here](https://cal.com/docs/self-hosting/apps/install-apps/google). 

> I will update this section at a later date, as the official documentation is good enough for this section.

## Nextcloud Talk Setup

> Still trying to figure this out.

## OpenID / OAuth Setup

> ### MUST HAVE A COMMERCIAL SUBSCRIPTION FOR THIS TO WORK!

> Visit the link [Cal.com Self Hosted - Purchase Commercial License](http://go.cal.com/self-hosted) to purchase a 7-day Free Trial and a commercial License Key.

> You will receive your keys needed after sucessful purchase.

Your keys should look like:

```yml
CALCOM_LICENSE_KEY=
CAL_SIGNATURE_TOKEN=
CALCOM_PRIVATE_API_ROUTE=
```

- Copy these and paste them at the bottom of your `.env` file.

- Save the file and restart calcom.

- Open Calcom in your web browser and navigate to `Settings > Single sign-on`

- You should now see options for `SSO with OIDC` or `SSO with SAML`.

---

## Authentik Basic OpenID / OAuth Setup

> To learn how to setup an OpenID/OAuth Provider with Authentik, click [here](/Authentik/Applications-&-Providers/Readme.md#authentik-basic-oauth2openid-setup)