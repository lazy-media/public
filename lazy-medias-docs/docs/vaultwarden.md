---
description: >-
  Recommended Vaultwarden Docker setup, official references, and a legacy config
  example.
---

# Vaultwarden

### Overview

Use the official Vaultwarden image and env template for Docker installs.

That is the cleanest setup. It is also the most up to date.

### Recommended setup

For most installs:

1. Start with the official Vaultwarden repo.
2. Use the official `.env.template` as your base.
3. Set values with Docker environment variables.
4. Avoid a custom JSON config unless you need one.

### Official references

* [Dani Garcia Vaultwarden GitHub Repo](https://github.com/dani-garcia/vaultwarden)
* [Dani Garcia Vaultwarden ENV File](https://github.com/dani-garcia/vaultwarden/blob/53f58b14d5626abfcefd52586ec9e78d067a2334/.env.template)

{% hint style="info" %}
Use the official env template as the source of truth. It usually reflects new options faster than older examples.
{% endhint %}

### Settings worth reviewing first

When you build your config, review these first:

* `DOMAIN`
* Admin token
* SMTP settings
* Signup and invitation settings
* 2FA options
* Have I Been Pwned API key

### Legacy JSON config example

The example below is kept as a reference only.

I moved away from this approach after hitting issues and now use Docker variables instead.

If you use a JSON config, bind-mount it into the container and verify each value against the official docs first.

{% hint style="warning" %}
This example is not verified as current. Use it carefully and prefer environment variables when possible.
{% endhint %}

{% code title="config.json" expandable="true" %}
```json
// EXAMPLE VAULTWARDEN CONFIG FILE
// IF USING DOCKER, BIND MOUNT THE CONFIG FILE

{
    // ADMIN TOKEN SETTINGS
    // "admin_token": "$argon2i$v=00$m=00,t=0,p=0$ARGON_2_KEY$ARGON_2_KEY",
    // "admin_token": "YOUR_PLAIN_TEXT_ADMIN_TOKEN"
  
    // DOMAIN INFORMATION
    "domain": "https://vault.YOUR.DOMAIN",
    
    // Have I Been Pwnd API KEY
    "hibp_api_key": "YOUR_HAVE_I_BEEN_PWND_API_KEY",
  
    // Registration & Signup Settings
    "signups_allowed": true,
    "signups_verify": true,
    "signups_verify_resend_time": 3600,
    "signups_verify_resend_limit": 3,
    "signups_domains_whitelist": "YOUR.DOMAIN,aol.com,att.net,comcast.net,facebook.com,gmail.com,googlemail.com,google.com,hotmail.com,mac.com,me.com,mail.com,msn.com,live.com,sbcglobal.net,verizon.net,yahoo.com,bellsouth.net,charter.net;cox.net,earthlink.net,juno.com,owncloud.com,owncloud.net,owncloud.org,nextcloud.com,nextcloud.org,nextcloud.net",
    "invitations_allowed": true,
    "invitation_org_name": "VaultWarden",
  
    // Emergency Access Settings
    "emergency_access_allowed": true,
  
    // User Settings
    "email_change_allowed": true,
    "password_hints_allowed": true,
    "show_password_hint": true,
  
    // Security Settings
    "sends_allowed": true,
    "trash_auto_delete_days": 30,
    "disable_icon_download": false,
    "password_iterations": 600000,
    "require_device_email": true,
    "admin_session_lifetime": 20,
  
    // Network Security Settings
    "ip_header": "X-Real-IP",
    // "ip_header": "X-Forward-For",
    "http_request_block_non_global_ips": true,
  
    // 2FA Settings
    "_enable_email_2fa": true,
    "disable_2fa_remember": false,
    "authenticator_disable_time_drift": true,
    "incomplete_2fa_time_limit": 3,

    // Advanced 2FA Settings
    "two_factor_providers": ["email", "authenticator", "yubico", "duo"],
    "two_factor_remember_duration": 30,
  
    // DUO Security Settings
    "_enable_duo": false,
    "duo_ikey": "YOUR_DUO_IKEY",
    "duo_skey": "YOUR_DUO_SKEY",
    "duo_host": "api-fdaeafeasfe.duosecurity.com",
    "_duo_akey": "YOUR_DUO_AKEY",
  
    // Yubico Settings
    "_enable_yubico": false,
    "yubico_client_id": "YOUR_YUBICO_ID",
    "yubico_secret_key": "YOUR_YUBICO_KEY",
  
    // Email & SMTP Settings
    "_enable_smtp": true,
    "use_sendmail": false,
    "smtp_host": "smtp.gmail.com",
    "smtp_security": "starttls",
    "smtp_port": 587,
    "smtp_from": "no-reply@YOUR.DOMAIN",
    "smtp_from_name": "Vaultwarden",
    "smtp_username": "owner@YOUR.DOMAIN",
    "smtp_password": "YOUR_SMTP_PASSWORD",
    "smtp_auth_mechanism": "plain",
    "smtp_timeout": 15,
    "smtp_embed_images": true,
    "smtp_accept_invalid_certs": false,
    "smtp_accept_invalid_hostnames": false,
    "email_token_size": 6,
    "email_expiration_time": 600,
    "email_attempts_limit": 3,
    "email_2fa_enforce_on_verified_invite": false,
    "email_2fa_auto_fallback": false,
  
    // Database Settings
    // "database_url": "DATABASE_URL",
    // "database_max_conns": 10,
    // "database_connection_timeout": 30,
    // "database_use_wal": true,
    
    // Rocket Server Settings
    //  "rocket_port": 8000,
    //  "rocket_address": "0.0.0.0",
    //  "rocket_tls": {
    //    "certs": "PATH_TO_CERT",
    //    "key": "PATH_TO_KEY"
    // },
    // "rocket_log": "normal",

    // Additional Settings
    "icon_redirect_code": 302,
    "icon_cache_ttl": 2592000,
    "icon_cache_negttl": 259200,
    "icon_download_timeout": 10,
    "reload_templates": false,
    "log_timestamp_format": "%Y-%m-%d %H:%M:%S.%3f",
    "increase_note_size_limit": false
  
}


///////////////////////////////////////////////////////////////////////////////////////
///// USE THE VARIABLES BELOW AT YOUR OWN RISK. HAVE NOT VERIFIED THEY WORK YET!! /////
///////////////////////////////////////////////////////////////////////////////////////

    // Advanced Security Settings
    "disable_admin_token": false,
    "data_dir": "DATA_DIR_PATH",
    "attachments_dir": "ATTACHMENTS_DIR_PATH",
    "icon_service": "internal",
    "icon_blacklist_non_global_ips": true,

    // Logging Settings
    "log_level": "info",
    "log_file": "PATH_TO_LOG_FILE",
    "extended_logging": false,

    // Advanced Email Settings
    "smtp_helo_name": "localhost",
    "smtp_ssl_verify": true,

    // Advanced User Settings
    "user_attachment_limit": 500,
    "org_attachment_limit": 1000,
    "user_attachment_quota": 104857600,
    "org_attachment_quota": 1073741824,

    // Rate Limiting
    "rate_limit": {
        "enabled": true,
        "period": 60,
        "count": 10
    }
```
{% endcode %}
