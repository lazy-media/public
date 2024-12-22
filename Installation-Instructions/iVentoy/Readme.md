# iVentoy Installation Instructions

## Resources

[iVentoy Website](https://www.iventoy.com/en/index.html)

### Note
I installed this in a Proxmox Virtual Machine Running Ubuntu 22.04

## Download iVentoy
Best to pull the url from the latest version from the website

```
wget https://github.com/ventoy/PXE/releases/download/v1.0.20/iventoy-1.0.20-linux-free.tar.gz
```

### Extract iVentoy

```
tar -xzf iventoy-1.0.20-linux-free.tar.gz
```

### Change into new iVentoy Directory

```
cd iventoy-1.0.20/
```

### Start iVentoy for the First Time

```
sudo bash iventoy.sh start
```

### Navigate to iVentoy in browser

Open a browser and navigate to iVentoy WebUI

Navigate to `Configuration > Boot Configuration`

Change `DHCP Server Mode` to External so it uses your modem, router or gateway to route traffic instead of using iVentoy as a DHCP Server.

# BONUS

## Network Share

## Install Prerequisites
This is only if you plan to use ISO's stored on a NAS.

```
sudo apt-get -y install cifs-utils
```

### Create SMB Credentials

Make sure you are in your home Directory

```
nano .smbcredentials
```

Enter the following:

```
username=YOUR-SHARE-USERNAME
password=YOUR-SHARE-PASSWORD
```

### Change Permissions

```
sudo chmod 600 .smbcredentials
```

