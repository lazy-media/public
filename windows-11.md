---
description: >-
  This will have any Windows 11 Pro related stuff I have found annoying and
  fixed about Windows 11 Pro. I am not sure if this is still applicable for
  Windows 11 Home.
---

# Windows 11

### Windows 11 Daily Automatic Restart

* Search for `Edit Group Policy`
* Once `Local Group Policy Editor` opens, Navigate to `Computer Configuration > Administrative Templates > Windows Components > Windows Update > Legacy Policies`
* Find `No auto-restart with logged on users for scheduled automatic updates installations`
* Double click to `Edit`.
* Enable this policy to prevent Windows from Auto Restarting while a user is at least logged into the machine.
