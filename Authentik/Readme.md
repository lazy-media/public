## NOTICE

To be clear, I have Authentik Setup in Docker with the Authentik Docker Compose File that is listed. I made a few modifications to my docker file, but this is just to persist data on all volumes listed.

### Authentik Setup

- I currently have Authentik installed alone on a Proxmox LXC container using Ubuntu 22.04, and separate from any other services.
- My Authentik Ports get set to 443 and 80 within the Docker Environment Variables File, but set to the standard ports in the Docker Compose File as 9443:9443 and 9000:9000.
- I currently ONLY run Authentik as my Reverse Proxy, no middle man like NPM, Traefik, Caddy, etc.
- I use Cloudflare Certificates installed into Authentik, not provided by any other reverse proxy or created by Let's Encrypt.
- I do not use Cloudflare Tunnels, I use other security measures provided by Cloudflare to protect my domain.
- For Installation Instructions on how I setup my Authentik, visit [Authentik Installation](Installation-Instructions/Authentik/Readme.md)

### Support

For further support, please visit the [Authentik Discord Server](https://goauthentik.io/discord). Please do a thorough search of the Discord Server before posting an issue, as I am sure the issue has been asked and solved. If not, feel free to post. Everyone is there to help each other. I am also pretty active on this Discord Server if you are looking for personal help.
