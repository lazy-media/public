# Stable Diffusion Installation

## References

- [Network Chuck YouTube Video](https://link.lazymedia.media/wHjOL)
- [Network Chuck Acadamy Documentation](https://link.lazymedia.media/wYZCQ)
- [Stable Diffusion Github](https://link.lazymedia.media/xNvqh)

# Installation Setup

Installed on Ubuntu Server 24.04
Dedicated Hardware, No VM
ASRock Motherboard
Intel Core i5-6600
NVIDIA GTX 1070

# Install Prerequisites

```
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
```

## Install Python Env

```
curl https://pyenv.run | bash
```

## Run the Commands the Script Gives at the End

```
export PYENV_ROOT="$HOME/.pyenv" 
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)" 
```

## Restart Shell

```
source .bashrc
```

## Make Sure Python is Running

```
pyenv -h
```

## Install Python 3.10

```
pyenv install 3.10
```

## Make Python 3.10 Global

```
pyenv global 3.10
```

# Create Directory for Stable Diffusion

If you are in your home directory, that is fine

```
mkdir stable-diffusion
```
### Change into that directory

```
cd stable-diffusion
```

# Install Stable Diffusion

```
wget -q https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh
```

## Make Sure Script is there

```
ls -a
```

## Make the Script Executable

```
chmod +x webui.sh
```

## Test the script and make sure it runs

```
./webui.sh --listen --api
```

# BONUS

## Make this a startup service for Ubuntu

Create a new Service File

```
nano /etc/systemd/system/stable-diffusion.service
```

Paste the following into the File (Make sure to change the directories of where you have Stable Diffusion Installed to)
```
# /etc/systemd/system/stable-diffusion.service

[Service]

ExecStart=/bin/bash /home/ubuntu/stable-diffusion/webui.sh --listen --api --api-auth stable-diffusion:2j3GQ5C3n361
Restart=always
WorkingDirectory=/home/ubuntu/stable-diffusion
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=Stable-Diffusion-Webui
User=ubuntu
Desc=Stable Diffusion Image Generation

[Install]
WantedBy=multi-user.target

# usage
#
# sudo mv stable-diffusion.service /etc/systemd/system/stable-diffusion.service
# sudo systemctl start stable-diffusion
```

## Start Stable Diffusion Service

```
sudo systemctl start stable-diffusion
```

### Make sure it works

Navigate to your machine IP Address and port number (Change IP Below to your machine, leave port number as is)

```
http://192.168.1.10:7860
```

## Enable the service to start at system startup

```
sudo systemctl enable stable-diffusion
```