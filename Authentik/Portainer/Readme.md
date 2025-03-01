# Portainer OpenID Setup

## Purpose

This will help you setup OpenID login to Portainer so you can log in with your Authentik User

## Original Documentation

- [Authentik Documentation](https://docs.goauthentik.io/integrations/services/portainer/)

## Assumptions

- Have basic knowledge of Authentik and how to create an OAuth2/OpenID Provider, if not, you can follow [Basic OAuth/OpenID Setup](/Authentik/Applications-&-Providers/Readme.md#authentik-basic-oauth2openid-setup)
- Have access to local portainer account

## Portainer Setup

- Login to local Portainer Admin
- Navigate to `Settings > Authentication`
- Select your preferred `Session Timeout`
- Select `OAuth` as the `Authentication Method`
- **Enable** `Use SSO`
- *Business Feature* **Enable** `Hide internal authentication prompt`
- **Enable** `Automatic User Provisioning` if you want to
- *Business Feature* **Enable** `Automatic Team Membership`
- Select `Custom` as your `Provider`
- Fill out the form accordingly
    - **Client ID=** `AUTHENTIK OAUTH CLIENT ID`
    - **Client Secret=** `AUTHENTIK OAUTH CLIENT SECRET`
    - **Authorization URL=** `https://auth.domain.example/application/o/authorize/`
    - **Access Token URL=** `https://auth.domain.example/application/o/token/`
    - **Resource URL=** `https://auth.domain.example/application/o/userinfo/`
    - **Redirect URL=** `https://portainer.domain.example`
    - **Logout URL=** `https://auth.domain.example/application/o/AUTHENTIK-PORTAINER-OAUTH-SLUG/end-session/`
    - **User Identifier=** `email`
    - **Scopes=** `email openid profile ak_proxy offline_access`
    - **Auth Style=** `Auto Detect`
- Click `Save`