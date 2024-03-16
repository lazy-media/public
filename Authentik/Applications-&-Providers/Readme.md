# Authentik WebUI Setup

## Setting Up Authentik with Cloudflare Certificates

### Prerequisites
1. Open two tabs or two browser windows for ease.
2. Login to your Authentik Admin Panel on one tab or window.
3. Login to your Cloudflare Account on the other.
4. Assumes your Cloudflare account already points to your Public IP Address and you have a DNS CNAME record set for Authentik.

### Cloudflare Setup

1. Login to your Cloudflare Account
2. Navigate to your Domain you want attached to Authentik.
3. Navigate to SSL/TLS > Origin Server
4. If no Origin Server Certificate exists, Create one.
