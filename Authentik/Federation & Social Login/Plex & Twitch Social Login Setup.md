# Plex & Twitch - OAuth Authentication, Enrollment, & User Group Assignment Setup

## Group Creation
- Create respective User Groups

## Authentication Flow Creation
- Created a new Flow and Named it respectively
- Designation is set as Authentication
- Click Save
- Clicked on the New Authentication Flow to stage bindings.
- Bind the "default-source-authentication-login"
- Go to Policies for the same Flow and add "default-source-authentication-if-sso"

## Enrollment Flow Creation
- Created a new Flow and Named it respectively
- Click on the Flow and click Stage Bindings.
- Create and Bind a New Stage
- Choose User Write Stage
- Named it 'RESPECTIVE SOURCE' Enrollment Writes
- Checked the box next to Create Users when Required
- Uncheck "Create new users as inactive".
- Leave User Path Template empty (autofilled later by Authentik)
- Select the group you want users to go into when enrolled
- Click Done or Update
- Bind a second existing stage and bind "default-source-authentication-login"
- Increment your order
- Click Done or Update
- Go to the Policy Section of the same Flow and add "default-source-enrollment-if-sso"

## Federation & Social Login Creation + Flows Attachment
- Create your Federation & Social Login Provider (i.e. Plex, Discord, Twitch)
- At the very bottom of your Federation & Social Login Provider, expand Flow Settings
- Select your respective flows for Authentication and Enrollment
- Under this OAuth Settings Page, I personally also made sure that the USER MATCHING MODE is set to "Link to a user with an identical email address. Can have security implications when a source doesn't validate email addresses." SET TO MATCH YOUR PREFERENCE.

## Add SSO & Flow to Login Page
- Go back to Flows
- Click on "default-authentication-flow"
- Go to "stage bindings"
- Edit stage for "default-authentication-identification"
- Expand Source Settings at the bottom
- Select your SSO providers that you setup. Hold CTRL + CLICK for multiple.
