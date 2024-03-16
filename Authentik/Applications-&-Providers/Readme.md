# Authentik Applications & Providers Setup

## Authentik New Easy Wizard Setup

1. Login to your Authentik Admin Account
2. Navigate to `Applications > Applications`
    - Click on `Create with Wizard`
    - Enter a Name of an Application
    - Enter a slug (if not autofilled)
    - (Optional) Set a Group that you want this application to be grouped into (i.e. `Admins`, `Nextcloud Users`)
    - (Optional) Expand `UI Settings` and set a `Launch URL` and enable `Open in new tab`
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
    - Click the `Edit` button under `Actions`
        - Under `Applications` either double click any applications on the left side, to enable access externally.
