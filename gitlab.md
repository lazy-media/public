---
description: Information on how to setup a Self Hosted GitLab Instance
---

# Gitlab

## Gitlab Omnibus Installation

### Notice

Please always try to refer to the official documentation as it will be the most up to date version to find information for Gitlab.

### Installation & Requirements

* Your system meets [Gitlab Self Hosting System Requirements](https://docs.gitlab.com/ee/install/requirements.html)
* Installed on Ubuntu 22.04
* Installed using the Linux Package (Omnibus) method
* Main Gitlab Config file is `/etc/gitlab/gitlab.rb`
* Root User access
* You have setup your DNS correctly and already have a URL pointing to your Gitlab Instance

### Original Documentation

* [Gitlab Omnibus Installation](https://about.gitlab.com/install/#ubuntu)
* [Gitlab Self Hosting System Requirements](https://docs.gitlab.com/ee/install/requirements.html)
* [Updating Gitlab Keys after Expiry](https://docs.gitlab.com/omnibus/update/package_signatures.html#update-keys-after-expiry-extension)

## Omnibus Installation Instructions

* Login as root user or non root user then switch to root user with `sudo su -`

#### Install and Configure Dependencies

```
apt-get update
```

```
apt-get install -y curl openssh-server ca-certificates tzdata perl
```

#### Add Gitlab Repository

```
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
```

#### Running Installation with Randomly Generated Password

**Change the `EXTERNAL_URL="https://gitlab.example.com"` to match your Gitlab Domain Name / URL you setup before running the command. Copy and Paste into a text document if needed to edit temporarily.**

#### Latest Version

```
sudo EXTERNAL_URL="https://gitlab.example.com" apt-get install gitlab-ee
```

#### Specific Version

```
sudo EXTERNAL_URL="https://gitlab.example.com" apt-get install gitlab-ee=16.2.3-ee.0
```

Pin the version to limit auto-updates

```
sudo apt-mark hold gitlab-ee
```

Show packages that are held back

```
sudo apt-mark showhold
```

#### Finding Initial Root Password

**YOU MUST GRAB THIS PASSWORD WITHIN THE FIRST 24 HOURS AFTER THIS IS CREATED**

```
nano /etc/gitlab/initial_root_password
```

### Run Install with Custom Root Password

**Change `<strongpassword>` to your own password**

```
sudo GITLAB_ROOT_PASSWORD="<strongpassword>" EXTERNAL_URL="http://gitlab.example.com" apt install gitlab-ee
```

## Updating Keys after Expiry Extension

This is needed in case you try to update and the you get an error about the signing keys being invalid.

#### Determining Type Of Update Method

To determine if you're using `apt-key` or `signed-by` update methods, run the following command

```
grep 'deb \[signed-by=' /etc/apt/sources.list.d/gitlab_gitlab-?e.list
```

You should get an output that is similar to, if using `signed-by`:

```
deb [signed-by=/usr/share/keyrings/gitlab_gitlab-ee-archive-keyring.gpg] https://packages.gitlab.com/gitlab/gitlab-ee/ubuntu/ jammy main
```

If using `apt-key` your output will be different.

#### Updating Keys

If using the `signed-by` method, run the following script as a root user

```
awk '/deb \[signed-by=/{
      pubkey = $2;
      sub(/\[signed-by=/, "", pubkey);
      sub(/\]$/, "", pubkey);
      print pubkey
    }' /etc/apt/sources.list.d/gitlab_gitlab-?e.list | \
  while read line; do
    curl -s "https://packages.gitlab.com/gpg.key" | gpg --dearmor > $line
  done
```

If using the `apt-key` method, run the following as a root user

```
apt-key del 3F01618A51312F3F
```

```
curl -s "https://packages.gitlab.com/gpg.key" | apt-key add -
```

```
apt-key list 3F01618A51312F3F
```

## Authentik OAuth2/OpenID & SAML Provider Setup

[Authentik OAuth2/OpenID & SAML Provider Setup](authentik/applications-and-providers.md#authentik-basic-oauth2-openid-setup)
