---
description: Information on how to install Docker Engine with three different methods.
---

# Docker Engine Installation

### Overview

This page covers a basic Docker Engine install on Linux. It includes **three install methods**. Pick **one** method and follow it end-to-end.

{% hint style="info" %}
Run these commands on the Docker host. Use a user with `sudo` access.
{% endhint %}

### 1) Prepare the host

#### Update system packages

```bash
sudo apt update && apt upgrade -y
```

{% hint style="info" %}
If the upgrade step errors due to permissions, run `sudo apt upgrade -y` as a separate command.
{% endhint %}

#### Install dependencies

```bash
sudo apt install -y ca-certificates curl
```

### 2) Install Docker (choose one method)

{% hint style="warning" %}
Only use **one** of the methods below. Mixing methods often causes broken upgrades.
{% endhint %}

{% include "https://app.gitbook.com/s/7ikPxOwA5dG7rGhQmIXN/~/reusable/UQARq3EjzOHi6XgEx5mi/" %}

### 3) Validate the installation

Check that Docker is installed and responding:

```bash
docker --version
```

If you plan to run containers as your user, add yourself to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Log out and back in, then verify:

```bash
docker ps
```

### Optional: NVIDIA Container Toolkit (GPU support)

[Visit this site to view instructions temporarily until I can update this](https://www.gravee.dev/en/setup-nvidia-gpu-for-docker/)
