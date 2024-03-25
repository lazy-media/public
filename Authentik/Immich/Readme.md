# Immich Setup

# NOTICE

Please take note of how my Authentik is setup [Authentik Setup](/Authentik/Readme.md)

## Assumptions

- You have basic knowledge of Setting Up OAuth Providers in Authentik

## Authentik Setup

- Create an OAuth Applicaton and Provider in Authentik
- For Redirect URLs in the Immich Provider, you can input 3 different URLS to be satisfied by Authentik and have SSO work.
- I personally entered the following redirect URLS with successfully working OAuth logins.
```
https://PUBLIC-IMMICH-URL/auth/login
app.immich:/
http://PRIVATE-IP-ADDRESS:PORT-NUMBER/auth/login
```

## Immich Setup

- Setup Immich with OAuth
- DO NOT CHECK MOBILE REDIRECT URL
- Remove Basic Authentication Form.

## Conclusion

This will allow users to use the mobile app, local IP, or domain name to login with OAuth correctly.
