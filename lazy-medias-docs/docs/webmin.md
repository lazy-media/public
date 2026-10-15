---
description: Install Webmin on Debian or Ubuntu with the official repository.
---

# Webmin

### Overview

This installs Webmin on a Debian or Ubuntu server.

Webmin provides a browser-based admin panel for Linux system management.

### Official site

* [Webmin Website](https://webmin.com/)

### Before you start

Make sure:

* You have shell access with `sudo` or root.
* The server can reach the internet.
* Port `10000` is allowed through your firewall.

{% hint style="info" %}
Webmin usually listens on `https://<server-ip>:10000`.
{% endhint %}

### Install Webmin

{% stepper %}
{% step %}
### Update the system

Refresh package metadata and install available updates.

```bash
apt update && apt upgrade -y
```
{% endstep %}

{% step %}
### Install `curl`

Install `curl` if it is not already present.

```bash
apt install curl -y
```
{% endstep %}

{% step %}
### Add the Webmin repository

Download and run the official repository setup script.

```bash
curl -o setup-repos.sh https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh
```
{% endstep %}

{% step %}
### Install Webmin

Install the package from the configured repository.

```bash
apt-get install -y --install-recommends webmin
```
{% endstep %}
{% endstepper %}

### Access Webmin

After the install finishes, open Webmin in your browser:

```
https://<server-ip>:10000
```

Log in with a system account that has the required privileges.

{% hint style="warning" %}
The first connection may show a browser certificate warning. That is common if you have not installed a trusted certificate yet.
{% endhint %}

### Quick validation

If the page does not load, check these first:

* The install completed without errors.
* Port `10000` is open.
* The server IP is correct.
* Local firewall rules are not blocking access.
