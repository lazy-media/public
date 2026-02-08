---
description: Information on how to scrape Authentik Metrics with Prometheus
---

# Prometheus Metrics for Authentik

### Overview

Configure Prometheus to scrape metrics from Authentik.

### Prerequisites / assumptions

{% hint style="info" %}
* Your Authentik Docker Compose setup is working.
* Metrics are exposed from Authentik.
  * If you followed these docs, uncomment `COMPOSE_PORT_METRICS` in your docker environment variables file.
  * See [Authentik Installation](authentik-installation.md) and [Docker Compose and ENV](authentik-installation.md#authentik-docker-compose-.env-and-geoip-override-files) for examples.
* You have Prometheus installed.
* You can locate and edit your Prometheus config file.
{% endhint %}

### Configure Prometheus scraping

Edit your Prometheus config file.

Mine is located at `/etc/prometheus/prometheus.yml`.

Add the following:

```
  - job_name: "Authentik Server"
    static_configs:
      - targets: ["INTERNAL.IP.OF.AUTHENTIK:9300"]
    metrics_path: "/metrics"
```

### Restart Prometheus

Restart the Prometheus service:

```
systemctl restart prometheus
```
