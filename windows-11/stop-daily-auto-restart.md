---
description: Instructions on how to stop daily auto restart with Windows 11
---

# stop-daily-auto-restart

* Search for `Edit Group Policy`
* Once `Local Group Policy Editor` opens, Navigate to `Computer Configuration > Administrative Templates > Windows Components > Windows Update > Legacy Policies`
* Find `No auto-restart with logged on users for scheduled automatic updates installations`
* Double click to `Edit`.
* Enable this policy to prevent Windows from Auto Restarting while a user is at least logged into the machine.
