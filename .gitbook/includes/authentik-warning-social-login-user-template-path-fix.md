---
title: Authentik Warning - Social Login User Template Path Fix
---

{% hint style="danger" %}
This small fix should not be needed but for some reason, Authentik does not allow the `User Path Template` Section to be left empty anymore. If for some reason you have issues with Social Login Enrollments, try these steps to fix it:

* While still in the Stage for Discord Enrollment Writes and in this section for `User Path Template` input:
* `goauthentik.io/sources/<your-federation-slug>`
  * To find your Federation Slug: Go to `Authentik Admin Panel > Directory > Federation and Social Login > Click Edit icon > Find Slug Field (second field usually)`
{% endhint %}
