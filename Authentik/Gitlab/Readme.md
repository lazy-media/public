# GitLab Installation

- Installed on Ubuntu Server 22.04
- Installed via Gitlab Documentation for Linux Package (Omnibus)

# Original documentation

- [Gitlab Installation](https://docs.gitlab.com/omnibus/installation/index.html)
- [Authentik Setup](https://docs.goauthentik.io/integrations/services/gitlab/)

## Adding OAuth to Gitlab Config File

Login and edit the Gitlab Ruby Config File

```
nano /etc/gitlab/gitlab.rb
```
The following lines are basic config options for OAuth or SAML Login
Add the following lines to the config file or search for them in the config
Change the 'openid_connect' to either 'openid_connect' or 'saml'
```
gitlab_rails['omniauth_enabled'] = true
gitlab_rails['omniauth_allow_single_sign_on'] = ['openid_connect']
gitlab_rails['omniauth_sync_email_from_provider'] = 'openid_connect'
gitlab_rails['omniauth_sync_profile_from_provider'] = ['openid_connect']
gitlab_rails['omniauth_sync_profile_attributes'] = ['email']
gitlab_rails['omniauth_block_auto_created_users'] = false
```

To have your Provider login automatically instead of stopping at Gitlab's Main Login page, add the following line:
```
gitlab_rails['omniauth_auto_sign_in_with_provider'] = 'openid_connect'
```

For OpenID / OAuth2 add the following and change anything that is necessary
```
gitlab_rails['omniauth_providers'] = [
  { 'name' => 'openid_connect',
    'label' => 'YOUR-LOGIN-DISPLAY-NAME',
    'icon' => 'https://YOUR-AUTHENTIK-URL/static/dist/assets/icons/icon.png',
    'args' => {
      'name' => 'openid_connect',
      'scope' => ['openid','profile','email'],
      'response_type' => 'code',
      'issuer' => 'https://YOUR-AUTHENTIK-URL/application/o/YOUR-GITLAB-OAUTH-PROVIDER-SLUG/',
      'discovery' => true,
      'client_auth_method' => 'query',
      'uid_field' => 'email',
      'send_scope_to_token_endpoint' => 'false',
      'client_options' => {
        'identifier' => 'YOUR-AUTHENTIK-OPENID-PROVIDER-ID',
        'secret' => 'YOUR-AUTHENTIK-OPENID-PROVIDER-SECRET-KEY',
        'redirect_uri' => 'https://YOUR-GITLAB-URL/users/auth/openid_connect/callback'
      }
    }
  }
]
```

Save and exit with CTRL + O then CTRL + X or CTRL + X, Then 'Y', Then ENTER

### Update GitLab Config to apply Changes

Enter the following to update Gitlab Rails Config and apply the changes
```
gitlab-ctl reconfigure
```
Your new OpenID / OAuth2 Provider should now show up on your Gitlab Login Page or Automatically login.


## Add SAML to GitLab

Login and edit your GitLab Ruby Config File
```
nano /etc/gitlab/gitlab.rb
```

The following lines are from the above Basic omniauth provider settings and changed for SAML
```
gitlab_rails['omniauth_enabled'] = true
gitlab_rails['omniauth_allow_single_sign_on'] = ['saml']
gitlab_rails['omniauth_sync_email_from_provider'] = 'saml'
gitlab_rails['omniauth_sync_profile_from_provider'] = ['saml']
gitlab_rails['omniauth_sync_profile_attributes'] = ['email']
gitlab_rails['omniauth_auto_sign_in_with_provider'] = 'saml'
gitlab_rails['omniauth_block_auto_created_users'] = false
```
Add the following lines to your GitLab Config File and change what is necessary
```
gitlab_rails['omniauth_auto_link_saml_user'] = true
gitlab_rails['omniauth_providers'] = [
  {
    name: 'saml',
    args: {
      assertion_consumer_service_url: 'https://YOUR-GITLAB-URL/users/auth/saml/callback',
      # Shown when navigating to certificates in authentik
      idp_cert_fingerprint: 'YOUR-AUTHENTIK-CERTIFICATE-FINGERPRINT',
      idp_sso_target_url: 'https://YOUR-AUTHENTIK-URL/application/saml/YOUR-AUTHENTIK-SAML-PROVIDER-SLUG/sso/binding/redirect/',
      issuer: 'https://YOUR-GITLAB-URL',
      name_identifier_format: 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent',
      attribute_statements: {
        email: ['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'],
        first_name: ['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'],
        nickname: ['http://schemas.goauthentik.io/2021/02/saml/username']
      }
    },
    label: 'YOUR-LOGIN-NAME-SHOWN-ON-MAIN-LOGIN'
  }
]
```

### Update GitLab Config to apply Changes

Enter the following to update Gitlab Rails Config and apply the changes
```
gitlab-ctl reconfigure
```
Your new SAML Provider should now show up on your Gitlab Login Page or Automatically login.
