---
description: Information on how to setup Plex & Twitch OAuth in Authentik.
---

# Plex & Twitch - OAuth Authentication, Enrollment, & User Group Assignment Setup

## Group Creation

* Create respective User Groups

## Authentication Flow Creation

1. Created a new Flow and Named it respectively
2. Designation is set as Authentication
3. Click Save
4. Clicked on the New Authentication Flow to stage bindings.
5. Bind the "default-source-authentication-login"
6. Go to Policies for the same Flow and add "default-source-authentication-if-sso"

## Enrollment Flow Creation

1. Created a new Flow and Named it respectively
2. Click on the Flow and click Stage Bindings.
3. Create and Bind a New Stage
4. Choose User Write Stage
5. Named it as you see fit for Enrollment Writes
6. Checked the box next to Create Users when Required
7. Uncheck "Create new users as inactive".
8. Leave User Path Template empty (autofilled later by Authentik)
9. Select the group you want users to go into when enrolled
10. Click Done or Update
11. Bind a second existing stage and bind "default-source-authentication-login"
12. Increment your order
13. Click Done or Update
14. Go to the Policy Section of the same Flow and add "default-source-enrollment-if-sso"

{% include "../../.gitbook/includes/authentik-social-login-fix-for-user-path-template.md" %}

## Federation & Social Login Creation + Flows Attachment

1. Create your Federation & Social Login Provider (i.e. Plex, Discord, Twitch)
2. At the very bottom of your Federation & Social Login Provider, expand Flow Settings
3. Select your respective flows for Authentication and Enrollment
4. Under this OAuth Settings Page, I personally also made sure that the USER MATCHING MODE is set to "Link to a user with an identical email address. Can have security implications when a source doesn't validate email addresses." SET TO MATCH YOUR PREFERENCE.

## Add SSO & Flow to Login Page

1. Go back to Flows
2. Click on "default-authentication-flow"
3. Go to "stage bindings"
4. Edit stage for "default-authentication-identification"
5. Expand Source Settings at the bottom
6. Select your SSO providers that you setup. Hold CTRL + CLICK for multiple.
