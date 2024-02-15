## This Authentik Instance was setup as a Proxy Provider, not a Forward Auth Provider.

## After setting up Vaultwarden Proxy in Authentik, input the following to block public access to admin page but allow access to Vaultwarden Web

### TO BE CLEAR: I am using Vaultwarden in a docker container using the vaultwarden/server image. I am also using Authentik to handle all traffic with no middle man like NPM or Traefik. These results may vary depending on your setup but this is what I have found to work for me. This enabled the whole user interface for me but blocked the admin section by Authentik.

```
^/$
^/#/.*
^/#/login
^/#/2fa
^/api/.*
^/images/.*
^/identity/.*
^/app/.*
^/locales/.*
```
