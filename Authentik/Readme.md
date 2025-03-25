## System Configuration Notice

### Authentik Deployment Overview

My Authentik implementation uses the official Docker Compose file from Authentik's documentation with the following customizations:
- Volume persistence modifications for all data stores
- Additional port exposures for service integration

**Support Scope:**  
Please note that I can only provide support for products and services documented in this repository. Undocumented items indicate either:
- The service is not in use
- Not configured with Authentik integration
- Outside my support capabilities

---

## Authentik Prerequisites & Environment

### Infrastructure Details
- **Host Environment:** Proxmox LXC container (Ubuntu 22.04)
- **Deployment Model:** Isolated standalone installation
- **Reverse Proxy:** Authentik-only solution (no NPM/Traefik/Caddy)

### Network Configuration
- **Port Mapping:**
  - Internal: 443/80 (Docker environment variables)
  - External: 9443:9443, 9000:9000 (Docker Compose)
- **Security Infrastructure:**
  - Cloudflare certificates (directly installed in Authentik)
  - No Cloudflare Tunnels (alternative Cloudflare security measures)
  - ISP modem in bridge mode
  - UniFi Security Gateway handling all traffic
    - Port 443 forwarded to Authentik

For complete setup instructions:  
[Authentik Installation Guide](Installation-Instructions/Authentik/Readme.md)

---

## Support Resources

### Official Documentation
- [Authentik Product Documentation](https://docs.goauthentik.io/docs)
- [GitHub Issue Tracker](https://github.com/goauthentik/authentik/issues)
- [Official Discord Server](https://goauthentik.io/discord)

### Recommended Learning Resources
[Cooptonian - Authentik Setup Video Series](https://youtube.com/playlist?list=PLH73rprBo7vSkDq-hAuXOoXx2es-1ExOP&si=Y0byly0a4PmfdxkR)

## 💖 Support My Work

Enjoying this project? Help me keep it alive and evolving:

### 🌟 One-Time Donations
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/lazymediawa)

### 🔄 Recurring Support
[![GitHub Sponsors](https://img.shields.io/badge/GitHub_Sponsors-30363D?style=for-the-badge&logo=github-sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/lazy-media)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://link.lazymedia.media/patreon)

### ₿ Crypto Donations
**Bitcoin:**  
`13GdxyJ85Y78oq97Ktnr6fqdCUsa4vcMgp`

---

## 🌐 Follow Me

Stay updated with my latest projects and tutorials:

### 📱 Social Media

[![Mastodon](https://img.shields.io/badge/Mastodon-6364FF?style=for-the-badge&logo=mastodon&logoColor=white)](https://link.lazymedia.media/mastodon)
[![Discord](https://img.shields.io/badge/Main_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://link.lazymedia.media/lazymedia-discord-promo-page)
[![Discord](https://img.shields.io/badge/Gaming_Community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://link.lazymedia.media/lazymedia-gaming-discord-promo-page)

### 💻 Dev Platforms
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lazy-media)
[![GitLab](https://img.shields.io/badge/GitLab-FCA121?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.lazymedia.media/root)

### 🎥 Video & Live Coding
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@LazyMediaWA)
[![Twitch](https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white)](https://twitch.tv/LazyMediaWA)
[![Kick](https://img.shields.io/badge/Kick-53FC18?style=for-the-badge&logo=kick&logoColor=black)](https://kick.com/LazyMedia)