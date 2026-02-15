---
description: >-
  Some useful information that has to do with Proxmox. More for personal
  reference.
---

# Proxmox

### Quick links

Common references I use for Proxmox setups and troubleshooting.

{% hint style="info" %}
**PCI/GPU passthrough guide (PVE 8)**\
Forum thread covering setup and gotchas.\
[Open guide](https://forum.proxmox.com/threads/pci-gpu-passthrough-on-proxmox-ve-8-installation-and-configuration.130218/)
{% endhint %}

{% hint style="info" %}
**YouTube: Proxmox 8 GPU passthrough**\
Quick walkthroughs and different hardware approaches.\
[Open search](https://www.youtube.com/results?search_query=proxmox+8+gpu+passthrough)
{% endhint %}

{% hint style="info" %}
**Proxmox Helper Scripts**\
Community-maintained scripts for common tasks.\
[Open scripts](https://community-scripts.github.io/ProxmoxVE/scripts)
{% endhint %}

#### Unlock a locked VM or LXC container

A VM or container can remain **locked** after an interrupted task (backup, snapshot, migration, etc.).

Run the appropriate command on the **Proxmox node shell** (not inside the guest). Replace `100` with the correct ID.

{% tabs %}
{% tab title="Unlock VM" %}
On the Proxmox host, run this command. Replace `100` with the VMID:

```
qm unlock 100
```
{% endtab %}

{% tab title="Unlock LXC" %}
On the Proxmox host, run this command. Replace `100` with the container ID (CTID):

```
pct unlock 100
```
{% endtab %}
{% endtabs %}
