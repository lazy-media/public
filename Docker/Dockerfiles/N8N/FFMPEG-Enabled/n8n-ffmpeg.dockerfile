# Use the official n8n image as the base
FROM n8nio/n8n:latest

# Temporarily Switch to Root User
USER root

# Install FFmpeg
RUN apk add --no-cache ffmpeg

# Switch back to node user
USER node