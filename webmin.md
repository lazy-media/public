---
description: Information on how to install Webmin for Linux Servers
---

# Webmin

## Documentation

[Webmin Website](https://webmin.com/)

## Install Dependencies

```
apt update && apt upgrade -y
```

```
apt install curl -y
```

## Install Webmin Repository

```
curl -o setup-repos.sh https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh
```

## Install Webmin

```
apt-get install -y --install-recommends webmin
```
