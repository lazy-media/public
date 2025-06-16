# Reactive Resume

## Original Documentation

- [Reactive Resume Docs](https://docs.rxresu.me/)
- [Reactive Resume Github](https://docs.rxresu.me/product-guides/self-hosting-reactive-resume-using-docker)

## Docker Compose & .env Files

> This is a modified version of the original docker-compose file from Reactive Resume. It is modified to use a .env file with Variables. Please change .env variables to reflect the docker-compose file.

- [Docker Compose File with .env File](docker-compose.yaml)
- [.env file](.env)

## Adding Local AI / OpenWebUI to Reactive Resume

You can integrate with OpenWebUI to use with your local AI. This requires an HTTPS connection.

> 1. Get an API/Access Token from OpenWebUI
> 2. Input the token in the appropriate field
> 3. Set the OpenWebUI URL as either:
>     - https://openwebui.example.com/api
>     - https://localhost:11434/api
> 4. Select your preferred model (e.g., llama3.2:latest)
> 5. Configure max tokens and other parameters as needed