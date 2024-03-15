## NOTICE

To be clear, I have Authentik Setup in Docker with the Authentik Docker Compose File that is listed. I made a few modifications to my docker file, but this is just to persist data on all volumes listed. I will not and can not provide any type of support for this product unless it is setup like mine is.

### Authentik Setup

- I currently have Authentik installed alone on a Proxmox LXC container using Ubuntu 22.04, and separate from any other services.
- I currently ONLY run Authentik as my Reverse Proxy, no middle man like NPM, Traefik, Caddy, etc.
- I use Cloudflare Certificates installed into Authentik, not provided by any other reverse proxy or created by Let's Encrypt.
- I do not use Cloudflare Tunnels, I use other security measures provided by Cloudflare to protect my domain.

### Support

For further support, please visit the [Authentik Discord Server](https://goauthentik.io/discord). Please do a thorough search of the Discord Server before posting an issue, as I am sure the issue has been asked and solved. If not, feel free to post. Everyone is there to help each other. I am also pretty active on this Discord Server if you are looking for personal help.
