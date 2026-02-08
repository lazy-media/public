# ReType

### Official Documentation

[ReType Documentation - Docker](https://retype.com/hosting/docker/)

Create a custom docker image for ReType

### Dockerfile

```docker
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS builder
WORKDIR /build
COPY . /build
RUN dotnet tool install retypeapp --tool-path /bin
RUN retype build --output .docker-build/

FROM httpd:latest
COPY --from=builder /build/.docker-build/ /usr/local/apache2/htdocs/
```

### Build the Image

```bash
docker build -t myorg/myapplication:latest .
```

### Start the Container

```bash
docker run --rm -p 8080:80 myorg/myapplication:latest
```
