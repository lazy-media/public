### This Authentik Instance was setup as a Proxy Provider, not a Forward Auth Provider.

### After setting up Vaultwarden Proxy in Authentik, input the following to block public access to admin page but allow access to Vaultwarden Web

```
^/$
^/#/.*
^/#/login
^/#/2fa
^/api/.*
^/images/.*
^/identity/.*
^/app/.*
^/*.js
^/locales/.*
```
