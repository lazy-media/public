## NOTICE

To be clear, I have Authentik Setup in Docker with the Original Authentik Docker Compose File that is listed in their documentation. I made a few modifications to my docker file, but this is just to persist data on all volumes listed, and expose other ports that may be needed for other services.

Please do not ask for support on a product or service that you are trying to use if it is not listed in this repository. It probably means, that I don't use it or don't have it set up with Authentik and will not be able to provide support for it.

### Authentik Prerequisite Setup

- I currently have Authentik installed alone on a Proxmox LXC container using Ubuntu 22.04, and separate from any other services.
- My Authentik Ports get set to 443 and 80 within the Docker Environment Variables File, but set to the standard ports in the Docker Compose File as 9443:9443 and 9000:9000.
- I currently ONLY run Authentik as my Reverse Proxy, no middle man like NPM, Traefik, Caddy, etc.
- I use Cloudflare Certificates installed into Authentik, not provided by any other reverse proxy or created by Let's Encrypt.
- I do not use Cloudflare Tunnels, I use other security measures provided by Cloudflare to protect my domain.
- I have my ISP Modem in bridge mode and have a Unifi Security Gateway handling all internet traffic.
    - I have port 443 forwarded to Authentik
- For Installation Instructions on how I setup my Authentik, visit [Authentik Installation](Installation-Instructions/Authentik/Readme.md)

### Support

For further support, please visit the [Authentik Documentation](https://docs.goauthentik.io/docs), [Authentik Github Issues](https://github.com/goauthentik/authentik/issues), or the [Authentik Discord Server](https://goauthentik.io/discord).

### Best Videos to watch to get started

[Cooptonian - Authentik Setup Playlist](https://youtube.com/playlist?list=PLH73rprBo7vSkDq-hAuXOoXx2es-1ExOP&si=Y0byly0a4PmfdxkR)
