---
description: Logs changes made to the documentation
---

# Changelog

{% updates format="full" %}
{% update date="2026-06-16" %}
## Added Resource Link

* Added a new footer link to a resources page for Subaru Impreza, WRX, and STI owners.
  * The page includes publicly available owners and service manuals for select model years, with more years planned later.
  * [Subaru Impreza, WRX & STI Owners and Service Manuals](https://site.lazymedia.media/subaru-manuals)
{% endupdate %}

{% update date="2026-03-14" %}
## Documentation Updates

* Replaced the retired Bitcoin donation address with the current active address.
* Updated [Donations & Sponsors](donations-and-sponsors.md) to improve the Bitcoin donation section:
  * Restyled BTCPay links as matching button-style badges.
  * Added a BTCPay contact button for payment questions and custom requests.
  * Split Bitcoin donations into a dedicated two-column section for better readability.
{% endupdate %}

{% update date="2026-02-23" %}
## Documentation and Policy Updates

* Updated [Donations & Sponsors](donations-and-sponsors.md) for improved readability and navigation.
* Expanded [Cookie Policy](joining-lazy-medias-server/cookie-policy.md) to cover:
  * Analytics and link measurement (Google, Umami, Tianji, Shlink).
  * Monitoring and metrics tooling (Grafana, Prometheus, InfluxDB, and similar systems).
  * Support and store experiences (Odoo support portal, WordPress store).
  * Payments (PayPal and Stripe) and UniFi/Ubiquiti network infrastructure assumptions.
  * Coverage for additional internal services beyond those listed in the docs.
* Expanded [Privacy Policy](joining-lazy-medias-server/privacy-policy.md) to reflect the same ecosystem assumptions (analytics, monitoring, support/store, UniFi), and documented backup retention:
  * Daily backups retained for 7 days.
  * Weekly backups retained for 2 weeks.
* Updated [Terms of Service](joining-lazy-medias-server/terms-of-service.md) to align scope with the documented services and the broader internal stack, and to reference PayPal/Stripe processing terms where applicable.
{% endupdate %}

{% update date="2026-02-18" %}
## Added Documentation

* Added a full guide for [UPS Monitor Setup](../truenas-scale/ups-monitor-setup.md) under TrueNAS SCALE.
  * Includes step-by-step UPS service config, NUT verification commands (`upsc`, `upscmd`), and troubleshooting.
  * Includes optional Peanut/PeaNUT visual monitoring steps with screenshot placeholders.
{% endupdate %}

{% update date="2026-02-17" %}
## Added Documentation

* Added [Bridged Networking (VM LAN Access)](../truenas-scale/bridged-networking-vm-lan-access.md) under TrueNAS SCALE, documenting bridge interface setup for VMs that need access to SMB shares hosted on the same server.
{% endupdate %}

{% update date="2026-02-15" %}
## Added Documentation

* Added a note for unlocking Proxmox VMs and LXCs for quick referencing
{% endupdate %}

{% update date="2026-02-11" %}
## Added Documentation

* Added Information on [Wordpress](../wordpress.md)
  * basic fixes for some common issues
{% endupdate %}

{% update date="2026-02-08" %}
## Documentation Updates

* Added Dockerfile for [ReType](../docker/dockerfiles/retype.md) just as a reference.
  * Suggested as an alternative for GitBook, but doesn't meet all requirements Lazy Media is looking for.
* Update some more documentation to fix broken or missing links
* Updated [Proxmox](../proxmox.md) page to look more "professional"
* Updated [Rocket.Chat](../rocketchat-server.md) page to look more "professional"
* Updated [Windows 11](../windows-11.md) page to look more "professional"
* Added a [Cookie Policy](joining-lazy-medias-server/cookie-policy.md), [Privacy Policy](joining-lazy-medias-server/privacy-policy.md) & [Terms of Service](joining-lazy-medias-server/terms-of-service.md) that only applies when you actually use a Lazy Media hosted service or log in via Lazy Media SSO
  * This is just for a reference that is always online to Lazy Media Users.
{% endupdate %}

{% update date="2026-02-06" %}
## Documentation Updates

* Added Quick Documentation for [Dockhand Docker Management Tool](../docker/docker-management-tools/dockhand-docker-management.md)
* Updated GitHub Repository with appropriately named files.
* Added Documentation for [Rocket-Chat Server Setup](../rocketchat-server.md)
* Removed `Need A Resume?` Page and combined with the [Reactive Resume Page](../reactive-resume.md)
* Updated more documentation and fixed more links.
* Updated some Authentik documentation to acknowledge it is outdated and needs updating
* Added Warning and Info notes to those pages to let users know.
* Separated Home lab sections into their own pages.
* Added additional Proxmox Servers to Home lab
* Added some documentation for [WatchTower](../docker/docker-management-tools/watchtower.md)
* Had GitBook AI Agent Help make the some of the documentation more professional looking and easier to read for users without changing the content that was already present. _More to come.._
{% endupdate %}

{% update date="2026-02-05" %}
## Documentation Updates

* Updated more information on the documentation
* Added GitLab Integration to push new documentation site directory structure to push to GitHub (one time process to overwrite current information on GitHub)
* GitHub Public Repo has been updated to reflect new GitBook Structure
* Fixed links to be local to GitBook instead of redirecting to GitHub content that doesn't exist
* Separated Donations / Sponsors Page
* Separated Join Lazy Media's Server to a new page.
{% endupdate %}

{% update date="2026-02-04" %}
## GitBook Integration

* Implemented GitBook into [Lazy Media's Public GitHub Repository](https://github.com/lazy-media/public)
* Added a new URL for permanent documentation site: [https://docs.lazymedia.media](https://docs.lazymedia.media/)
* Updating Documentation to look and feel more professional
* Enabled more than 30 different languages for the documentation site
* Implemented AI Search into the Public Documentation Site
* Implemented a Status Badge for the Plex Server Status for a better "Live" Status report
* Reorganization of the Documentation is under way, please be patient for this to be completed
{% endupdate %}

{% update date="2026-01-29" %}
## Email Issue Fixed

* Email issue with not being able to receive emails
* Fixed email issue
* All emails are successfully being received and delivered
{% endupdate %}
{% endupdates %}
