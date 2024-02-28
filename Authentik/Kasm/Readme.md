# Kasm OpenID / OAuth Setup with Authentik

## Setting up Kasm

This guide assumes you already have Kasm up and Running. Best if done from a fresh install.

### Requirements

- Login with local Kasm Admin account.
- Navigate to **Admin > Access Management > Users**
- Make sure your local user **DOES NOT** have the same username, email, or anything else that matches with your Authentik Admin or other accounts. **Best to use default Kasm Admin Account** for this until this is finished being setup.

### Creating Groups in Kasm

- **It is best to Manually Create the Same groups in Kasm as you have in Authentik. These should be identically named.**

### Setting up OpenID

- Navigate to **Admin > Access Management > Authentication > OpenID**
- Click on **Add Config** in the top right
- Fill out the form as follows:
```
Display Name = ENTER-YOUR-DISPLAY-NAME-HERE
Logo URL = https://YOUR-AUTHENTIK-URL/static/dist/assets/icons/icon.png
ENABLED = true
Auto Login = true or false (Your Preference)
Hostname = LEAVE EMPTY
Default = true
Client ID = AUTHENTIK-OAUTH-PROVIDER-CLIENT-ID-HERE
Client Secret = AUTHENTIK-OAUTH-PROVIDER-CLIENT-SECRET-KEY-HERE
Authorization URL = https://YOUR-AUTHENTIK-URL/application/o/authorize/
Token URL = https://YOUR-AUTHENTIK-URL/application/o/token
User Info URL = https://YOUR-AUTHENTIK-URL/application/o/userinfo
Scope = email profile openid ak_proxy # Enter One Per Line
Username Attributes = email
Groups Attributes = groups
```

Click Save.

### Edit OAuth PROVIDER

- Now Edit the OAuth Provider you just created in Kasm.
- Click on the tab for Attribute Mapping
- Click Add SSO Mapping
- Select Email for the first field
- Under Attribute enter email
- Click Save

### Edit Groups for SSO Mapping

- Navigate to Admin > Access Management > Groups
- Edit each group in Kasm that you have in Authentik
- In Each Group you want assigned to Kasm Users upon first login, click on the tab for SSO Group Mapping
- Click on Add SSO Mapping
- Select your newly created Authentik SSO Provider
- Choose if you want this assigned to all users or not
- If not assigned to all users, under Group Attributes, enter the name of the Group from Authentik you want assigned. **MUST BE IDENTICAL**

## Example

If you have an Authentik Group named "authentik Admins" or "Discord Users", then you would enter these exact names, spellings, and capitalizations into Kasm when creating new groups and assigning SSO Group Mapping Attributes

## Conclusion

You should now be able to login to Kasm with your new Authentik Login Button or it will automatically log you in if you decided to enable that. If you login with your Authentik Admin, it should assign you to the Admin Group of Kasm (if setup correctly).
