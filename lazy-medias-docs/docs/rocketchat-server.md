---
description: RocketChat Server is a self hosted alternative to Slack.
---

# Rocket-Chat Server

### Overview

Rocket.Chat is a self-hosted chat platform.

This install uses the official `rocketchat-server` Snap on Ubuntu.

{% hint style="info" %}
Run commands as a user with `sudo` access.
{% endhint %}

### Prerequisites

* Ubuntu Server 22.04 or later
* `snapd` installed (usually automatic on Ubuntu Server)
* SSH access to the server
* Basic comfort with Ubuntu + Snap

#### Recommended (but optional)

* A DNS name for Rocket.Chat
* A reverse proxy for HTTPS and easy access
* Outbound email (SMTP) for invites and password resets

### Install Rocket.Chat

{% stepper %}
{% step %}
### Install the Snap

```bash
sudo snap install rocketchat-server
```
{% endstep %}

{% step %}
### Confirm it’s running

Check the service status:

```bash
sudo snap services rocketchat-server
```

If it’s not running, start it:

```bash
sudo snap start rocketchat-server
```
{% endstep %}

{% step %}
### Open the web UI

Open Rocket.Chat in your browser. Use your server IP or hostname.

If you put it behind a reverse proxy, use the public URL.
{% endstep %}
{% endstepper %}

### Post-install checklist

Do these early. They prevent most “later” pain.

1. Create the first admin account.
2. Set the site URL in Rocket.Chat settings.
3. Configure SMTP for email delivery.
4. Decide how you’ll handle HTTPS (reverse proxy strongly recommended).
5. Plan backups before inviting users.

### Reverse proxy + HTTPS (recommended)

Put Rocket.Chat behind a reverse proxy if you can.

It simplifies HTTPS. It keeps URLs predictable.

Minimum checklist:

* Create a DNS record (for example `chat.yourdomain.tld`).
* Terminate TLS at the proxy.
* Forward traffic to the Rocket.Chat service on the host.
* Set Rocket.Chat’s “Site URL” to the public `https://…` URL.

{% hint style="warning" %}
If your “Site URL” is wrong, OAuth, invites, and redirects get weird fast.
{% endhint %}

### Updates

Snaps typically refresh automatically. You can also refresh manually:

```bash
sudo snap refresh rocketchat-server
```

### Logs

If the UI won’t load or setup fails, look at the service logs first:

```bash
sudo snap logs -f rocketchat-server
```

### Backups (minimum viable)

Back up Rocket.Chat’s Snap data directory.

Check this first during restores.

1. Stop Rocket.Chat.
2. Back up `/var/snap/rocketchat-server/common`.
3. Start Rocket.Chat.

```bash
sudo snap stop rocketchat-server
```

```bash
sudo tar -czf rocketchat-snap-backup.tgz /var/snap/rocketchat-server/common
```

```bash
sudo snap start rocketchat-server
```

{% hint style="warning" %}
Always test restores. A backup you never restored is a guess.
{% endhint %}

### Uninstall

Remove Rocket.Chat:

```bash
sudo snap remove rocketchat-server
```

{% hint style="warning" %}
Uninstall removes the Snap. Make sure you have backups first.
{% endhint %}

### Resources

* [Rocket.Chat Documentation](https://docs.rocket.chat/)
* [Rocket.Chat GitHub](https://github.com/RocketChat/Rocket.Chat)
* [Rocket.Chat Community Forum](https://forums.rocket.chat/)

### Troubleshooting

#### Locked out of Rocket-Chat Server due to 2FA?

Login to your Ubuntu Server.

Create the file for `2fa_disable.env` and write information into it with one of the following commands.

{% tabs %}
{% tab title="tee" %}
{% code overflow="wrap" %}
```bash
echo -e "environment:\n  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enforce_Password_Fallback=false\n  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enabled=false" | sudo tee /var/snap/rocketchat-server/common/2fa_disable.env
```
{% endcode %}
{% endtab %}

{% tab title="cat" %}
{% code overflow="wrap" %}
```bash
sudo bash -c 'cat > /var/snap/rocketchat-server/common/2fa_disable.env << EOF
environment:
  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enforce_Password_Fallback=false
  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enabled=false
EOF'
```
{% endcode %}
{% endtab %}

{% tab title="printf" %}
{% code overflow="wrap" %}
```bash
sudo sh -c 'printf "environment:\n  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enforce_Password_Fallback=false\n  OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enabled=false\n" > /var/snap/rocketchat-server/common/2fa_disable.env'
```
{% endcode %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If this doesn’t take effect, re-check the file formatting. The tabbed commands above are the safest to copy/paste.
{% endhint %}

Or do it manually. Change directory into the folder, create the file, paste the content, and save it.

```bash
cd /var/snap/rocketchat-server/common
```

```bash
sudo nano 2fa_disable.env
```

Enter the following into the file:

```dotenv
enviroment:
OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enforce_Password_Fallback=false
OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enabled=false
```

Save the file with `CTRL + X` > `Y` > `ENTER`

Restart the Rocket-Chat Server:

```bash
sudo snap restart rocketchat-server
```
