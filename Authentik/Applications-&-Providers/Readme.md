# Authentik Applications & Providers Setup

## Authentik New Easy Wizard Setup

- Login to your Authentik Admin Account
- Navigate to `Applications > Applications`
    - Click on `Create with Wizard`
    - Enter a Name for your Application (i.e. Sonarr)
    - Enter a slug (if not autofilled)
    - (Optional) Set a Group that you want this application to be grouped into (i.e. `Admins`, `Nextcloud Users`)
        - Be aware: That if you set this group, you need to manually type in the group exactly how you want it grouped. If there is a mispelling or any difference, it will create a new group.
    - (Optional) Expand `UI Settings`
        - Set a `Launch URL`
            - To hide an application enter the launch URL as `blank://blank`
                - Please note that when this is set for OpenID/OAuth Providers/Applications, this is used on the Authentik Logout Page of that Provider when you are asked to go back to the Authentik Overview, log out of Authentik completely, or Log back into the application you just signed out of.
        - Enable `Open in new tab`
    - Click `Next`
    - Select `Transparent Reverse Proxy` and click `Next`
    - Provider name should be autofilled, change if you want to
    - (Optional) Select an Authentication Flow if you want to, I usually don't select one.
    - Select `Authorization Flow` as either Implicit or Explicit
        - Implicit will not show a dialog box before continuing to the site in question.
        - Explicit will show a dialog box before fully navigating to the site in question and force the user to confirm they want to continue.
    - Set your `External Host` to a fully qualified subdomain name (i.e. `https://test.domain.example`)
    - Set the `Internal Host` to the internal IP Address and Port Number of the service you want Proxied. (i.e. `http://192.168.1.10:8080`)
        - **NOTE: If your internal service normally uses `https` instead of `http`, (i.e. `https://192.168.1.10:8443`), make sure you `DISABLE INTERNAL HOST SSL VALIDATION`**
    - Expand `Advanced Protocol Settings` at the bottom
        - Under `Certificate`, choose your Cloudflare Certificate we create earlier.
    - (Optional) For Testing, you can pass through the whole application you are trying to proxy by putting a `/` under the `Unauthenticated Paths` box.
    - Click `Next` or `Finish`
    - Navigate to `Applications > Outposts`
    - Click the `Edit` button under `Actions` for the default `authentik Embedded Outpost`
        - Under `Applications` either double click any applications on the left side, or Select on the Left Side, and press the `>` in the center column to move to the right side. The right side tells Authentik which applications you want available externally.
    - Click `Update`.

## Expanded Application & Provider Setup

- Login to your Authentik Admin Account
- Navigate to `Applications > Providers`
    - Click on `Create`
    - Select `Proxy Provider` and click `Next`
    - Enter a Name for your Provider (i.e. Sonarr)
        - (optional) Select an Authentication Flow
        - Select `Authorization Flow` as either Implicit or Explicit
            - Implicit will not show a dialog box before continuing to the site in question.
            - Explicit will show a dialog box before fully navigating to the site in question and force the user to confirm they want to continue.
        - Select `Proxy` instead of `Forward auth`
        - Enter your `External Host` as a fully qualified subdomain. (i.e. `https://example.domain.ex`)
        - Set the `Internal Host` to the internal IP Address and Port Number of the service you want Proxied. (i.e. `http://192.168.1.10:8080`)
            - **NOTE: If your internal service normally uses `https` instead of `http`, (i.e. `https://192.168.1.10:8443`), make sure you `DISABLE INTERNAL HOST SSL VALIDATION`**
            - Expand `Advanced Protocol Settings` at the bottom
                - Under `Certificate`, choose your Cloudflare Certificate we create earlier.
            - (Optional) For Testing, you can pass through the whole application you are trying to proxy by putting a `/` under the `Unauthenticated Paths` box.
    - Click `Finish`
- Navigate to `Applications > Applications`
    - Click `Create`
        - Enter a Name for your Application (i.e. Sonarr)
        - Enter a Slug (if not autofilled) (i.e. sonarr)
            - Slugs cannot have spaces. If you type out a slug manually, spaces will be replaced with a dash (`-`)
        - Enter a Group Name if you want these to be grouped into separate groups (i.e. `Plex Users`, `Nextcloud Users`, `Admins`)
            - Be aware: That if you set this group, you need to manually type in the group exactly how you want it grouped. If there is a mispelling or any difference, it will create a new group.
        - Select a Provider you want this Application linked to. (i.e. Sonarr)
        - Backchannel Providers is left empty.
        - (optional) Expand `UI Settings`
            - Fill out a Launch URL, or leave empty to be automatically pulled from the selected provider.
                - To hide an application enter the launch URL as `blank://blank`
                    - Please note that when this is set for OpenID/OAuth Providers/Applications, this is used on the Authentik Logout Page of that Provider when you are asked to go back to the Authentik Overview, log out of Authentik completely, or Log back into the application you just signed out of.
            - Enable `Open in new tab`
            - Upload an Icon for the Application
    - Click `Create`
- Navigate to `Applications > Outposts`
    - Click the `Edit` button under `Actions` for the default `authentik Embedded Outpost`
        - Under `Applications` either double click any applications on the left side, or Select on the Left Side, and press the `>` in the center column to move to the right side. The right side tells Authentik which applications you want available externally.
    - Click `Update`.

## Application Group Permissions

- Login to your Authentik Admin Panel
- Navigate to `Applications > Applications`
- Find an Application you want to secure to a Group (i.e. Plex Users)
- Click the `NAME` of the Application, this should look like a link (i.e. Sonarr)
    - When the page loads, you should have 3 tabs that say `Overview`, `Policy/Group/User Bindings` and `Permissions`
    - Select `Policy/Group/User Bindings`
    - Click on `Bind Existing Policy`
        - On the Binding Pop Up Page, you should have 3 options, `Policy`, `Group`, and `User`
        - Select `Group`
            - In the `Group` Dropdown Menu, select the `authentik Admins` group first.
            - Make sure the `Order` is `0`
            - Select `Create`
    - Click on `Bind Existing Stage` again.
        - Select `Group` again
            - In the `Group` Dropdown Menu, select the next group you want to be able to access this application (i.e. Plex Users)
            - Increment your `Order` to `10` or any number greater than `0` so it gets placed under the previous group added.
            - Select `Create`


### Conclusion

This should explain how to Add your Cloudflare Certificate into Authentik, and setup your first Applicaton and Provider using your Cloudflare certificate for Security. This also explains how to setup an Application and Provider, connect it to your default authentik outpost, and apply Group policies to the applications.
