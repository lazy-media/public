# iVentoy Installation Instructions

## Resources

[iVentoy Website](https://www.iventoy.com/en/index.html)

### Note
I installed this in a Proxmox Virtual Machine Running Ubuntu 24.04

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

### Edit FSTAB

```
sudo nano /etc/fstab
```

Add the following line, changing what is needed if directories are different

```
//YOUR-NAS-IP/ISOs/ /home/ubuntu/iventoy/iso/ cifs credentials=/home/ubuntu/.smbcredentials 0 0
```

### Reload Daemon

```
sudo systemctl daemon-reload
```

### Mount the Share

```
sudo mount -a
```

You should now be able to see your ISOs inside iVentoy ISO folder.

## Create a Service for iVentoy

This allows for iVentoy to start at system boot so you don't have to start it your self everytime

```
sudo nano /etc/systemd/system/iventoy.service
```

Paste the following into the file, changing what is needed if your directories are different

```
# /etc/systemd/system/iventoy.service
[Unit]
Description = iVentoy iPXE Server
Requires = network-online.target
After    = network-online.target
Wants    = network-online.target

[Service]
Type = forking
User = root
Group = root
WorkingDirectory = /home/ubuntu/iventoy
ExecStart = /home/ubuntu/iventoy/iventoy.sh -R start
ExecStop = /home/ubuntu/iventoy/iventoy.sh stop
Restart = on-failure

[Install]
WantedBy = multi-user.target
```

Save the file and exit

### Start and enable the iVentoy Service

```
sudo systemctl start iventoy.service && sudo systemctl enable iventoy.service
```
