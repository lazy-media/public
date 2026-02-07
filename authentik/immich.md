---
description: Information on how to setup Immich OpenID / OAuth with Authentik
---

# Immich

### Assumptions

* You have basic knowledge of Setting Up OAuth Providers in Authentik

### Authentik Setup

* Create an OAuth Applicaton and Provider in Authentik
* For Redirect URLs in the Immich Provider, you can input 3 different URLS to be satisfied by Authentik and have SSO work.
* I personally entered the following redirect URLS with successfully working OAuth logins.
* The first two are for lan and wan connections, the third one is for mobile applications

```
https://PUBLIC-IMMICH-URL/auth/login
http://PRIVATE-IP-ADDRESS:PORT-NUMBER/auth/login
app.immich:///oauth-callback
```

### Immich Setup

* Setup Immich with OAuth
* DO NOT CHECK MOBILE REDIRECT URL
* Remove Basic Authentication Form.

### Immich Google Photos Takeout Helpers

If you do a Google Photos Takeout, you need to run one of these programs below first before uploading to Immich. If you don't, then your pictures and videos will not be organized by date, time, location, etc..

* [Google Photos Takeout Helper](../google-photos-takeout/)

### Conclusion

This will allow users to use the mobile app, local IP, or domain name to login with OAuth correctly.
