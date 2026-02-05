---
description: Nextcloud Self Hosted Setup Instructions
---

# Nextcloud Setup

## IMAGICK SETUP NOT CURRENTLY WORKING WITH NEXTCLOUD...STILL WORKING ON FIGURING THIS OUT.

## References

* [Imagick Setup](https://link.lazymedia.media/YdFfX)

## Prerequisites

* Ubuntu Server 22.04 or really any Ubuntu Version you want with Snap preinstalled
* Installed via Snap / Snapd

## Installation

```
sudo snap install nextcloud
```

## Imagick Installation and Setup for Favicon

### Install PHP Requirements

```
sudo apt install php php-common gcc
```

### Install Imagemagick

```
sudo apt install imagemagick
```

### Install PHP Module Imagick

```
sudo apt install php-imagick
```

### Restart Webserver

Apache2

```
sudo systemctl restart apache2
```

NGINX

```
sudo systemctl restart nginx
```

### Verify Installation

```
php -m | grep imagick
```
