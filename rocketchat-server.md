---
description: RocketChat Server is a self hosted alternative to Slack.
---

# Rocket-Chat Server

### Prerequisites

* Ubuntu Server 22.04 or later
* Snapd installed (automatic if installing Ubuntu Server from ISO file)
* Basic knowledge of SSH, Ubuntu, and SNAP

### Installation

Login to your Ubuntu Server via ssh with a user that has the ability to run commands with sudo privileges.

Install the Rocket-Chat Server:

```bash
sudo snap install rocketchat-server
```

#### Locked out of Rocket-Chat Server due to 2FA?

Login to your Ubuntu Server

Create the file for `2fa_disable.env` and write information into it with one of the following commands

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

or if you prefer to do it manually you can change directory into the folder, create the file, write / copy the information into the file, and then save it.

```bash
cd /var/snap/rocketchat-server/common
```

```bash
sudo nano 2fa_disable.env
```

Enter the following into the file

```dotenv
enviroment:
OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enforce_Password_Fallback=false
OVERWRITE_SETTING_Accounts_TwoFactorAuthentication_Enabled=false
```

Save the file with `CTRL + X` > `Y` > `ENTER`

Restart the Rocket-Chat Server with:

```bash
sudo snap restart rocketchat-server
```

