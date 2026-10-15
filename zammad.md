---
description: >-
  Install and configure Zammad with TrueNAS SCALE Apps, including the required
  proxy scheme setting.
---

# Zammad

## Zammad on TrueNAS SCALE

Use this guide to deploy Zammad through **TrueNAS SCALE Apps**. It covers the required container environment variable that prevents CSRF failures when Zammad runs behind HTTPS.

{% hint style="warning" %}
Set `NGINX_SERVER_SCHEME` before completing the initial Zammad setup. Its value must match the scheme users use in their browser.
{% endhint %}

### What you need

Before installation, prepare the following:

* A running TrueNAS SCALE system with access to **Apps**.
* A suitable app source that provides Zammad.
* Persistent storage for the application and its data services.
* A hostname or IP address for access.

For HTTPS access, also prepare a reverse proxy and a valid TLS certificate. The reverse proxy must forward requests to the Zammad app.

### Choose the access scheme

Zammad must know whether the public connection uses HTTP or HTTPS. Choose one value only.

| User access method            | Required variable     | Required value |
| ----------------------------- | --------------------- | -------------- |
| HTTPS through a reverse proxy | `NGINX_SERVER_SCHEME` | `https`        |
| Direct HTTP access            | `NGINX_SERVER_SCHEME` | `http`         |

{% hint style="info" %}
Use `https` whenever a reverse proxy terminates TLS. Do not use the internal container connection scheme.
{% endhint %}

### Install the app

{% stepper %}
{% step %}
#### Open the app catalog

In TrueNAS SCALE, open **Apps** and locate **Zammad** in the configured catalog. Select **Install**.
{% endstep %}

{% step %}
#### Set application details

Choose a recognizable application name. Select the desired storage, networking, and service options for your environment.

Use persistent datasets or volumes for all Zammad data. Do not rely on ephemeral container storage.
{% endstep %}

{% step %}
#### Add the environment variable

Find the app's container or workload environment settings. Add this variable to the Zammad container:

```
NGINX_SERVER_SCHEME=https
```

Use this value when users reach Zammad over HTTPS through a reverse proxy.

If users reach Zammad directly over HTTP, use:

```
NGINX_SERVER_SCHEME=http
```

Do not configure both values. Save the environment configuration.
{% endstep %}

{% step %}
#### Deploy Zammad

Review the installation form. Confirm the storage locations, network exposure, and environment variable. Select **Install**.

Wait until the app reports a healthy or running state.
{% endstep %}
{% endstepper %}

### Configure reverse proxy access

Use this section when the public Zammad URL uses HTTPS.

1. Create a proxy route for the Zammad hostname.
2. Forward the route to the Zammad service and port exposed by TrueNAS SCALE.
3. Enable TLS for the public hostname.
4. Confirm that the proxy forwards the original `Host` header.
5. Set `NGINX_SERVER_SCHEME=https` in the Zammad container.

After deployment, open the public HTTPS URL. Complete Zammad's first-run setup from that same URL.

{% hint style="warning" %}
Changing between HTTP and HTTPS later requires updating `NGINX_SERVER_SCHEME` and redeploying the app. Clear existing browser cookies if the prior session continues to fail.
{% endhint %}

### Verify the installation

After the app starts:

1. Open the public Zammad URL.
2. Confirm the page loads without redirects to an incorrect scheme.
3. Sign in or complete the initial administrator setup.
4. Create a test ticket or update a test setting.
5. Confirm the action completes without a CSRF error.

### Troubleshooting

#### CSRF errors after sign-in or form submission

A CSRF error usually means Zammad detects a different request scheme than the browser uses.

* For a public HTTPS URL, set `NGINX_SERVER_SCHEME=https`.
* For direct HTTP access, set `NGINX_SERVER_SCHEME=http`.
* Apply the setting to the Zammad container, then redeploy the app.
* Clear the browser cookies for the Zammad hostname before testing again.

#### Zammad opens with HTTP links behind HTTPS

Confirm that the reverse proxy provides HTTPS to visitors. Then verify `NGINX_SERVER_SCHEME` is exactly `https`, in lowercase. Redeploy after changing the variable.

#### The app does not start

Check the app events and container logs in TrueNAS SCALE. Verify storage paths are writable and that each required Zammad service is healthy. Resolve startup errors before exposing the service through a reverse proxy.

### Ongoing maintenance

Keep the app and TrueNAS SCALE updated. Back up every persistent dataset used by Zammad before upgrades. Test restores periodically, especially before major version updates.
