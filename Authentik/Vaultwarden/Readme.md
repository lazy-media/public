# Vaultwarden Admin Page Verification with Authentik

### Please be aware of how I have my Authentik instance setup. Found at [Authentik Setup](/Authentik/Readme.md)

## Assumptions
- Assumes that you are using the docker image `vaultwarden/server`
- Assumes you already have Vaultwarden installed and running
- Assumes you want the Admin Page enabled but everything else publicly available.
    - I only want the Admin Page enabled for individually inviting people instead of having registration open.
- Assumes you have setup Authentik with Vaultwarden already and it is accessible behind Authentik

## Authentik Variables
These are to be entered under the `Authentik Provider > Unauthenticated Paths` section.

```
^/$
^/#/.*$
^/#/login$
^/#/2fa$
^/api/.*$
^/images/.*$
^/identity/.*$
^/connectors/.*$
^/app/.*$
^/locales/.*$
^/notifications/.*$
^/icons/.*$
^/encrypt-worker.*.js
^/webauthn-connector.html
^/*.html
^/*.*.js
^/*.js
^/*.png$
^/*.jpg$
^/*.avif$
^/*.woff$
```

## NOTICE
These results may vary depending on your situation, but these are the settings I have found to work to allow all types of 2fa, assets, and anything else that needs to be used to load the web interface of Vaultwarden, while still protecting the Admin Page. To use from only a mobile device, not all of these are needed.
