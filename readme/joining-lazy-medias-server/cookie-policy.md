---
description: >-
  How Lazy Media uses cookies and similar technologies across hosted apps, SSO,
  and related services.
---

# Cookie Policy

### Last updated

2026-02-22

### Who this is for

This Cookie Policy (“Policy”) applies to Lazy Media (“we”, “us”).

It applies when you use any Lazy Media hosted app or service.

It also applies when you use Lazy Media single sign-on (SSO).

SSO is primarily handled by [Authentik](../../authentik/).

{% hint style="info" %}
Lazy Media runs 100+ self-hosted services.

Not all services are public.

This Policy applies to any Lazy Media service you access, whether public or internal.
{% endhint %}

### Related documents

This Policy should be read with:

* [Privacy Policy](privacy-policy.md)
* [Terms of Service](terms-of-service.md)

If this Policy conflicts with the Privacy Policy, the Privacy Policy controls for privacy topics.

### Services covered

This Policy covers use of Lazy Media services documented here:

* [Joining Lazy Media's Server](./)
* [Authentik](../../authentik/)
* [Immich](../../immich.md)
* [Nextcloud](../../nextcloud.md)
* [Paperless-NGX](../../paperless-ngx.md)
* [Vaultwarden](../../vaultwarden.md)
* [Rocket-Chat Server](../../rocketchat-server.md)
* [Mastodon](../../mastodon.md)
* [Vikunja](../../vikunja.md)
* [Kasm Workspaces](../../kasm.md)
* [Jellyfin](../../jellyfin.md)
* [Gitlab](../../gitlab.md)
* [Reactive Resume](../../reactive-resume.md)
* [Cal.com Appointment & Scheduling](../../cal.com-appointment-and-scheduling.md)
* [Pterodactyl](../../pterodactyl-gaming-server.md)
* [FiveM Server Setup with TX Admin](../../fivem.md)
* [WordPress](../../wordpress.md)

{% hint style="info" %}
Some pages describe self-hosting guides or internal infrastructure. This Policy applies when you use a Lazy Media hosted service or Lazy Media SSO.
{% endhint %}

### Extra services assumed by this documentation

This documentation references a broader ecosystem than the pages list can capture.

Assume the following also exist and may use cookies or similar storage:

* A **support portal** based on **Odoo (open source)**.
* A **store site** based on **WordPress** (often with e-commerce plugins).
* A **link shortener / link analytics** stack (for example, Shlink).
* A **monitoring / observability** stack (for example, Grafana, Prometheus, InfluxDB).
* A **network infrastructure** stack based on **UniFi / Ubiquiti**.

If you access any of these via a browser, expect session cookies and security tokens.

### What cookies are

Cookies are small text files stored on your device.

They help websites and apps remember sessions, settings, and preferences.

We also use similar technologies that behave like cookies:

* Local storage and session storage.
* Tokens stored in your browser.
* Pixel tags and embedded content that can set identifiers.

For simplicity, we refer to all of these as “cookies” in this Policy.

### Why we use cookies

We use cookies for the following purposes:

* **Security and authentication.**
* **Service functionality and preferences.**
* **Reliability and performance troubleshooting.**
* **Abuse prevention and rate limiting.**
* **Analytics and link measurement** (where enabled and legally permitted).

Some cookies are required to make the services work.

If you block required cookies, parts of the services may not function.

### Types of cookies we use

#### 1) Strictly necessary cookies

These are required for core features.

Typical uses include:

* Maintaining login sessions (including SSO sessions).
* CSRF protection.
* Load balancing and routing.
* Fraud and abuse prevention.

These cookies are usually set automatically when you use the service.

#### 2) Functional cookies

These support non-essential features.

Typical uses include:

* Remembering display preferences (theme, language, layout).
* Remembering app configuration choices.
* Keeping you signed in longer, when supported.

#### 3) Performance and diagnostics cookies

These help us understand reliability issues.

Typical uses include:

* Error reporting and debugging.
* Measuring service performance.
* Detecting outages and degraded performance.

Where possible, we prefer aggregated and minimal data.

#### 4) Analytics cookies (if enabled)

We may use analytics to understand general usage patterns.

If we use non-essential analytics cookies, we aim to:

* Use them only with consent where required by law.
* Collect data at a level appropriate for operations and planning.

{% hint style="info" %}
Not every Lazy Media service uses every category above. Many self-hosted apps rely mainly on session and security cookies.
{% endhint %}

### Analytics, link tracking, and stats tooling

Lazy Media may run first-party and third-party analytics.

This can apply to the docs site, the support portal, the store, and any public app.

#### Analytics providers (assumed)

Depending on the site and configuration, we may use:

* **Google** analytics and advertising measurement tools.
* **Umami** (self-hosted analytics).
* **Tianji** (self-hosted analytics and monitoring).
* **Shlink** (short links and click analytics).

We may also run other self-hosted analytics, telemetry, or logging tools.

#### What these tools can store

These tools can use cookies or similar storage for:

* A pseudonymous identifier (repeat visits).
* Session state (single visit grouping).
* Attribution (referrer, campaign parameters).
* Abuse prevention and bot filtering.

Some configurations may be cookie-less.

Even then, server logs may still record click or pageview events.

{% hint style="info" %}
This docs site uses short links (for example, `links.lazymedia.media`).

When you click them, the short-link service can log the click.

It may also set cookies if it serves an interactive page.
{% endhint %}

### Monitoring, metrics, and admin dashboards

Lazy Media uses monitoring and metrics tools to keep services stable.

Examples include **Grafana**, **Prometheus**, and **InfluxDB**.

If you access these web UIs, they commonly use cookies for:

* Login sessions (including SSO-backed sessions).
* CSRF protection.
* UI preferences (theme, time range, last dashboard).

Prometheus itself is often cookie-free.

Grafana is the most likely to set browser cookies.

We may also run other observability tools for logs, tracing, and uptime checks.

### Third‑party cookies and embedded content

Some pages or services may include third‑party components.

Those third parties may set their own cookies or identifiers.

Common examples across our stack include:

* **Identity providers** used for social login via Authentik.
* **DNS / TLS / edge security providers** where used (for example, Cloudflare).
* **Documentation hosting** providers (for example, GitBook) and embedded media providers (where used).
* **Analytics providers** (for example, Google) where enabled.
* **Payment processors** (PayPal and Stripe) when you donate or pay.

When a third party sets cookies, their policies apply.

We do not control third‑party cookie lifetimes or behaviors.

#### Cloudflare

Where used, Cloudflare may set cookies or similar identifiers.

These are typically used for security and fraud prevention.

Examples include bot detection and rate limiting support.

#### PayPal and Stripe

If you use PayPal or Stripe checkout flows, they may set cookies or identifiers.

These are typically used to process payments and prevent fraud.

They may also be used for compliance and risk scoring.

### Cookies in support and store experiences

If you use Lazy Media’s support portal (Odoo) or store site (WordPress):

* Expect login and session cookies.
* Expect CSRF and anti-abuse tokens.
* Expect preference cookies (language, theme).

On store flows, cookies may also support:

* Cart state and checkout continuity.
* Fraud prevention and payment handoff to PayPal or Stripe.

### Cookies in authentication and SSO

If you log in via Lazy Media SSO, Authentik typically sets cookies to:

* Maintain your authenticated session.
* Enforce security controls such as CSRF protections.
* Track login state across apps that rely on SSO.

Apps integrated with Authentik can also set their own app-specific cookies.

Integration examples are documented here:

* [Basic Applications & Providers Setup](../../authentik/applications-and-providers.md)
* [Basic HTTP Authentication Passthrough](../../authentik/basic-http-authentication.md)
* [Federation & Social Logins](../../authentik/federation-and-social-login/)

### Cookies and the homelab network (UniFi)

Lazy Media’s homelab network infrastructure is based on UniFi / Ubiquiti.

If you access network-related portals or admin UIs, they can set cookies for:

* Administrator session management.
* Device identification within the portal.
* UI preferences.

Network telemetry and logs are typically server-side.

They may still correlate to sessions initiated from your browser.

### How you can control cookies

You can control cookies in several ways.

#### Browser settings

Most browsers let you:

* Delete cookies and site data.
* Block third‑party cookies.
* Block all cookies (may break login).
* Set per-site exceptions.

#### App‑level settings

Some apps let you disable specific features that rely on cookies.

Settings differ by application.

#### Consent controls (where required)

In some regions, we may request consent for non-essential cookies.

You can withdraw consent at any time by changing your browser settings.

Where available, you can also use any on-site consent controls.

{% hint style="warning" %}
Disabling cookies may break login flows, including SSO. It may also prevent CSRF protections from working.
{% endhint %}

### Retention

Cookie lifetimes vary by app and purpose.

Some cookies expire when you close your browser.

Others persist for a longer period to remember settings.

We aim to keep cookie lifetimes no longer than reasonably necessary.

### Do Not Track

Some browsers offer “Do Not Track” (DNT) signals.

There is no universal standard for responding to DNT.

We currently treat DNT as a preference signal, not a binding instruction.

### Changes to this Policy

We may update this Policy as services change.

We will update the “Last updated” date.

You can also track documentation changes in:

* [Changelog](../changelog.md)

### Contact

Use one of these channels:

* GitHub repo: [Lazy Media public repository](https://github.com/lazy-media/public)
* Community links: [Donations & Sponsors](../donations-and-sponsors.md)
* Access-related requests: [Joining Lazy Media's Server](./)

{% hint style="warning" %}
This document is provided for transparency. It is not legal advice.
{% endhint %}

<details>

<summary>Scope reference: documentation pages covered by this Cookie Policy</summary>

This Policy is written to be generic enough to cover all services and pages documented here.

If you use any Lazy Media hosted version of these, this Policy applies.

#### Core access and docs

* [Lazy Media's Docs](../../)
* [Joining Lazy Media's Server](./)
* [Cookie Policy](cookie-policy.md)
* [Privacy Policy](privacy-policy.md)
* [Terms of Service](terms-of-service.md)
* [Donations & Sponsors](../donations-and-sponsors.md)
* [Changelog](../changelog.md)

#### Auth and identity (Authentik)

* [Authentik](../../authentik/)
* [Authentik Installation](../../authentik/authentik-installation.md)
* [Basic Applications & Providers Setup](../../authentik/applications-and-providers.md)
* [Basic HTTP Authentication Passthrough](../../authentik/basic-http-authentication.md)
* [Federation & Social Logins](../../authentik/federation-and-social-login/)
  * [Plex & Twitch - OAuth Authentication, Enrollment, & User Group Assignment Setup](../../authentik/federation-and-social-login/plex-and-twitch-social-login-setup.md)
  * [Discord - OAuth Authentication, Enrollment, & User Group Assignment Setup](../../authentik/federation-and-social-login/discord.md)
* [Cloudflare Zero Trust](../../authentik/cloudflare-zero-trust.md)
* [Custom CSS Examples](../../authentik/custom-css-examples.md)
* [Default Authentik Flows](../../authentik/default-authentik-flows.md)
* [Prometheus Metrics for Authentik](../../authentik/prometheus.md)

**Authentik app integrations**

* [Dockhand](../../authentik/dockhand.md)
* [Gitlab (Authentik)](../../authentik/gitlab.md)
* [Grafana](../../authentik/grafana.md)
* [Immich (Authentik)](../../authentik/immich.md)
* [Jellyfin (Authentik)](../../authentik/jellyfin.md)
* [Jitsi Meet Test Files](../../authentik/jitsi-meet.md)
* [Kasm (Authentik)](../../authentik/kasm.md)
* [Mastodon (Authentik)](../../authentik/mastodon.md)
* [Nextcloud (Authentik)](../../authentik/nextcloud.md)
* [Paperless-NGX (Authentik)](../../authentik/paperless-ngx.md)
* [Portainer](../../authentik/portainer.md)
* [RocketChat Server](../../authentik/rocketchat.md)
* [Uptime Kuma](../../authentik/uptime-kuma.md)
* [Vaultwarden](../../authentik/vaultwarden.md)
* [Vikunja](../../authentik/vikunja.md)
* [Wiki-JS](../../authentik/wiki.js.md)

#### AI services (if hosted by Lazy Media)

* [Artificial Intelligence](../../artificial-intelligence/)
  * [Faster Whisper Wyoming Installation](../../artificial-intelligence/faster-whisper.md)
  * [Ollama Installation](../../artificial-intelligence/ollama.md)
  * [Open-WebUI](../../artificial-intelligence/open-webui.md)
  * [Piper Installation](../../artificial-intelligence/piper.md)
  * [Stable-Diffusion](../../artificial-intelligence/stable-diffusion.md)

#### Apps and platforms

* [Cal.com Appointment & Scheduling](../../cal.com-appointment-and-scheduling.md)
* [FiveM Server Setup with TX Admin](../../fivem.md)
* [Gitlab](../../gitlab.md)
* [Immich](../../immich.md)
* [Jellyfin](../../jellyfin.md)
* [Kasm Workspaces](../../kasm.md)
* [Mailcow](../../mailcow-installation-instructions.md)
* [Mastodon](../../mastodon.md)
* [Nextcloud](../../nextcloud.md)
* [Paperless-NGX](../../paperless-ngx.md)
* [Pterodactyl](../../pterodactyl-gaming-server.md)
* [Reactive Resume](../../reactive-resume.md)
* [Rocket-Chat Server](../../rocketchat-server.md)
* [Vaultwarden](../../vaultwarden.md)
* [Vikunja](../../vikunja.md)
* [Webmin](../../webmin.md)

#### Docker / self-hosting tooling (admin-facing)

* [Docker](../../docker/)
  * [Docker Engine Installation](../../docker/installation.md)
  * [Docker Management Tools](../../docker/docker-management-tools/)
    * [Dockhand Docker Management](../../docker/docker-management-tools/dockhand-docker-management.md)
    * [Dozzle Docker Logs](../../docker/docker-management-tools/dozzle-docker-logs.md)
    * [Portainer Docker Management](../../docker/docker-management-tools/portainer.md)
    * [WatchTower](../../docker/docker-management-tools/watchtower.md)
  * [Dockerfiles](../../docker/dockerfiles/)
    * [N8N](../../docker/dockerfiles/n8n.md)
    * [ReType](../../docker/dockerfiles/retype.md)

#### Data import helpers

* [Google Photos Takeout](../../google-photos-takeout/)
  * [Google Photo Takeout Helper](../../google-photos-takeout/google-photo-takeout-helper.md)
  * [Immich-Go](../../google-photos-takeout/immich-go.md)

#### Infrastructure and platform notes

* [Dell Poweredge R710 Drivers and Bootable ISO](../../dell-poweredge-r710.md)
* [iVentoy](../../iventoy.md)
* [My Home Lab](../../my-homelab/)
  * [AI-Server](../../my-homelab/ai-server.md)
  * [Personal PC](../../my-homelab/personal-pc.md)
  * [Proxmox Server 1](../../my-homelab/proxmox-server-1.md)
  * [Proxmox Server 2](../../my-homelab/proxmox-server-2.md)
  * [Proxmox Server 3](../../my-homelab/proxmox-server-3.md)
  * [Proxmox Server 4](../../my-homelab/proxmox-server-4.md)
  * [Proxmox Backup Server](../../my-homelab/proxmox-backup-server.md)
  * [TrueNas Scale Server](../../my-homelab/truenas-scale-server.md)
  * [Unifi / Ubiquiti Equipment](../../my-homelab/unifi-ubiquiti-equipment.md)
* [Proxmox](../../proxmox.md)
* [TrueNas Scale](../../truenas-scale/)
  * [Bridged Networking (VM LAN Access)](../../truenas-scale/bridged-networking-vm-lan-access.md)
  * [LSI 9300 16i HBA](../../truenas-scale/lsi-9300-16i-hba.md)
  * [UPS Monitor Setup](../../truenas-scale/ups-monitor-setup.md)
* [Windows 11](../../windows-11.md)
* [WordPress](../../wordpress.md)

</details>
