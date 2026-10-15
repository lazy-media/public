---
description: Information on how to setup Nextcloud OpenID / OAuth with Authentik.
---

# Nextcloud

## Nextcloud OAuth / OpenID Setup with Authentik

### Documentation

* [Authentik Documentation](https://docs.goauthentik.io/integrations/services/nextcloud/)

### Purpose

This helps walk you through on how to setup Authentik as an OpenID provider and make Nextcloud use Authentik as a Login Method. This will also use a Property Mapping to control the amount of storage a user has assigned using Authentik User Attribute Settings. This also allows Nextcloud to know the Authentik Admin user and assign the proper Nextcloud Admin group to allow Administrative access to your Authentik Admin.

### Assumptions

* This guide assumes you have Nextcloud setup and running. Depening on your Nextcloud Setup and instance, your URL might be different.
* Your Nextcloud can either have `index.php` or not in the url. Please adjust these to your preference or requirements.
* This guide uses the Nextcloud version installed via the SNAP Store on Ubuntu Server 22.04

### Requirements

* Make sure you have the App `OpenID Connect user backend` installed on Nextcloud.
  * This can be found at:
    * Login to Nextcloud Admin Account
    * Click on User Icon in top right corner
    * Click on `+ Apps`
    * In the list on the left, select `Integration`
    * Find `OpenID Connect User Backend` and click `Download and Enable`
* Do not have the `Group Quota` or `User Quota` apps installed on Nextcloud as Authentik will handle storage quota's.

***

## Nextcloud Custom Scope Setup

### Authentik Nextcloud Scope Mapping Setup

**This Scope mapping adds Authentik Admins to the Nextcloud Admin Group and Assigns User or Group Storage Quotas**

* Login to Authentik Admin Portal
* Navigate to `Customization > Property Mappings`
* Create a new Property Mapping
  * Create a `Scope Mapping`
  * Enter a Name such as `Nextcloud Quota`
  * Enter Scope Name as `nextcloud` (This links this to the scope `nextcloud` in the Nextcloud OpenID Scope Settings below)
  * (optional) Enter a Description
  * In the Expression Field copy and paste the code below

```
# Extract all groups the user is a member of
groups = [group.name for group in user.ak_groups.all()]

# Nextcloud admins must be members of a group called "admin".
# This is static and cannot be changed.
# We append a fictional "admin" group to the user's groups if they are an admin in authentik.
# This group would only be visible in Nextcloud and does not exist in authentik.
if user.is_superuser and "admin" not in groups:
    groups.append("admin")

return {
    "name": request.user.name,
    "groups": groups,
    # To set a quota set the "nextcloud_quota" property in the user's attributes
    "quota": user.group_attributes().get("nextcloud_quota", None)
}
```

* Click `Finish` to Save

### Authentik Nextcloud User or Group Quota Setup

* Login to Authentik Admin Panel
* Navigate to `Directory > Users` or `Directory > Groups`
* Click the `Edit` icon under `Actions` for a user or group you want to restrict the storage amount for
  * Locate the `Attributes` box for the user or group
  * Enter in `nextcloud_quota: 10GB`
    * Where `10GB` is, you can change this to the amount of storage you want to assign to the user. Change the `10` to the amount followed by the size type below with no space between.
    * Use `MB` for Megabytes
    * Use `GB` for Gigabytes
    * Use `TB` for Terabytes

***

## Authentik OAuth / OpenID Setup

* Login to Authentik Admin Panel
* Navigate to `Applications > Providers`
* Create a New Provider
  * Create an `OAuth2/OpenID Provider`
  * Enter a Name of your choosing
  * Leave `Authentication Flow` empty
  * Authorization Flow is set as either Implicit or Explicit
    * Implicit should not ask the user for confirmation before logging into the site in question.
    * Explicit will force the user to confirm the login request before logging in to the site in question.
  * Client Type should be `Confidential`
  * **Copy** the `Client ID` and the `Secret Key` in to a document temporarily
  * Enter the `Redirect URI` as `https://YOUR-NEXTCLOUD-URL/index.php/apps/user_oidc/code` or `https://YOUR-NEXTCLOUD-URL/apps/user_oidc/code` (depending on your installation)
  * Choose a Signing Key (I selected the Cloudflare Certificate we imported during [Authentik Installation](https://github.com/lazy-media/public/blob/main/Authentik/Authentik-Installation/README.md#cloudflare-setup))
  * **Expand** `Advanced Protocol Settings` and scroll down to `Scopes`
    * Make sure the `nextcloud` (scope we just created), `authentik default OAuth Mapping: OpenID 'email'`, `authentik default OAuth Mapping: OpenID 'openid'`, and `authentik default OAuth Mapping: OpenID 'profile'` are selected.
  * `Subject Mode` is set to `Based on the User's Email` (I would recommend this method for nextcloud, but it's your choice...)
  * Click `Finish` to save.
* Navigate to `Applications > Applications`
* Create a New Application
  * Enter a name of your choosing
  * Enter the slug as something like `nextcloud-oauth`, this will be used in the next step.
  * (optional) Set a Group that you would like this grouped into.
    * This is not the Permissions section to restrict users from using this. To set permissions, visit [Application Group Permissions](applications-and-providers.md#application-group-permissions)
    * This Group Setting only groups applications on the Main Authentik Overview page for each User. Enter a name Exactly as you want it Grouped. If it is mispelled in anyway, it will create another group.
  * Select your `Provider` as the Nextcloud OAuth we just created above.
  * (optional) **Expand** `UI Settings`
    * Set a Launch URL (I set to main nextcloud url, not the redirect URL)
    * Enable `Open in new tab`
    * Set an Icon
  * Click `Finish` to save.

***

## Nextcloud OpenID Setup

* Login to Nextcloud local/default Admin Account
* Navigate to `+ Apps`
* Install `OpenID Connect user backend` if needed, instructions above [Requirements](https://github.com/lazy-media/public/blob/main/Authentik/Nextcloud/README.md#requirements)
* After installation, Navigate to `Administration Settings > OpenID Connect`
* Add a New Provider by click the Plus Icon
* Fill out the Form as Follows:
  * Identifier = `YOUR DISPLAY NAME SHOWN ON NEXTCLOUD LOGIN`
  * Client ID = `YOUR AUTHENTIK PROVIDER CLIENTID`
  * Client Secret = `YOUR AUTHENTIK PROVIDER SECRET KEY`
  * Discover Endpoint = `https://YOUR-AUTHENTIK-URL/application/o/YOUR-PROVIDER-SLUG/.well-known/openid-configuration`
    * Where `YOUR-PROVIDER-SLUG` is, enter the slug you created above such as `nextcloud-oauth`
  * Scope = `email` `profile` `openid` `ak_proxy` `nextcloud`
    * Enter these all on one line with a space in between each.
  * User ID Mapping = `sub`
  * Quota Mapping = `quota`
  * Groups Mapping = `groups`
  * Use Unique User ID = `False / Unchecked`
  * Use Group Provisioning = `True / Checked`
  * Send ID Token hint on logout = `True / Checked`

At the bottom with the check boxes

* Fill out the Form as Follows:
  * Use Unique user id = `UNCHECKED`
  * Use Provider Identifier as prefix for ids = `UNCHECKED`
  * Use Group Provisioning = `CHECKED`
  * (OPTIONAL) Check Bearer Token on API and WebDav with Bearer Token = `Checked / Unchecked`
  * (OPTIONAL) Auto Provision User when Accessing API and WebDav with Bearer Token = `Checked / Unchecked`
  * Send ID Token hint on logout = `CHECKED`

### Nextcloud Quota Expression Policy Property Mapping

```
# Extract all groups the user is a member of
groups = [group.name for group in user.ak_groups.all()]

# Nextcloud admins must be members of a group called "admin".
# This is static and cannot be changed.
# We append a fictional "admin" group to the user's groups if they are an admin in authentik.
# This group would only be visible in Nextcloud and does not exist in authentik.
if user.is_superuser and "admin" not in groups:
    groups.append("admin")

return {
    "name": request.user.name,
    "groups": groups,
    # To set a quota set the "nextcloud_quota" property in the user's attributes
    "quota": user.group_attributes().get("nextcloud_quota", None)
}
```
