---
description: >-
  Watchtower is a docker app that can update other docker apps by pulling new
  images, gracefully shutting down existing containers, and restarts with same
  options and new image.
---

# WatchTower

## Original Documentation

* [WatchTower Site](https://containrrr.dev/watchtower/)
* [WatchTower GitHub Repo](https://github.com/containrrr/watchtower)
* [WatchTower Update Error Fix](https://github.com/containrrr/watchtower/issues/2126)

## Installation

* This will be updated at a later time as the current documentation is good enough.

### Update Errors?

Are you getting an error saying:

```
Error response from daemon: client version 1.25 is too old
```

Fix it with:

Login in to your docker server via ssh with a user that has sudo privileges

Navigate to `/lib/systemd/system`

```bash
cd /lib/systemd/system
```

Edit the `docker.service` file with your editor choice or

```bash
sudo nano docker.service
```

Add the following under the `[Service]` section of the file

```
Environment=DOCKER_MIN_API_VERSION=1.24
```

Save the file and exit.&#x20;

{% hint style="info" %}
Nano Command = `CTRL + X` > `Y` > `ENTER`
{% endhint %}

Reload the Daemon Service

```bash
sudo systemctl daemon-reload
```

Restart the Docker Service

```bash
sudo systemctl restart docker
```
