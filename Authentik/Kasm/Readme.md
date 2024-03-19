# Kasm OpenID / OAuth Setup with Authentik

## My Authentik Setup

- I currently have Authentik installed alone on a Proxmox LXC container using Ubuntu 22.04, and separate from any other services.
- My Authentik Ports get set to 443 and 80 within the Docker Environment Variables File, but set to the standard ports in the Docker Compose File as 9443:9443 and 9000:9000.
- I currently ONLY run Authentik as my Reverse Proxy, no middle man like NPM, Traefik, Caddy, etc.
- I use Cloudflare Certificates installed into Authentik, not provided by any other reverse proxy or created by Let's Encrypt.
- I do not use Cloudflare Tunnels, I use other security measures provided by Cloudflare to protect my domain.
- I have my ISP Modem in bridge mode and have a Unifi Security Gateway handling all internet traffic.
    - I have port 443 forwarded to Authentik
- For Installation Instructions on how I setup my Authentik, visit [Authentik Installation](Installation-Instructions/Authentik/Readme.md)

## Assumptions
- This guide assumes you already have Kasm up and Running from a fresh install.
- This is best if done from a fresh install.
- No users currently in Kasm have the same email, or username as any Authentik User.
- You are on the latest version of Authentik.

## Setting Up Authentik with Easy Setup Wizard

- Login to Authentik Admin
- Navigate to `Applications > Applications`
- Click on `Create with Wizard`
- Enter a Name such as `Kasm OAuth`
    - Slug should get autofilled
    - (Optional) Type a Group you want this categorized under.
    - (Optional) Expand `UI Settings` 
        - Enter a `Launch URL` (To Hide this OAuth Provider on the User Apps Main Page, type in `blank://blank`)
        - Select `Open in new tab`
- Click `Next`
- Select `OAuth2/OIDC`
- Click `Next`
- The Name for the Application should be autofilled (Change if you want)
    - Authentication Flow is usually Empty
    - Authorization Flow is either Implicit or Explicit
        - Implicit will not show a confirmation diaglog box to the user
        - Explicit will show a confirmation box and force the user to confirm they want to continue.
    - Under Protocol Settings
        - Client Type should be `Confidential`
        - Make note of `ClientID` & `Client Secret`
        - Redirect URIs/ Origins can be left blank since it autofills with first successful redirect.
            - You can also enter `https://kasm.domain.example/api/oidc_callback` (replace `kasm.domain.example` with your domain)
        - Choose a Signing Key. I use an Imported Cloudflare Cert, so I select this.
    - Expand `Advanced Protocol Settings`
        - Under `Scopes`, Hold CTRL and Click on the scopes for `email`, `openid`, and `profile` at minimum, if not already preselected.
        - Under `Subject Mode`, I personally select `Based on User's Email`
        - I usually leave everything else default on this screen.
    - Click `Next` to save and Finish.

## Setting up Kasm

### Requirements

- Login with local Kasm Admin account.
- Navigate to `Admin > Access Management > Users`
- Make sure your local user **DOES NOT** have the same username, email, or anything else that matches with your Authentik Admin or other accounts. **Best to use default Kasm Admin Account** for this until this is finished being setup.

### Creating Groups in Kasm

- **It is best to manually create the same groups in Kasm as you have in Authentik. These should be identically named.**
- *You don't need all your Authentik Groups in Kasm, just the ones you want, like the group you have set in Authentik to access Kasm.*
- **EXAMPLE: If you have an Authentik group named `Discord Users`, or `Kasm Users` then you would create a Kasm Group called `Discord Users`, or `Kasm Users`.**
- This is just for ease in my opinion, but you can name these whatever you want. The SSO Group Mapping is what matters most.

### Setting up OpenID

- Navigate to `Admin > Access Management > Authentication > OpenID`
- Click on `Add Config` in the top right
- Fill out the form as follows:
    - **Display Name** = `ENTER-YOUR-DISPLAY-NAME-HERE`
    - **Logo URL** = `https://YOUR-AUTHENTIK-URL/static/dist/assets/icons/icon.png`
    - **ENABLED** = `true`
    - **Auto Login** = `true` or `false` (Your Preference)
    - **Hostname** = `LEAVE EMPTY`
    - **Default** = `true`
    - **Client ID** = `AUTHENTIK-OAUTH-PROVIDER-CLIENT-ID-HERE`
    - **Client Secret** = `AUTHENTIK-OAUTH-PROVIDER-CLIENT-SECRET-KEY-HERE`
    - **Authorization URL** = `https://YOUR-AUTHENTIK-URL/application/o/authorize/`
    - **Token URL** = `https://YOUR-AUTHENTIK-URL/application/o/token`
    - **User Info URL** = `https://YOUR-AUTHENTIK-URL/application/o/userinfo`
    - **Scope** *(NEW LINE FOR EACH)* = `email` `profile` `openid` `ak_proxy`
    - **Username Attributes** = `email`
    - **Groups Attributes** = `groups`

- Click `Save`.

### Edit Kasm OAuth Provider

- Now Edit the OAuth Provider you just created in Kasm.
- Click on the tab for `Attribute Mapping`
- Click `Add SSO Mapping`
- Select `Email` for the first field
- Under Attribute enter `email`
- Click `Save`

### Edit Kasm Groups for SSO Mapping

- Navigate to `Admin > Access Management > Groups`
- Edit the `All Users` Group
- Click on the tab for `SSO Group Mappings`
- Click on `Add SSO Mapping`
    - Select your Provider we just added
    - Slide to Select `Assign All Users`
    - Click `Submit`
- Edit the `Admins` Group
- Click on the tab for `SSO Group Mappings`
- Click on `Add SSO Mapping`
    - Select your Provider we just added
    - **DO NOT SELECT** `Assign All Users`
    - Under Attributes type in `authentik Admins`
    - Click `Submit`
- Edit any other group in Kasm
- For each Group, click on the tab for `SSO Group Mapping`
- Click on `Add SSO Mapping`
- Select your `Authentik SSO Provider`
- **DO NOT SELECT** `Assign All Users`
- Under `Group Attributes`, enter the name of the Group from Authentik you want assigned. **MUST BE IDENTICAL**
    - **(i.e.) An Authentik Group Named `Discord Users` should be typed in exactly as `Discord Users` in to this `Group Attributes`**

## Conclusion

You should now be able to login to Kasm with your new Authentik Login Button or it will automatically log you in if you decided to enable that. If you login with your Authentik Admin, it should assign you to the Admin Group of Kasm (if setup correctly).
