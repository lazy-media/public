# Nextcloud OAuth / OpenID Setup with Authentik

## Documentation

- [Authentik Documentation](https://docs.goauthentik.io/integrations/services/nextcloud/)

## Assumptions

- This guide assumes you have Nextcloud setup and running. Depening on your Nextcloud Setup and instance, your URL might be different.
- Your Nextcloud can either have ```index.php``` or not in the url. Please adjust these to your preference or requirements.
- This guide uses the Nextcloud installed via the SNAP Store on Ubuntu Server 22.04

## Requirements

- Make sure you have the App `OpenID Connect user backend` installed on Nextcloud

## Nextcloud Setup

- Login to Nextcloud Admin Account
- Navigate to Apps
- Install `OpenID Connect user backend` if needed
- After installation, Navigate to `Administration Settings > OpenID Connect`
- Add a New Provider by click the Plus Icon
- Fill out the Form as Follows:

Identifier = `YOUR DISPLAY NAME SHOWN ON NEXTCLOUD LOGIN`
Client ID = `YOUR AUTHENTIK PROVIDER CLIENTID`
Client Secret = `YOUR AUTHENTIK PROVIDER SECRET KEY`
Discover Endpoint = `https://YOUR-AUTHENTIK-URL/application/o/YOUR-PROVIDER-SLUG/.well-known/openid-configuration`
Scope = `email` `profile` `openid` `ak_proxy`
User ID Mapping = `sub`
Quota Mapping = `quota`
Groups Mapping = `groups`
Use Unique User ID = `False / Unchecked`
Use Group Provisioning = `True / Checked`
Send ID Token hint on logout = `True / Checked`

At the bottom with the check boxes

Use Unique user id = `UNCHECKED`
Use Provider Identifier as prefix for ids = `UNCHECKED`
Use Group Provisioning = `CHECKED`
(OPTIONAL) Check Bearer Token on API and WebDav with Bearer Token = `Checked / Unchecked`
(OPTIONAL) Auto Provision User when Accessing API and WebDav with Bearer Token = `Checked / Unchecked`
Send ID Token hint on logout = `CHECKED`


## Authentik Setup for Nextcloud Quota

