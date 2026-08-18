---
description: >-
  Configure Jellyfin access, XMLTV guide data, Live TV, and interface
  customization.
---

# Jellyfin

## Jellyfin setup guide

Configure Jellyfin access, XMLTV guide data, Live TV, and login-page customization.

### Jellyfin setup

Complete these prerequisites before configuring Jellyfin:

* A working Jellyfin server with administrator access.
* A PHP-enabled web server that Jellyfin can reach.
* A TVTV lineup ID for your location.

### Jellyfin configuration

#### Configure Quick Connect

Quick Connect lets compatible devices sign in without a browser-based login flow.

1. Open **Administration → Dashboard → General**.
2. Find **Quick Connect**.
3. Enable the setting and save your changes.

#### Configure single sign-on

Configure an external identity provider when you want centralized user access. Follow the [Authentik Jellyfin OpenID setup](authentik/jellyfin.md) for an Authentik-based configuration.

### Guide source configuration

Create an XMLTV endpoint before adding guide data to Jellyfin. This configuration uses the following sources:

* [Jellyfin TV guide script](https://gist.github.com/idolpx/c82747bb740c303f56ad8a1e8f17d575)
* [TVTV](https://tvtv.us) for listing data.

{% stepper %}
{% step %}
#### Create the guide file

Sign in to your PHP web server. Open a public directory, such as `/var/www/YOURWEBSITE/`.

Create a file named `tvxml.php`.
{% endstep %}

{% step %}
#### Configure XMLTV

Copy the script below into `tvxml.php`. Set `$timezone` and `$lineUpID` for your location.

Set `$days` to the required guide duration. TVTV supports up to eight days.

{% hint style="warning" %}
This script may no longer work. TVTV has restricted access to its API and XMLTV files. You may need an alternative guide-data source.
{% endhint %}

{% code title="tvxml.php" expandable="true" collapsedlinecount="20" %}
```php
<?php
//
// tvtv2xmltv Guide Data
// https://gist.github.com/idolpx/c82747bb740c303f56ad8a1e8f17d575
// Author: Jaime Idolpx (jaime@idolpx.com)
//
// - This script will extract guide data from "tvtv.us" and produce an "XmlTV" data file
// - Set the options for the guide data you want to extract below
// - Host this on a php enabled web server
// - Configure your TV Guide software to use it as a data source (Jellyfin in my case)
//
// https://www.tvtv.us/
// http://wiki.xmltv.org/index.php/XMLTVFormat
// https://www.xmltvlistings.com/help/api/xmltv
//


$timezone = "America/New_York";  // Set to your local timezone
$lineUpID = "USA-OTA30236";      // Set this to ID of the Line Up data you want to extract
$days     = 8;                   // Number of days worth of guide data to collect (8 days max)

//////////////////////////////////////////////////////////////////////////////////////////////////

// Setup filename for download
$fileDate = date ( "Ymd" );
header("Content-disposition: attachment; filename=xmltv.".$fileDate.".xml");
header("Content-type: text/xml");

// Build XMLTV data
$url = "http". ( !empty ( $_SERVER['HTTPS'] ) ? "s" : "" )."://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
$now = strtotime ( "now" );
$startTime = date ( 'Y-m-d\T00:00:00.000\Z', $now );

echo("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\r\n");
echo("<!DOCTYPE tv SYSTEM \"xmltv.dtd\">\r\n");
echo("<tv date=\"".$startTime."\" source-info-url=\"".$url."\" source-info-name=\"tvtv2xmltv\">\r\n");

// GET lineup data
$lineup_url = "https://www.tvtv.us/api/v1/lineup/".$lineUpID."/channels";
$json = file_get_contents( $lineup_url );
$lineup_data = json_decode( $json, true );

$channels = "";
foreach ( $lineup_data as &$channel )
{
    // Build channel query string
    $channels .= $channel["stationId"].",";

    // Channel data
    echo("<channel id=\"".$channel["channelNumber"]."\">");
    echo("<display-name>".$channel["channelNumber"]."</display-name>");
    echo("<display-name>".$channel["stationCallSign"]."</display-name>");
    echo("<icon src=\"https://www.tvtv.us".$channel["logo"]."\" />");
    echo("</channel>\r\n");
    @ob_flush(); flush();
}

// Get max 8 days of guide data starting today
if ( $days > 8 ) $days = 8;
for ( $day = 0; $day < $days; $day++)
{
    // GET guide data
    $now = strtotime ( "now + ".$day." day" );
    $end = strtotime ("now + ".($day + 1)." day" );
    $startTime = date ( 'Y-m-d\T04:00:00.000\Z', $now ); //"2023-05-23T04:00:00.000Z";
    $endTime = date ( 'Y-m-d\T03:59:00.000\Z', $end ); //"2023-05-24T03:59:00.000Z";
    $listing_url = "https://www.tvtv.us/api/v1/lineup/".$lineUpID."/grid/".$startTime."/".$endTime."/".$channels;
    $json = file_get_contents( $listing_url );
    $listing_data = json_decode( $json, true );

    $index = 0;
    foreach ( $lineup_data as &$channel )
    {
        // Program Data
        foreach ( $listing_data[$index] as &$program )
        {
            $programId = htmlspecialchars ( $program['programId'], ENT_XML1, 'UTF-8' );
            $title = htmlspecialchars ( $program['title'], ENT_XML1, 'UTF-8' );
            $subtitle = @htmlspecialchars ( $program['subtitle'], ENT_XML1, 'UTF-8' );
            $flags = implode ( ", ", $program['flags'] );
            $type = htmlspecialchars ( $program['type'], ENT_XML1, 'UTF-8' );
            $startTime = htmlspecialchars ( $program['startTime'], ENT_XML1, 'UTF-8' );
            $start = htmlspecialchars ( $program['start'], ENT_XML1, 'UTF-8' );
            $duration = htmlspecialchars ( $program['duration'], ENT_XML1, 'UTF-8' );
            $runTime = htmlspecialchars ( $program['runTime'], ENT_XML1, 'UTF-8' );

            $tStart = new DateTime($startTime);
            $tStart->setTimeZone(new DateTimeZone($timezone));
            $startTime = $tStart->format("YmdHis O");
            $tStart->add(new DateInterval('PT'.$program['runTime'].'M'));
            $endTime = $tStart->format("YmdHis O");

            echo("<programme start=\"".$startTime."\" stop=\"".$endTime."\" duration=\"".$duration."\" channel=\"".$channel["channelNumber"]."\">");
            echo("<title lang=\"en\">".$title."</title>");
            echo("<sub-title lang=\"en\">".$subtitle."</sub-title>");

            if ( $type == "M" )
                echo("<category lang=\"en\">movie</category>");

            if ( $type == "N" )
                echo("<category lang=\"en\">news</category>");

            if ( $type == "S" )
                echo("<category lang=\"en\">sports</category>");

            if ( strstr($flags, "EI") )
                echo("<category lang=\"en\">kids</category>");

            if ( strstr($flags, "HD") )
            {
                echo("<video>");
                echo("<quality>HDTV</quality>");
                echo("</video>");
            }

            if ( strstr($flags, "Stereo") )
            {
                echo("<audio>");
                echo("<stereo>stereo</stereo>");
                echo("</audio>");
            }

            if ( strstr($flags, "New") )
            {
                echo("<new />");
            }

            echo("</programme>\r\n");
            @ob_flush(); flush();
        }

        $index++;
    }
}

echo("</tv>");

```
{% endcode %}
{% endstep %}

{% step %}
#### Validate the guide endpoint

Open `http://YOUR-SERVER/tvxml.php` in a browser. The server should download an XMLTV file.
{% endstep %}
{% endstepper %}

### Jellyfin Live TV setup

1. Open **Administration → Dashboard → Live TV**.
2. Select **Add TV Guide Data Source**.
3. Choose **Custom XMLTV**.
4. Enter the XMLTV URL from your PHP web server, such as `http://192.168.1.10/tvxml.php`.
5. Save the provider, then refresh the guide.
6. Select the **three vertical dots** beside the provider.
7. Select **Map Channels** and map each guide channel to its Jellyfin channel.

{% hint style="info" %}
Jellyfin must reach the guide URL. Use an address accessible from the Jellyfin server, not only from your browser.
{% endhint %}

{% hint style="warning" %}
Channel mapping is required for guide data to appear against the correct channels. Complete **Map Channels** after adding or changing a guide provider.
{% endhint %}

### Jellyfin customization

#### Customize the login page

This optional CSS places **Quick Connect** beside the sign-in buttons. It hides the manual sign-in form and password controls.

In Jellyfin, open **Administration → Dashboard → General → Branding**. Paste the following into **Custom CSS code**, then save your changes.

{% hint style="warning" %}
Keep a tested SSO or Quick Connect path before applying this CSS. It removes Jellyfin’s local login form and password-reset controls.
{% endhint %}

```css
/* ==========================================================================
Removes Main Login Form and Forgot Password Button. Shows Quick Connect at the top
of the page with the other Login and SSO Buttons.
========================================================================== */

#loginPage .quickConnectContainer,
#loginPage .btnQuickConnect {
  order: 1; /* pin Quick Connect up with Sign In / other login buttons */
}

#loginPage .manualLoginForm {
  display: none !important;
}

#loginPage .btnForgotPassword {
  display: none !important;
}

#userProfilePage .updatePasswordForm {
  display: none !important;
}

.customMenuOptions a[href*="SSOViews"] {
  display: none !important;
}
```

### Verify and maintain the setup

Open **Live TV → Guide** to confirm that listings load correctly. Refresh guide data after changing the PHP script or its lineup configuration.

Review the login page after applying custom CSS. Confirm that each intended sign-in method remains available.
