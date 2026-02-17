---
description: Create a `br0` bridge, move the host IP to it, and attach VMs to the bridge.
---

# Bridged Networking (VM LAN Access)

### Overview

Use a bridge when you want VMs to sit directly on your LAN. This is the common `br0` setup.

This is especially useful when your VMs need to access **SMB shares hosted on the same server**.

The key idea is simple:

* Remove the IP config from the physical NIC.
* Create `br0` using that NIC as a member.
* Put the IP config on `br0`.

#### What this enables (VMs → SMB on the same host)

After this change:

* Your TrueNAS host keeps its normal LAN IP (now assigned to the bridge).
* Your VMs can use bridged networking and get normal LAN connectivity.
* From the VM, connect to SMB using the **TrueNAS host IP/hostname** (the address on the bridge).

{% hint style="info" %}
If you configured SMB to bind to specific IPs, make sure the IP you use (the bridge IP) is included.
{% endhint %}

{% hint style="warning" %}
Changing network interfaces can disconnect the web UI.

Do this during a maintenance window. Have console access ready (local keyboard/monitor, IPMI, etc.).
{% endhint %}

### Before you start

Collect the current network settings first:

* Host IP address and prefix (example: `192.168.1.10/24`)
* Default gateway
* DNS servers
* The active physical interface name (example: `enp3s0`)

{% hint style="info" %}
If you currently use DHCP, consider reserving the IP in your router first. It prevents surprise IP changes after the bridge cutover.
{% endhint %}

#### If this is an existing system (VMs / Apps already running)

Shut down anything using the physical NIC you plan to bridge.

At minimum:

* If the VM OS supports hot-swapping network devices, you can change the NIC without shutting down.
* If it does not, shut down the VM first.
* If your TrueNAS server has multiple physical NICs:
  * Move the VM's NIC off the NIC you’re about to bridge.
  * Attach it to a NIC that is not currently being used.
* If your TrueNAS server has only a single physical NIC:
  * Record the NIC **Device Order** value before removing it.
  * Remove the NIC device from the VM completely.

This avoids “interface in use” edge cases during the change.

### Step-by-step: create `br0`

{% stepper %}
{% step %}
### Open network interfaces

In the TrueNAS web UI:

1. Go to **Network**.
2. Open **Interfaces**.
{% endstep %}

{% step %}
### Remove the IP from the physical NIC

1. Find the physical interface that currently holds the host IP.
2. Click **Edit** (pencil icon).
3. Under **Aliases**, remove any existing entries.
4. If **DHCP** is enabled, disable it.
5. Click **Save**.

At this point, the host should have **no IP** on the physical NIC.
{% endstep %}

{% step %}
### Create the bridge interface

1. Click **Add**.
2. Set **Type** to **Bridge**.
3. Set **Name** to `br0`.
4. Under **Bridge members**, select the physical NIC from step 2.

{% hint style="warning" %}
Do not add multiple NICs as bridge members to “combine” them.

If you need multi-NIC throughput or redundancy, create a bond/LAGG first. Then bridge the bond.
{% endhint %}
{% endstep %}

{% step %}
### Assign the host IP to `br0`

1. Under **Aliases**, click **Add**.
2. Enter the same IP and prefix you noted earlier (example: `192.168.1.10/24`).
3. Click **Save**.

TrueNAS requires **Test Changes** before it finalizes network updates. If the change breaks connectivity, TrueNAS will automatically revert after **60 seconds** by default. Adjust the timer if your IP will change, then confirm only after you reconnect successfully.
{% endstep %}

{% step %}
### Reconnect and validate

1. Re-open the web UI at the host IP.
2. Verify `br0` shows the expected IP.
3. Verify the physical NIC has no alias IP.
{% endstep %}

{% step %}
### Attach VMs to `br0`

For each VM:

1. Edit the VM.
2. If you removed the NIC earlier, add a new NIC device now.
   * Set **Device Order** to the value you recorded.
3. Update the NIC device to use `br0`.
4. Start the VM.

Once the VM is online, it should be able to reach the TrueNAS host over the LAN and connect to SMB shares using the host IP/hostname.
{% endstep %}
{% endstepper %}

### Validate SMB access from a VM

Use the TrueNAS **host IP/hostname** (the address now on the bridge).

Before testing, confirm on TrueNAS:

* **Services → SMB** is running.
* Your SMB share exists and your user has permissions.

{% tabs %}
{% tab title="Windows" %}
1. Verify the port is reachable:

```powershell
Test-NetConnection -ComputerName <truenas-hostname-or-ip> -Port 445
```

2. Open the share in File Explorer:

```
\\<truenas-hostname-or-ip>\<share-name>
```

3. Optional: map a drive:

```powershell
net use Z: \\<truenas-hostname-or-ip>\<share-name> /persistent:yes
```
{% endtab %}

{% tab title="Linux" %}
1. Verify the port is reachable:

```bash
nc -vz <truenas-hostname-or-ip> 445
```

2. List shares (requires `smbclient`):

```bash
smbclient -L //<truenas-hostname-or-ip> -U <username>
```

3. Mount a share (requires `cifs-utils`):

```bash
sudo mount -t cifs //<truenas-hostname-or-ip>/<share-name> /mnt/truenas \
  -o username=<username>
```
{% endtab %}

{% tab title="FreeBSD" %}
1. Verify the port is reachable:

```sh
nc -vz <truenas-hostname-or-ip> 445
```

2. Mount a share:

```sh
sudo mkdir -p /mnt/truenas
sudo mount_smbfs -I <truenas-hostname-or-ip> //<username>@<truenas-hostname-or-ip>/<share-name> /mnt/truenas
```

{% hint style="info" %}
If you need `smbclient` on FreeBSD, install the Samba client tools (`pkg install samba-client`).
{% endhint %}
{% endtab %}
{% endtabs %}

### Troubleshooting

#### Web UI is unreachable after the change

* Wait for the revert timer.
* Use console access to roll back the interface changes.
* Confirm the IP, prefix, gateway, and DNS values are correct.

#### Bridge exists but there’s no network connectivity

* Ensure the physical NIC is selected as a **bridge member**.
* Ensure the IP alias is on `br0`, not the physical interface.
* Check for a duplicate IP on the LAN.

#### You want to use more than one NIC

A bridge is not a safe way to aggregate NICs. Use bonding/LACP, then bridge the bond if needed.
