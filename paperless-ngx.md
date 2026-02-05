---
description: Information on how to setup Paperless-NGX Self Hosted
---

# Paperless-NGX

## Installation Process

## Original Documentation / Website

* [Paperless NGX](https://docs.paperless-ngx.com)

### Login

Login as root user

### Update System

```
apt update && apt dist-upgrade -y
```

#### Install CA-Certificates and Curl

```
sudo apt-get install -y ca-certificates curl
```

### Install Docker and Docker Compose Plugin

Setup Docker's Official GPG Key:

```
apt-get update
```

```
install -m 0755 -d /etc/apt/keyrings 
```

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
```

```
chmod a+r /etc/apt/keyrings/docker.asc
```

Add Docker Repository to APT Sources:

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Run an Update

```
apt-get update
```

Install Docker

```
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Create Non-Root User with no password with Docker Privledges

Replace 'YOURUSER' with the name of a user you want

```
adduser YOURUSER --disabled-password
```

Fill in your information if you want or just press ENTER until the end then press Y to Confirm account creation

Now Add this user to the docker group

```
usermod -aG docker YOURUSER
```

### Switch to new User

```
su - YOURUSER
```

### Install Paperless-NGX using Easy Install

```
bash -c "$(curl --location --silent --show-error https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/install-paperless-ngx.sh)"
```

Fill out the information as told in the setup steps.

### Example Paperless Docker Compose and Docker Compose Environment Files

{% tabs %}
{% tab title="Basic Docker Compose" %}
{% include ".gitbook/includes/paperless-ngx-basic-docker-compose-file.md" %}
{% endtab %}

{% tab title="OpenID Docker Compose" %}
{% include ".gitbook/includes/paperless-ngx-with-openid-docker-compose-file.md" %}
{% endtab %}

{% tab title=".env.example" %}
{% include ".gitbook/includes/paperless-ngx-example-environment-variables-file.md" %}
{% endtab %}
{% endtabs %}

## Authentik OAuth / OpenID Setup

Please visit [Paperless-NGX OAuth Setup](authentik/paperless-ngx.md)
