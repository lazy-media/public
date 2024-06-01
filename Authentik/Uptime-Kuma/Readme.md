# Uptime Kuma and Authentik Setup

## Original Documentation
- [Authentik Uptime Kuma Documentation](https://docs.goauthentik.io/integrations/services/uptime-kuma/)
- [Uptime Kuma Installation](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install#-non-docker)

## My Installation Method
- Installed on Proxmox LXC Container with Ubuntu 22.04
- Installed via Non Docker Method

## Assumptions
- Basic knowledge of Authentik
- Basic knowledge of Uptime Kuma

## Authentik Setup
I recommend you follow the official Authentik Documentation above for best results. But this is what I did to make it work.

Setup a Provider and Application for Uptime Kuma and add to your Outpost.

In the Uptime Kuma Authentik Provider, edit the section for `Unauthenticated Paths` and input the following:

```
^/$
^/status
^/assets/
^/assets
^/icon.svg
^/api/.*
^/upload/.*
^/metrics
```
The line with `^/status` you can define this as a public one such as `default`. So if you only want the default status page viewable publically but want all other status pages protected by Authentik, you can refine this to be something like `^/status/default` or `^/status/admin` to allow the single page.