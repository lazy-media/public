---
description: >-
  An example on how to setup a basic Authentik Application & Provider. This is a
  generic setup where Authentik is your reverse proxy.
---

# Basic Applications & Providers Setup

### Intro

This guide walks through creating Authentik Applications and Providers.

It covers Proxy Providers and OAuth2/OIDC using the built-in wizard.

It also covers binding access to groups.

### Prerequisites

* Authentik is installed and running.
* You can sign in to the Authentik Admin UI.
* You have an Authentik admin account.
* You have a working domain and DNS for your external hostnames.
* Your target service is reachable on your internal network.
* You know the service’s internal URL and port.

### Assumptions

* Authentik is acting as your reverse proxy.
* You will publish apps on unique subdomains.
* The embedded outpost is available and running.
* You will attach apps to an outpost to make them reachable.

### Authentik Proxy Provider Easy Wizard Setup

1. **Login to your Authentik Admin Account**
2. **Navigate to `Applications > Applications`**
   1. Click on `Create with Wizard`
   2. Enter a Name for your Application (i.e. Sonarr)
   3. Enter a slug (if not autofilled, this is the path for Authentik to use, so it should be something simple or related to the program)
   4. (Optional) Set a Group that you want this application to be grouped into on the User Interface (i.e. `Admins`, `Nextcloud Users`)
      1. <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Be aware: That if you set this group, you need to manually type in the group exactly how you want it grouped. If there is a mispelling or any difference, it will create a new group.</p></div>
   5. (Optional) Expand `UI Settings`
      1. Set a `Launch URL`
         * To hide an application enter the launch URL as `blank://blank`
           * Please note that when this is set for OpenID/OAuth Providers/Applications, this is used on the Authentik Logout Page of that Provider when you are asked to go back to the `Authentik Overview`, `log out of Authentik completely`, or `Log back into the application you just signed out of`.
      2. Enable `Open in new tab`
   6. Click `Next`
   7. Select `Transparent Reverse Proxy` and click `Next`
   8. Provider name should be autofilled, change if you want to
   9. (Optional) Select an Authentication Flow if you want to, I usually don't select one.
   10. Select `Authorization Flow` as either Implicit or Explicit
       1. Implicit will not show a dialog box before continuing to the site in question.
       2. Explicit will show a dialog box before fully navigating to the site in question and force the user to confirm they want to continue.
   11. Set your `External Host` to a fully qualified subdomain name (i.e. `https://test.domain.example`)
   12. Set the `Internal Host` to the internal IP Address and Port Number of the service you want Proxied. (i.e. `http://192.168.1.10:8080`)
       1. <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p><strong>NOTE: If your internal service normally uses <code>https</code> instead of <code>http</code>, (i.e. <code>https://192.168.1.10:8443</code>), make sure you <code>DISABLE INTERNAL HOST SSL VALIDATION</code></strong></p></div>
   13. Expand `Advanced Protocol Settings` at the bottom
       1. Under `Certificate`, choose your Cloudflare Certificate we created during [Authentik Installation](../Installation-Instructions/Authentik/#cloudflare-setup).
   14. (Optional) For Testing, you can pass through the whole application you are trying to proxy by putting a `/` under the `Unauthenticated Paths` box.
   15. Click `Next` or `Finish`
   16. Navigate to `Applications > Outposts`
   17. Click the `Edit` button under `Actions` for the default `authentik Embedded Outpost`
       1. Under `Applications` either double click any applications on the left side, or Select on the Left Side, and press the `>` in the center column to move to the right side. The right side tells Authentik which applications you want available externally.
   18. Click `Update`.

***

### Application & Proxy Provider Setup Without Easy Setup Wizard

1. **Login to your Authentik Admin Account**
2. **Navigate to `Applications > Providers`**
   1. Click on `Create`
   2. Select `Proxy Provider` and click `Next`
   3. Enter a Name for your Provider (i.e. Sonarr)
      1. (optional) Select an Authentication Flow
      2. Select `Authorization Flow` as either Implicit or Explicit
         * Implicit will not show a dialog box before continuing to the site in question.
         * Explicit will show a dialog box before fully navigating to the site in question and force the user to confirm they want to continue.
      3. Select `Proxy` instead of `Forward auth`
      4. Enter your `External Host` as a fully qualified subdomain. (i.e. `https://nextcloud.domain.example`)
      5. Set the `Internal Host` to the internal IP Address and Port Number of the service you want Proxied. (i.e. `http://192.168.1.10:8080`)
         * <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p><strong>NOTE: If your internal service normally uses <code>https</code> instead of <code>http</code>, (i.e. <code>https://192.168.1.10:8443</code>), make sure you <code>DISABLE INTERNAL HOST SSL VALIDATION</code></strong></p></div>
         * Expand `Advanced Protocol Settings` at the bottom
           * Under `Certificate`, choose your Cloudflare Certificate we create earlier.
         * (Optional) For Testing, you can pass through the whole application you are trying to proxy by putting a `/` under the `Unauthenticated Paths` box.
   4. Click `Finish`
3. **Navigate to `Applications > Applications`**
   1. Click `Create`
      1. Enter a Name for your Application (i.e. Sonarr)
      2. Enter a Slug (if not autofilled) (i.e. sonarr)
         * Slugs cannot have spaces. If you type out a slug manually, spaces will be replaced with a dash (`-`)
      3. Enter a Group Name if you want these to be grouped into separate groups (i.e. `Plex Users`, `Nextcloud Users`, `Admins`)
         * <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Be aware: That if you set this group, you need to manually type in the group exactly how you want it grouped. If there is a mispelling or any difference, it will create a new group.</p></div>
      4. Select a Provider you want this Application linked to. (i.e. Sonarr)
      5. Backchannel Providers is left empty.
      6. (optional) Expand `UI Settings`
         1. Fill out a Launch URL, or leave empty to be automatically pulled from the selected provider.
            1. To hide an application enter the launch URL as `blank://blank`
               * Please note that when this is set for OpenID/OAuth Providers/Applications, this is used on the Authentik Logout Page of that Provider when you are asked to go back to the Authentik Overview, log out of Authentik completely, or Log back into the application you just signed out of.
         2. Enable `Open in new tab`
         3. Upload an Icon for the Application
   2. Click `Create`
4. **Navigate to `Applications > Outposts`**
   1. Click the `Edit` button under `Actions` for the default `authentik Embedded Outpost`
      1. Under `Applications` either double click any applications on the left side, or Select on the Left Side, and press the `>` in the center column to move to the right side. The right side tells Authentik which applications you want available externally.
   2. Click `Update`.

***

### Authentik Basic OAuth2/OpenID Setup

#### Using Authentik's New Easy Setup Wizard

1. **Login to Authentik Admin**
2. **Navigate to `Applications > Applications`**
3. **Click on `Create with Wizard`**
4. **Enter a Name such as `Example OAuth`**
   1. **TAKE NOTE OF THE SLUG** Slug should get autofilled, change if you want to make it something easy to remember. This is used in some cases for URLS in the application you are trying to setup.
   2. (Optional) Type a Group you want this categorized under.
   3. (Optional) Expand `UI Setdtings`
      1. Enter a `Launch URL`
         * To Hide this OAuth Provider on the User Apps Main Page, type in `blank://blank`
         * Leave empty to have Authentik Auto detect
         * Enter the base url of the app you want to set (i.e. `https://nextcloud.example.domain`)
      2. Select `Open in new tab`
5. **Click `Next`**
6. **Select `OAuth2/OIDC`**
7. **Click `Next`**
8. **The Name for the Application should be autofilled (Change if you want)**
   1. Authentication Flow is usually Empty
   2. Authorization Flow is either Implicit or Explicit
      1. Implicit will not show a confirmation diaglog box to the user
      2. Explicit will show a confirmation box and force the user to confirm they want to continue.
   3. Under Protocol Settings
      1. Client Type should be `Confidential`
      2. Make note of `ClientID` & `Client Secret`
      3. Redirect URIs/ Origins can be left blank since it autofills with first successful redirect
         * If you know the redirect uri, fill it in here
      4. Choose a Signing Key. I use an Imported Cloudflare Cert, so I select this.
   4. Expand `Advanced Protocol Settings`
      1. Under `Scopes`, Hold CTRL and Click on the scopes for `email`, `openid`, `profile`, and `offline_access` at minimum, if not already preselected. You can also select `ak_proxy` if your OAuth provider has issues, this usually resolves it for me.
      2. Under `Subject Mode`, I personally select `Based on User's Email`
      3. I usually leave everything else default on this screen.
   5. Click `Next` to save and Finish.

***

### Application Group Permissions

1. **Login to your Authentik Admin Panel**
2. **Navigate to `Applications > Applications`**
3. **Find an Application you want to secure to a Group (i.e. Plex Users)**
4. **Click the `NAME` of the Application, this should look like a link (i.e. Sonarr)**
   1. When the page loads, you should have 3 tabs that say `Overview`, `Policy/Group/User Bindings` and `Permissions`
   2. Select `Policy/Group/User Bindings`
   3. Click on `Bind Existing Policy`
      1. On the Binding Pop Up Page, you should have 3 options, `Policy`, `Group`, and `User`
      2. Select `Group`
         * In the `Group` Dropdown Menu, select the `authentik Admins` group first.
         * Make sure the `Order` is `0`
         * Select `Create`
   4. Click on `Bind Existing Stage` again.
      1. Select `Group` again
         * In the `Group` Dropdown Menu, select the next group you want to be able to access this application (i.e. Plex Users)
         * Increment your `Order` to `10` or any number greater than `0` so it gets placed under the previous group added.
         * Select `Create`

***

### Conclusion

This should explain how to create Authentik Applications and Providers using either the easy setup wizard or the manual setup flow. It also explains how to attach your applications to an outpost so they are available externally, how to select your certificate for provider security settings, and how to restrict access by binding applications to groups.
