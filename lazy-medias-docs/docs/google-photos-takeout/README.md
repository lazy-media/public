---
description: >-
  Information on how to get a Google Photos Takeout and merge the metadata back
  into the correct files so they can be imported into another app like Immich.
---

# Google Photos Takeout

### Overview

Google Photos Takeout exports photos/videos plus separate `.json` metadata files. Most self-hosted photo apps expect metadata to be embedded in the media files.

This page helps you pick a tool to:

* merge Takeout `.json` metadata into the correct photos/videos
* optionally upload the results to Immich

{% hint style="warning" %}
I am not the creator of either project. These links are provided for convenience.

Always read the upstream README and release notes from the creators before running anything.
{% endhint %}

### Which one should you use?

Use the quick guide below, then click the linked page for the tool you choose.

#### Quick decision guide

* Want to do everything **locally** first, then upload later? Use [**Google Photo Takeout Helper**](google-photo-takeout-helper.md).
* Want to **process and upload to Immich in one step**? Use [**Immich-Go**](immich-go.md).

### Google Photo Takeout Helper

Best when you want a local, offline conversion step.

What it does:

* walks your Takeout export
* matches each media file to its `.json`
* writes metadata back into the photo/video file (so other apps can read it)

Notes:

* It can require **\~2× the storage** of your Takeout.
  * It may copy files into a new output structure.
* It has multiple options/prompts during processing.

[Google Photo Takeout Helper](google-photo-takeout-helper.md)

### Immich-Go

_Recommended for uploading a Google Photos Takeout to Immich._

Best when you want to process and upload in one workflow.

What it does:

* processes the Takeout (similar goal as the helper above)
* uploads directly to your Immich instance

[Immich-Go](immich-go.md)

{% hint style="info" %}
If you’re unsure, start with **Google Photo Takeout Helper**. It’s easier to validate the output before you upload anything.
{% endhint %}
