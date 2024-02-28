# Wiki-JS OAuth Setup
## Authentik Documentation Used
[Authentik Docs](https://goauthentik.io/integrations/services/wiki-js/)
## Preparation
- Open 2 browser tabs or windows
- Navigate to your Wiki-JS Admin Portal in one of the tabs or windows
- Navigate to your Authentik Admin Portal in the other
## Wiki-JS Setup - Part 1
- Go to your Wiki-JS Admin Portal
- Navigate to ***Authentication***
- Add a ***Generic OpenID Connect/OAuth2***
- ***Make a note of the*** **Callback URL/Redirect URI** in the **Configuration Reference** section at the bottom.
## Authentik Setup - Part 1
- Go to your Authentik Admin Portal and Navigate to Admin Section.
- Go to ***Applications***, then ***Providers***
- ***Create*** a new ***OAuth2/OpenID Provider***
- Set ***Redirect URI*** ***to*** the ***Wiki-JS Callback URL from above***
- Select any Signing Key
- ***NOTE THE CLIENT ID AND CLIENT SECRET***
- Click SAVE
## Wiki-JS Setup - Part 2
- Go back to your Wiki-JS Admin Portal
- Configure the Authentication Method similar to the following:
- ***REPLACE 'authentik.company' WITH YOUR URL FOR AUTHENTIK***
```
Client ID: Client ID from the authentik provider.
Client Secret: Client Secret from the authentik provider.
Authorization Endpoint URL: https://authentik.company/application/o/authorize/
Token Endpoint URL: https://authentik.company/application/o/token/
User Info Endpoint URL: https://authentik.company/application/o/userinfo/
Issuer: https://authentik.company/application/o/wikijs/
Logout URL: https://authentik.company/application/o/wikijs/end-session/
Allow self-registration: Enabled
Assign to group: The group to which new users logging in from authentik should be assigned.
```
## Authentik Setup - Part 2
- Go back to your Authentik Admin Portal
- Create an Application
- Enter a name
- Under Provider, select the Wiki Provider you created earlier.
- Expand UI SETTINGS
- Set the LAUNCH URL to the Wiki-JS Callback URL you noted down above.

## IMPORTANT NOTE
- Doing this will skip the Wiki-JS Login Prompt and log you in directly.
- Optionally, you can setup a seperate Authentication and Enrollment Flow to add these users to a Group.
- Check this guide out on how to setup [Authentik OAuth Setup](https://gitlab.lazymedia.media/lazymedia/authentik/-/blob/9236f51bc5693c6812d89e5000ae9487e0fdc96e/Flows%20Setup/OAuth%20Flow%20Setup.md)
