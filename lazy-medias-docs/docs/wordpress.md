---
description: >-
  Common self-hosted WordPress fixes (FTP credential prompt, upload size
  limits).
---

# WordPress

### Overview

This page covers two common WordPress issues in self-hosted installs.

1. WordPress prompts for FTP credentials during plugin/theme updates.
2. The WordPress media uploader has a low max upload size.

### References

* [Upload max file size limit (Docker forum thread)](https://forums.docker.com/t/issues-increasing-docker-wordpress-container-filesize-limit/119936) (uses the `.htaccess` approach)
* [Fixing FTP access authorization issue (YouTube)](https://www.youtube.com/watch?v=rjTJexgjVdE)

### Fix: WordPress asks for FTP credentials

This prompt is usually a permissions/ownership problem. WordPress must be able to write to its install directory.

#### 1) Validate ownership and permissions

Verify WordPress can write to the directories it updates, especially:

* `wp-content/`
* `wp-content/plugins/`
* `wp-content/themes/`
* `wp-content/uploads/`

Also verify `wp-config.php` and `.htaccess` are owned by the same user that runs PHP.

#### 2) Set the filesystem method (only if permissions are correct)

If permissions are correct and the prompt still appears, add this near the end of `wp-config.php`. Place it just above `/* That's all, stop editing! Happy publishing. */`.

```php
define('FS_METHOD', 'direct');
```

### Increase the max upload size

This method updates WordPress’ limits via `.htaccess`. It typically applies to Apache-based installs.

Before you start, ensure WordPress can write to `.htaccess`. Keep a backup so you can revert quickly.

If you use the **Really Simple SSL** plugin, it can prevent changes to `.htaccess`. Disable that protection before editing the file:

* In the WordPress admin console, open the **Really Simple SSL** dashboard.
* Go to **Really Simple SSL settings**.
* Ensure `Stop Editing the .htaccess file` is **unchecked**.

{% hint style="warning" %}
Use this at your own risk. This is what worked for Lazy Media. If you break your site, revert the `.htaccess` change.
{% endhint %}

#### 1) Edit `.htaccess`

Edit the `.htaccess` file in the root of your WordPress install.

* If this is Docker on Linux, it’s often in a Docker volume under:
  * `/var/lib/docker/volumes/YOUR-WORDPRESS-CONFIG-STORAGE`
* If your setup differs, locate the volume or bind-mount used by WordPress.

#### 2) Add the directives

Add the following to the bottom of `.htaccess`.

```php
# Increase Max Upload File Size
php_value upload_max_filesize 50M
php_value post_max_size 50M
```

#### 3) Tune the limit

To change the limit, edit the `50M` values. Only change the number. Keep the trailing `M`.
