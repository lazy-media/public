# Jellyfin OpenID/OAuth Setup with Authentik

## Original Documentation

- [Jellyfin SSO Plugin](https://github.com/9p4/jellyfin-plugin-sso)

## Assumptions

- You have Jellyfin Installed and running
- You have a local Jellyfin Admin account to log into temporarily.
- You have basic knowledge of setting up an OAuth2/OpenID Provider in Authentik and already have one created to input into Jellyfin

## (Optional) Authentik Scope Mapping

Scope Name = `jellyfin`
```
return [group.name for group in user.ak_groups.all()]
```
Attach to your Jellyfin OAuth2/OpenID Provider in Authentik

## Enable Jellyfin Quick Connect

I recommend enabling the Quick Connect setting inside your Jellyfin server to make it possible to connect mobile devices, tv's, game consoles, and other media streaming devices other than a computer and web browser. This SSO method DOES NOT work with anything other than a computer and web browser, which is why I recommend enabling this feature.

To enable this feature:
- Login to Jellyfin Admin
- Navigate to `Administration > Dashboard`
- Locate and click on `General` in the left pane
- Find `Quick Connect` and check the box to enable it

## Adding Jellyfin OpenID Repository

- Login to Jellyfin Admin account
- Navigate to `Administration > Dashboard`
    - In the left pane, find and click on `Plugins`
    - Click on `Repositories` at the Top of the page
    - Click on the `+` button to add a new repository
        - Name the repository how you want. Something like `Jellyfin OpenID`
        - For `Repository URL`, enter
        ```
        https://raw.githubusercontent.com/9p4/jellyfin-plugin-sso/manifest-release/manifest.json
        ```
        - Click `Save` to add the repository
- Click on the `Catalog` tab at the top of the page
    - You should now see `SSO Authentication` show up. If you do not, restart your Jellyfin Server.
    - Click on and Install the new `SSO Authentication`
- Click on the `My Plugins` tab at the top of Jellyfin
    - Find the plugin `SSO-Auth` and click on it.
        - This should bring you to a screen that says `SSO Settings` with a form to fill out.
        - Fill out the form as you wish, but these are the settings I put:
            - **Name of OID Provider =** Authentik
            - **OID Endpoint =** https://YOUR-AUTHENTIK-URL/application/o/YOUR-JELLYFIN-OPENID-SLUG/.well-known/openid-configuration
            - **OpenID Client ID =** YOUR-AUTHENTIK-OAUTH2-CLIENT-ID
            - **OID Secret =** YOUR-AUTHENTIK-OAUTH2-CLIENT-SECRET
            - **Enabled =** YES
            - **Enable Authorization By Plugin =** YES
            - **Enable All Folders =** NO
            - **ENABLED FOLDERS CHECKLIST BOX:** I did not select anything
            - **ROLES:** (enter 1 per line): `authentik Admins`, `Jellyfin Users` or whatever groups you want
            - **Admin Roles:** `authentik Admins`
            - **(optional) ROLE BASED FOLDER ACCESS:** Enabled
            - Fill out the roles you want and how you want them, this is all up to you.
            - **Live TV Roles:** Enter your roles/groups you want access to Live TV. Something like `Jellyfin Users`
            - **Live TV Management Roles:** Enter something like your `authentik Admins` role
            - Do not enable Live TV Access by Default
            - Do not enable Live TV Management by Default
            - **ROLE CLAIM:** `groups`
            - **Request Additional Scopes:** (Enter 1 per line) `jellyfin` (if added scope mapping above), `openid`, `profile`, `email`, and `ak_proxy`
            - **Do not** set a `Default Provider`
            - **Set Default Username Claim:** `preferred_username`
            - **DO NOT CHECK THE 3 Insecure Boxes unless you need to**
            - **Scheme Override:** Enter `https` only if you need to.
        - Click `Save`

### Adding the Login Button to Jellyfin's Login Page

- Navigate to the `General` tab in the left pane
- Scroll down to the `Branding` Section
- Find the `Login Disclaimer` box
    - Input the following into this box:
```
<form action="https://YOUR-JELLYFIN-URL/sso/OID/start/NAME-OF-PROVIDER-YOU-NAMED-IN-JELLYFIN-ABOVE">
  <button class="raised block emby-button button-submit">
    ENTER NAME YOU WANT SHOWN ON LOGIN PAGE
  </button>
</form>
```
- Find the `Custom CSS Code` box
- Enter the following into this box:
```
a.raised.emby-button {
  padding: 0.9em 1em;
  color: inherit !important;
}

.disclaimerContainer {
  display: block;
}
```
- Click `Save` to enable the login button.