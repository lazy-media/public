######################################################
# STEP 1: Start with the official n8n image as our base
######################################################
FROM n8nio/n8n:latest

######################################################
# STEP 2: Become root to install system packages
# (We need admin privileges to install software)
######################################################
USER root

######################################################
# STEP 3: Install ALL required system packages
# (These are like "apps" the system needs to run Python tools)
######################################################
RUN apk add --no-cache \
    # Basic Python setup
    python3 py3-pip \
    # Video/Audio tools
    ffmpeg \
    # Compilers and build tools (temporary - we'll remove these later)
    build-base python3-dev libffi-dev openssl-dev cargo \
    g++ pkgconfig llvm-dev llvm15 clang musl-dev \
    # Image processing libraries
    libjpeg-turbo-dev zlib-dev libpng-dev tiff-dev libwebp-dev \
    openblas-dev freetype-dev harfbuzz-dev lcms2-dev jpeg-dev openjpeg-dev \
    # Audio processing libraries
    portaudio-dev alsa-lib-dev libsndfile-dev \
    # Security certificates and compression
    ca-certificates xz

######################################################
# STEP 4: Create a safe space for Python packages
# (This keeps our Python tools separate from system tools)
######################################################
RUN python3 -m venv /home/node/.n8nvenv && \
    # Fix permissions so the 'node' user can access it
    chown -R node:node /home/node/.n8nvenv

######################################################
# STEP 5: Install Python packages
# (These are the actual tools your workflows will use)
######################################################
RUN python3 -m ensurepip && \
    # Upgrade the package installer first
    pip3 install --upgrade pip setuptools wheel && \
    # Main tools for automation
    pip install --no-cache-dir \
        requests beautifulsoup4 pandas numpy \
        # Video tools
        yt-dlp pytube \
        # Image processing
        opencv-python pillow \
        # Huggingface.co AI tools
        huggingface_hub gradio_client \
        # Audio processing
        soundfile audioread

######################################################
# STEP 6: Clean up our mess
# (Remove temporary tools to make the image smaller)
######################################################
RUN apk del --purge \
    build-base python3-dev libffi-dev openssl-dev cargo \
    g++ pkgconfig llvm-dev clang && \
    # Clear package cache
    rm -rf /var/cache/apk/* /tmp/*

######################################################
# STEP 7: Switch back to the safe 'node' user
# (n8n expects to run as this user for security)
######################################################
USER node

######################################################
# STEP 8: Make sure Python tools are in our PATH
# (So n8n can find all the commands we installed)
######################################################
ENV PATH="/home/node/.n8nvenv/bin:$PATH"

######################################################
# STEP 9: Set default working directory
# (This is where n8n will look for your workflows)
######################################################
WORKDIR /home/node/app