# Kasm Installation Instructions

## Update System and Reboot
```
apt update && apt dist-upgrade -y && reboot
```
## Install Dependencies
```
apt install -y curl
```

## Single Server Installation
### Change to Temp Directory
```
cd /tmp
```
### Download Kasm to Temp Directory
```
curl -O https://kasm-static-content.s3.amazonaws.com/kasm_release_1.14.0.3a7abb.tar.gz
```
### Extract Kasm from downloaded file
```
tar -xf kasm_release_1.14.0.3a7abb.tar.gz
```
### Run Install script
```
sudo bash kasm_release/install.sh
```

# Third Party Registries

Linux.io
```
https://kasmregistry.linuxserver.io
```

# Setting Up OAuth with Authentik

### Create Provider and Application in Authentik and make note of Client ID and Secret Key.

Visit [Kasm OAuth Instructions](/Authentik/Kasm/Readme.md)
