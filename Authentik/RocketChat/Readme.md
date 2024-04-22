# Rocket Chat Server OAuth2/OpenID Setup with Authentik

# Documentation
[Authentik Documentation](https://docs.goauthentik.io/integrations/services/rocketchat/)

# Assumptions

- Basic understanding of setting up an Authentik OAuth2/OpenID Provider and Application, if not, you can follow this guide [Basic OAuth/OpenID Setup](/Authentik/Applications-&-Providers/Readme.md#authentik-basic-oauth2openid-setup)
- Have RocketChat Server installed and running
- I have RocketChat Server installed via SNAP on Ubuntu 22.04

# Rocket Chat Server Config

- Login to Local RocketChat Admin Account
- Navigate to `Workspace Administration`
- Navigate to `Settings` in the left column
- Find the option for `OAuth` and click `Open`
- Create a `Custom OAuth`
- Fill out the form appropriately
    - **URL=** `https://auth.domain.example/application/o`
    - **Token Path=** `/token/`
    - **Token Sent Via=** `Payload`
    - **Identity Token Sent Via=** `Same as "Token Sent Via"`
    - **Identity Path=** `/userinfo/`
    - **Authorize Path=** `/authorize/`
    - **Scope=** `email profile openid`
    - **Param Name for Access Token=** `access_token`
    - **Id=** `AUTHENTIK OAUTH CLIENT ID`
    - **Secret=** `AUTHENTIK OAUTH CLIENT SECRET`
    - **Login Style=** `Redirect`
    - **Button Text=** `LOGIN BUTTON TEXT - CHANGE TO YOUR LIKING`
    - **Button Text Color=** `#FFFFFF` # Change to your liking, enter a Hex Value
    - **Button Color=** `#1d74f5` # Change to your liking, enter a Hex Value
    - **Key Field=** `Username`
    - **Username Field=** `preferred_username`
    - **Email Field=** `email`
    - **Name Field=** `name`
    - **Avatar Field=** `EMPTY`
    - **Roles/Group field name=** `groups`
    - **Roles/Group field for Channel Mapping=** `groups`
    - **User Data Group Map=** `rocket.cat`
    - (Optional) **Map Roles/Groups to Channels=** `Unchecked`
    - (Optional) **Merge Roles From SSO=** `Unchecked`
    - (Optional) **Roles to Sync=** `ENTER YOUR AUTHENTIK ROLES TO SYNC`
    - **Merge Users=** `Checked`
    - (Optional) **Merge Users from distinct Services=** `Unchecked`
    - **Show Button on Login Page=** `Checked`
- SAVE
