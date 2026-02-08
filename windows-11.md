---
description: >-
  This will have any Windows 11 Pro related stuff I have found annoying and
  fixed about Windows 11 Pro. I am not sure if this is still applicable for
  Windows 11 Home.
---

# Windows 11

### Overview

Quick fixes for common Windows 11 Pro annoyances. Some items may not apply to Windows 11 Home.

### Disable daily automatic restarts (while a user is logged in)

Configure the Windows Update policy that blocks auto-restarts during scheduled update installs.

{% stepper %}
{% step %}
### Open Local Group Policy Editor

Search for `Edit group policy`.

Open **Local Group Policy Editor**.
{% endstep %}

{% step %}
### Navigate to the Windows Update legacy policies

Go to:

`Computer Configuration > Administrative Templates > Windows Components > Windows Update > Legacy Policies`
{% endstep %}

{% step %}
### Enable the “No auto-restart” policy

Find:

`No auto-restart with logged on users for scheduled automatic updates installations`

Double-click it, then set it to **Enabled**.
{% endstep %}
{% endstepper %}

Once enabled, Windows should not auto-restart while a user is logged in.
