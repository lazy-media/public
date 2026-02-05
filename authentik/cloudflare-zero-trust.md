---
description: Information on how to setup Cloudflare Zero Trust in Authentik.
---

# Cloudflare Zero Trust Authentik Setup

## NOTICE

Your results may vary, but this is what I did to get access to Cloudflare Zero Trust with my Authentik Instance. I DO NOT ACTIVELY USE CLOUDFLARE ZERO TRUST. I ONLY SET THIS UP AS A QUICK TEST TO HELP WITH ANOTHER SUPPORT QUESTION.

THIS WAS ABLE TO GET ME TO LOGIN TO MY CLOUDFLARE ZERO TRUST INSTANCE AND ABLE TO VIEW APPLICATIONS AFTER THE APPROPRIATE PERMISSIONS WERE IN PLACE IN CLOUDFLARE. THIS IS GOING TO BE YOUR RESPONSIBILITY TO FIGURE OUT. I ONLY FIGURED OUT HOW TO GET THE LOGIN PORTION WORKING.

***

## Assumptions

* You have knowledge of Cloudflare Zero Trust
* You have your Authentik User and a Cloudflare Zero Trust user with the same email

***

## Authentik Setup

1. Login to your Authentik Admin panel
2. Navigate to `Applications > Providers`
3. Create a Cloudflare Provider with the following settings:
   1. **Name=** `Cloudflare Zero Trust`
   2. **Authentication Flow=** `EMPTY`
   3. **Authorization Flow=** `YOUR CHOICE` I choose Implicit
   4. **EXPAND PROTOCOL SETTINGS**
      1. **Client Type=** `Confidential`
      2. **Client ID=** `MAKE NOTE OF THIS`
      3. **Client Secret=** `MAKE NOTE OF THIS`
      4. **Redirect URIs/Origins=** `LEAVE BLANK, LET AUTHENTIK AUTOFILL UPON FIRST LOGIN`
      5. **Signing Key=** `Cloudflare Imported Cert`
   5. **EXPAND ADVANCED PROTOCOL SETTINGS**
      1. **Access Code Validity=** Default
      2. **Access Token Validity=** Default
      3. **Refresh Token Validity=** Default
      4. **Scopes=** Select the following (Hold CTRL to select multiple)
         * `authentik default OAuth Mapping: OpenID 'email'`
         * `authentik default OAuth Mapping: OpenID 'offline_access'`
         * `authentik default OAuth Mapping: OpenID 'openid'`
         * `authentik default OAuth Mapping: OpenID 'profile'`
      5. **Subject Mode=** `Based on the User's Email`
      6. **Issuer Mode=** \`Each provider has a different issuer, base on the application slug
4. Click `SAVE` or `Finish`
5. Navigate to `Applications > Applications`
   1. Attach an Application to the Cloudflare Provider we just created
   2. **MAKE NOTE OF THE APPLICATION SLUG WHEN YOU CREATE THIS, IT IS NEEDED IN THE NEXT STEP WITH CLOUDFLARE!**

***

## Cloudflare Setup

1. Login to your Cloudflare admin panel
2. Navigate to your Zero Trust panel
3. Navigate to your Zero Trust Settings
4. Select `Authentication`
5. Find `Login Methods` and click `Add New`
   1. Select `OpenID Connect`
      * Fill out the form as follows:
        1. **Name=** Your Preferred Name for the Provider
        2. **App ID=** AUTHENTIK PROVIDER CLIENT ID
        3. **Client Secret=** AUTHENTIK PROVIDER CLIENT SECRET
        4. **Auth URL=** `https://auth.DOMAIN.EXAMPLE/application/o/authorize/`
        5. **Token URL=** `https://auth.DOMAIN.EXAMPLE/application/o/token/`
        6. **Certificate URL=** `https://auth.DOMAIN.EXAMPLE/application/o/AUTHENTIK-CLOUDFLARE-PROVIDER-SLUG/jwks/`
        7. **Proof Key for Code Exchange (PKCE)=** Disabled
        8. **Email Claim=** `email`
        9. **OIDC Claims=** (Create a new one for each scope claim)
           * `profile`
           * `openid`
           * `ak_proxy`
           * `offline_access`
6. Navigate to your Cloudflare Zero Trust Settings again
7. Find `App Launcher` and click `Manage`
   1. Click on the Tab for `Authentication`
   2. If you do not have `Accept all available identity providers` enabled, either enable it or select the provider we just created.

***

## Conclusion

This should enable Authentik Login on your personal Cloudflare Zero Trust instance and allow the use of your Authentik credentials to login to Cloudflare Zero Trust.

Please remember that it is your responsibility to setup Cloudflare Zero Trust to your needs. This guide only helps with getting the Authentik login method to display on the page.
