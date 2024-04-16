# Grafana OpenID / OAuth Setup with Authentik

## NOTES:

I only use Authentik as my Reverse proxy and I have the Standalone version of Grafana installed, not the docker version.

## Grafana Setup

edit the config file

```
#################################### Server ####################################
[server]
# Protocol (http, https, h2, socket)
protocol = http
protocol_https = https

# This is the minimum TLS version allowed. By default, this value is empty. Accepted values are: TLS1.2, TLS1.3. If nothing is set TLS1.2 would be taken
;min_tls_version = ""

# The ip address to bind to, empty will bind to all interfaces
http_addr = IP.ADDRESS.OF.GRAFANA

# The http port  to use
http_port = 3000

# The public facing domain name used to access grafana from a browser
domain = grafana.domain.example

# Redirect to correct domain if host header does not match domain
# Prevents DNS rebinding attacks
;enforce_domain = true

# The full public facing url you use in browser, used for redirects and emails
# If you use reverse proxy and sub path specify full url (with sub path)
root_url = %(protocol)s://%(http_addr)s:%(http_port)s/
root_url = %(protocol_https)s://%(domain)s/
```

Scroll down the `AUTH` section of the config file and input

```
[auth]
signout_redirect_url = https://auth.domain.example/application/o/OAUTH-SLUG/end-session/
# Optionally enable auto-login
oauth_auto_login = false

[auth.generic_oauth]
name = authentik
enabled = true
client_id = REDACTED
client_secret = REDACTED
scopes = openid email profile
auth_url = https://auth.domain.example/application/o/authorize/
token_url = https://auth.domain.example/application/o/token/
api_url = https://auth.domain.example/application/o/userinfo/
# Optionally map user groups to Grafana roles
role_attribute_path = contains(groups, 'authentik Admins') && 'Admin' || contains(groups, 'Grafana Editors') && 'Editor' || 'Viewer'
```

## Authentik Setup

Make Group for `Grafana Editors`
