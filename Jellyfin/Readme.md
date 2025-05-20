# Jellyfin Initial Setup and TV Guide Setup

## Original Creator / Content

- [Jellyfin TV Guide Script](https://gist.github.com/idolpx/c82747bb740c303f56ad8a1e8f17d575)
- [TV Guide Site Used](https://tvtv.us)

## Assumptions

- You already have Jellyfin Installed and Working
- You have a web server running PHP

## TV Guide Setup

- Login to your Web server running PHP
- Navigate to a folder that is publicly accessible.
    - Usually something like `/var/www/YOURWEBSITE/`
- Create a new file and name it something like `tvxml.php`
- Paste the contents of [TVXML.php](/Installation-Instructions/Jellyfin/tvxml.php) into this newly created file.
- Save the file and exit

### Jellyfin Setup

- Navigate to your `Jellyfin Admin Panel > Live TV > Live TV`
- Add a new TV Provider
- Use a custom or XMLTV file
- In the File or URL spot, insert the local address or public address of the file you created on your PHP enabled web server.
    - This should be something like `http://192.168.1.10/tvxml.php` or `https://web.domain.example/tvxml.php`

### Jellyfin Authentik OpenID Setup

> [Authentik Jellyfin OpenID Setup](/Authentik/Jellyfin/Readme.md)

### Conclusion
That's it, you should now be able to view a TV Guide in Jellyfin.