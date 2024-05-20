# Cloudflare Zero Trust Authentik Setup

## NOTICE
Your results may vary, but this is what I did to get access to Cloudflare Zero Trust with my Authentik Instance.
I DO NOT ACTIVELY USE CLOUDFLARE ZERO TRUST. I ONLY SET THIS UP AS A QUICK TEST TO HELP WITH ANOTHER SUPPORT QUESTION.

THIS WAS ABLE TO GET ME TO LOGIN TO MY CLOUDFLARE ZERO TRUST INSTANCE AND ABLE TO VIEW APPLICATIONS AFTER THE APPROPRIATE PERMISSIONS WERE IN PLACE IN CLOUDFLARE. THIS IS GOING TO BE YOUR RESPONSIBILITY TO FIGURE OUT. I ONLY FIGURED OUT HOW TO GET THE LOGIN PORTION WORKING.

## Assumptions
- You have knowledge of Cloudflare Zero Trust

## Authentik Setup

- Login to your Authentik Admin panel
- Navigate to `Applications > Providers`
- Create a Cloudflare Provider with the following settings:
    - **Name=** `Cloudflare Zero Trust`
    - **Authentication Flow=** `EMPTY`
    - **Authorization Flow=** `YOUR CHOICE` I choose Implicit
    - **EXPAND PROTOCOL SETTINGS**
        - **Client Type=** `Confidential`
        - **Client ID=** `MAKE NOTE OF THIS`
        - **Client Secret=** `MAKE NOTE OF THIS`
        - **Redirect URIs/Origins=** `LEAVE BLANK, LET AUTHENTIK AUTOFILL UPON FIRST LOGIN`
        - **Signing Key=** `Cloudflare Imported Cert`
    - **EXPAND ADVANCED PROTOCOL SETTINGS**
        - **Access Code Validity=** Default
        - **Access Token Validity=** Default
        - **Refresh Token Validity=** Default
        - **Scopes=** Select the following (Hold CTRL to select multiple)
            - `authentik default OAuth Mapping: OpenID 'email'`
            - `authentik default OAuth Mapping: OpenID 'offline_access'`
            - `authentik default OAuth Mapping: OpenID 'openid'`
            - `authentik default OAuth Mapping: OpenID 'profile'`
        - **Subject Mode=** `Based on the User's Email`
        - **Issuer Mode=** `Each provider has a different issuer, base on the application slug
- Click `SAVE` or `Finish`
- Navigate to `Applications > Applications`
    - Attach an Application to the Cloudflare Provider we just created
    - **MAKE NOTE OF THE APPLICATION SLUG WHEN YOU CREATE THIS, IT IS NEEDED IN THE NEXT STEP WITH CLOUDFLARE!**

## Cloudflare Setup

- Login to your Cloudflare admin panel
- Navigate to your Zero Trust panel
- Navigate to your Zero Trust Settings
- Select `Authentication`
- Find `Login Methods` and click `Add New`
    - Select `OpenID Connect`
        - Fill out the form as follows:
            - **Name=** Your Preferred Name for the Provider
            - **App ID=** AUTHENTIK PROVIDER CLIENT ID
            - **Client Secret=** AUTHENTIK PROVIDER CLIENT Secret
            - **Auth URL=** `https://auth.DOMAIN.EXAMPLE/application/o/authorize/`
            - **Token URL=** `https://auth.DOMAIN.EXAMPLE/application/o/token/`
            - **Certificate URL=** `https://auth.DOMAIN.EXAMPLE/application/o/AUTHENTIK-CLOUDFLARE-PROVIDER-SLUG/jwks/`
            - **Proof Key for Code Exchange (PKCE)=** Disabled
            - **Email Claim=** `email`
            - **OIDC Claims=** (Create a new one for each scope claim)
                - `profile`
                - `openid`
                - `ak_proxy`
                - `offline_access`