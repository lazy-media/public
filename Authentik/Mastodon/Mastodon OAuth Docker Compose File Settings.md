## TO BE CLEAR, I AM RUNNING MASTODON IN A DOCKER COMPOSE FILE. I AM RUNNING SEPERATE DOCKER CONTAINERS FOR THE DATABASE AND REDIS. I AM ALSO USING PORTAINER TO MANAGE THIS STACK AND OTHER CONTAINERS.

### My Mastodon Docker Compose FILE

```

---
version: "2.1"
services:
  mastodon:
    image: lscr.io/linuxserver/mastodon:latest
    container_name: mastodon
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - LOCAL_DOMAIN=MASTODON-DOMAIN
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - DB_HOST=db
      - DB_USER=mastodon
      - DB_NAME=mastodon
      - DB_PASS=DB-PASSWORD
      - DB_PORT=5432
      - ES_ENABLED=false
      - SECRET_KEY_BASE=GENERATE-THIS-USING-PROPER-COMMAND
      - OTP_SECRET=GENERATE
      - VAPID_PRIVATE_KEY=GENERATE
      - VAPID_PUBLIC_KEY=GENERATE
      - SMTP_SERVER=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_LOGIN=YOUR-EMAIL
      - SMTP_PASSWORD=YOUR-EMAIL-PASSWORD
      - SMTP_FROM_ADDRESS=YOUR-EMAIL
      - S3_ENABLED=false
      - WEB_DOMAIN=DOMAIN-FOR-MASTODON #optional
      - SIDEKIQ_ONLY=false #optional
      - SIDEKIQ_QUEUE= #optional
      - SIDEKIQ_DEFAULT=false #optional
      - SIDEKIQ_THREADS=5 #optional
      - DB_POOL=5 #optional
      - OIDC_ENABLED=true
      - OIDC_DISPLAY_NAME=DISPLAY-NAME-FOR-OAUTH-ON-MASTODON-LOGIN-PAGE
      - OIDC_DISCOVERY=true
      - OIDC_ISSUER=https://YOUR-AUTHENTIK-DOMAIN/application/o/mastodon-oauth/
      - OIDC_AUTH_ENDPOINT=https://YOUR-AUTHENTIK-DOMAIN/application/o/authorize/
      - OIDC_SCOPE=openid,profile,email
      - OIDC_UID_FIELD=sub
      - OIDC_CLIENT_ID=AUTHENTIK-PROVIDER-CLIENT-ID
      - OIDC_CLIENT_SECRET=AUTHENTIK-PROVIDER-CLIENT-SECRET
      - OIDC_REDIRECT_URI=https://YOUR-MASTODON-DOMAIN/auth/auth/openid_connect/callback
      - OIDC_SECURITY_ASSUME_EMAIL_IS_VERIFIED=true

    volumes:
      - /var/lib/docker/volumes/mastodon/_data:/config
    ports:
      - 80:80
      - 443:443
    restart: unless-stopped
    
    ```

    
