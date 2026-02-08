---
description: Nextcloud Self Hosted Setup Instructions
---

# Nextcloud

## Nextcloud

{% hint style="danger" %}
LAZY MEDIA HAS SINCE CONVERTED TO USING THE NEXTCLOUD APP PROVIDED BY TRUENAS SCALE.

THIS DOCUMENTATION REFERENCES HOW TO USE THE SNAP PACKAGE FROM UBUNTU.
{% endhint %}

### References

* [Imagick Setup](https://link.lazymedia.media/YdFfX)

### Prerequisites

* Ubuntu Server 22.04 or really any Ubuntu Version you want with Snap preinstalled
* Installed via Snap / Snapd

### SNAP Package Installation

```
sudo snap install nextcloud
```

### Imagick Installation and Setup for Favicon

{% hint style="danger" %}
DOCUMENTATION AFTER THIS POINT MAY NOT BE ACCURATE, PLEASES USE AT YOUR OWN RISK OR HELP UPDATE THE DOCS TO REFLECT THE CORRECT METHOD.
{% endhint %}

#### Install PHP Requirements

```
sudo apt install php php-common gcc
```

#### Install Imagemagick

```
sudo apt install imagemagick
```

#### Install PHP Module Imagick

```
sudo apt install php-imagick
```

#### Restart Webserver

Apache2

```
sudo systemctl restart apache2
```

NGINX

```
sudo systemctl restart nginx
```

#### Verify Installation

```
php -m | grep imagick
```

### OpenID / OAuth Setup

Visit [Authentik Nextcloud OpenID / OAuth Setup](authentik/nextcloud.md)
