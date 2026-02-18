---
description: Setting up a UPS monitor on TrueNAS SCALE
---

# UPS Monitor Setup

### Overview

TrueNAS SCALE uses **NUT** (Network UPS Tools) for UPS management.

This setup gives you:

* Clean shutdown when power fails.
* A working NUT config you can query with `upsc`.
* Optional visual monitoring with the **Peanut / PeaNUT** app.

{% hint style="info" %}
Menu names can shift between SCALE releases. If you do not see **System Settings**, look for **System**.
{% endhint %}

### Before you start

* Plug the UPS into the TrueNAS host (USB or network).
* Know your UPS vendor and model.
* Plan a safe shutdown behavior for your environment.

{% hint style="warning" %}
Test shutdown behavior during a maintenance window. Do not “discover” your settings during a real outage.
{% endhint %}

### Step-by-step: configure the UPS service

{% stepper %}
{% step %}
### Open the UPS service settings

1. Log in to the TrueNAS SCALE admin UI.
2. Go to **System Settings → Services**.
3. Find **UPS**.
4. Click **Edit** (pencil icon).
{% endstep %}

{% step %}
### Fill in the core settings

Set these fields:

* **Identifier**: anything you want. Example: `ups`.
* **UPS Mode**: `Master`.
* **Monitor User**: anything you want. Example: `upsmon`.
* **Monitor Password**: use a strong password.
* **Driver**: pick the best match for your UPS.
* **Port or Hostname**: `auto` (works for most USB devices).
* **Remote Monitor**: enable if a client connects over the network.
* **Shutdown Mode**: choose your preference.
* **Shutdown Timer**: choose your preference.
* **Shutdown Command**: `shutdown -h 0`
* **Power Off UPS**: choose your preference.

{% hint style="info" %}
Driver choice matters the most. If readings look wrong, try another driver first.
{% endhint %}
{% endstep %}

{% step %}
### Save and enable the service

1. Click **Save**.
2. Toggle the **UPS** service to **Running**.
{% endstep %}
{% endstepper %}

### Verify with NUT commands (CLI)

Use the built-in NUT tools to confirm telemetry and status.

Official NUT docs: [NUT user manual](https://networkupstools.org/docs/user-manual.chunked/)

{% hint style="info" %}
Replace `<identifier>` with your **Identifier**. Example: `ups`.
{% endhint %}

```bash
# Query all variables from the local NUT server
upsc <identifier>@localhost

# Common fields you should see
upsc <identifier>@localhost ups.status
upsc <identifier>@localhost battery.charge
upsc <identifier>@localhost input.voltage

# List available instant commands (varies by UPS/driver)
upscmd -l <identifier>@localhost
```

{% hint style="warning" %}
Instant commands can cut power or start self-tests. Read the output of `upscmd -l` before running anything.
{% endhint %}

### Optional: visual monitoring with Peanut (PeaNUT)

Peanut (often styled **PeaNUT**) is a lightweight web UI for NUT. It connects to TrueNAS over the NUT port (`3493`).

#### Install Peanut

1. Go to **Apps**.
2. Install **Peanut / PeaNUT** from your catalog.
3.

    <figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
4. Use your normal Apps storage pattern (pool + dataset).

{% columns %}
{% column %}
<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>
{% endcolumn %}

{% column %}
<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### Add your TrueNAS NUT server in Peanut

In Peanut, click **Manage Servers** or **Add Server**.

Fill the form:

* **Name**: your UPS identifier. Example: `ups`.
* **Server Address**: TrueNAS IP or hostname.
* **Port**: `3493`
* **Username**: your **Monitor User**
* **Password**: your **Monitor Password**

Use the **⋯** menu under the password field. Select **Test**.

You should see a green indicator next to the server name.

Click **Apply**.

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If Peanut cannot connect, enable **Remote Monitor** in TrueNAS. Then restart the UPS service.
{% endhint %}

### Troubleshooting

#### No UPS data in `upsc`

* Re-check the **Driver**.
* Re-check **Port or Hostname**.
* Restart the UPS service after changes.

#### Peanut cannot connect

* Confirm the UPS service is **Running**.
* Confirm **Remote Monitor** is enabled (if connecting over LAN).
* Confirm you used port `3493`.
* Confirm the monitor username and password match.

#### You want remote access outside your LAN

Do not expose NUT directly to the internet. Use a VPN or a trusted internal reverse proxy pattern instead.
