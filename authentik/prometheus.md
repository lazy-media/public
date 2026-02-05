---
description: Information on how to scrape Authentik Metrics with Prometheus
---

# Prometheus Metrics for Authentik

## Purpose

This will help you setup Prometheus to gather metrics from Authentik.

## Assumptions

* Assumes you have the Authentik Docker Compose file setup correctly, and make sure you have the ports set in your docker environment variables file. If you followed my instructions, you should just need to Uncomment the `COMPOSE_PORT_METRICS` line in your docker environment variables file.
* Assumes you have the standalone version of prometheus installed or you know where your config file is located to edit, if it differs from mine.

## Prometheus Setup

Edit your prometheus config file. Mine is found at `/etc/prometheus/prometheus.yml`

Add the following to the file:

```
  - job_name: "Authentik Server"
    static_configs:
      - targets: ["INTERNAL.IP.OF.AUTHENTIK:9300"]
    metrics_path: "/metrics"
```

## Restart Prometheus

```
systemctl restart prometheus
```
