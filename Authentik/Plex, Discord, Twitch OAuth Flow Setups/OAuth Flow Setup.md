# Plex, Discord, Twitch - OAuth Authentication, Enrollment, & User Group Assignment Setup

## Group Creation
- Create respective User Groups
## Authentication Flow Creation
- Created a new Flow and Named it Plex Authentication
- Designation is set as Authentication
- Clicked on the Plex Authentication to stage bindings.
- Bind the "default-source-authentication-login"
- Go to Policies for the same Flow and add "default-source-authentication-if-sso"
## Enrollment Flow Creation
- Created a new Flow and Named it Plex Enrollment
- Click on the Flow and click Stage Bindings.
- Create and Bind a New Stage
- Choose User Write Stage
- Named it Plex Enrollment Writes
- Checked the box next to Create Users when Required
- Uncheck "Create new users as inactive".
- I left User Path Template empty
- Select the group you want users to go into when enrolled
- Click Done or Update
- Bind a second existing stage and bind "default-source-authentication-login"
- Increment your order
- Click Done or Update
- Go to the Policy Section of the same Flow and add "default-source-enrollment-if-sso"
## Federation & Social Login Creation + Flows Attachment
- Create your Federation & Social Login OAuth Provider (i.e. Plex, Discord, Twitch)
- At the very bottom of your OAuth Provider, expand Flow Settings
- Select your respective flows for Authentication and Enrollment
- Under this OAuth Settings Page, I personally also made sure that the USER MATCHING MODE is set to "Link to a user with an identical email address. Can have security implications when a source doesn't validate email addresses."
## Add SSO & Flow to Login Page
- Go back to Flows
- Click on "default-authentication-flow"
- Go to "stage bindings"
- Edit stage for "default-authentication-identification"
- Expand Source Settings at the bottom
- Select your SSO providers that you setup.
