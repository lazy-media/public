# Discord - OAuth Authentication, Enrollment, & User Group Assignment Setup
### Original Documentation
- [Authentik Docs](https://goauthentik.io/integrations/sources/discord/)

### Explanation of Flow

This flow allows the use of Discord Login with Authentik. This explains how to create a deny stage to display a message to users if they are not part of your Discord Server. This flow creation will allow Authentik to verify a user against your Discord Server based on Server ID and Role ID, Assign them to an Authentik Group, and Add the Discord Login to the Main Authentik Login Page. Authentik will handle user creation upon a user's first login.

## Group Creation
- Login to Authentik Admin Panel
- Navigate to Directory > Groups
- Create a group for Discord Users

## Create a Deny Stage
- Navigate to Flows and Stages > Stages
- Create a new stage
- Select Deny Stage
- Enter your name as Discord Verification and enter the message of your choosing.
- Select Finish to save

## Authentication Flow Creation
- Navigate to Flows and Stages > Flows
- Create a new flow and name it Discord Authentication
- Designation is set as Authentication
- Click Finish
- Clicked on the new Discord Authentication flow and go to Stage Bindings
- Bind an existing stage and select the Deny Stage you just created. Binding order should be 0. Click Finish to save.
- Click the Expand arrow for the Discord Verification Deny Stage you just added, click Create and Bind Policy.
- Create an Expression Policy
- Add the following:
```
# To get the role and guild ID numbers for the parameters, open Discord, go to Settings > Advanced and
# enable developer mode.
# Right-click on the server/guild title and select "Copy ID" to get the guild ID.
# Right-click on the server/guild title and select server settings > roles, right click on the role and click
# "Copy ID" to get the role ID.

ACCEPTED_ROLE_ID = "CHANGE TO DISCORD ROLE ID"
ACCEPTED_GUILD_ID = "CHANGE TO DISCORD SERVER ID"
GUILD_NAME_STRING = "CHANGE TO SERVER NAME"
ROLE_NAME_STRING = "CHANGE TO ROLE NAME"

# Only change below here if you know what you are doing.
GUILD_API_URL = f"https://discord.com/api/users/@me/guilds/{ACCEPTED_GUILD_ID}/member"

# Ensure flow is only run during OAuth logins via Discord
if context['source'].provider_type != "discord":
    return True

# Get the user-source connection object from the context, and get the access token
connection = context.get("goauthentik.io/sources/connection")
if not connection:
  return False
access_token = connection.access_token

guild_member_object = requests.get(
    GUILD_API_URL,
    headers= {
        "Authorization": f"Bearer {access_token}",
    }
).json()

# The response for JSON errors is held within guild_member_object['code']
# See: https://discord.com/developers/docs/topics/opcodes-and-status-codes#json
# If the user isn't in the queried guild, it gives the somewhat misleading code = 10004.
if "code" in guild_member_object:
    if guild_member_object['code'] == 10004:
        ak_message(f"User is not a member of {GUILD_NAME_STRING}.")
    else:
        ak_create_event("discord_error", source=context['source'], code=guild_member_object['code'])
        ak_message("Discord API error, try again later.")
    # Policy does not match if there is any error.
    return False

user_matched = any(ACCEPTED_ROLE_ID == g for g in guild_member_object["roles"])
if not user_matched:
    ak_message(f"User is not a member of the {ROLE_NAME_STRING} role in {GUILD_NAME_STRING}.")
return user_matched
```
CHANGE THE FOLLOWING LINES WITHIN THE QUOTES IN THE CODE ABOVE BEFORE SAVING AND CONTINUING:
```
ACCEPTED_ROLE_ID = "CHANGE TO DISCORD ROLE ID"
ACCEPTED_GUILD_ID = "CHANGE TO DISCORD SERVER ID"
GUILD_NAME_STRING = "CHANGE TO SERVER NAME"
ROLE_NAME_STRING = "CHANGE TO ROLE NAME"
```
- Click Next to Save the Policy
- Create the binding with **NEGATE RESULT ENABLED** and **FAILURE RESULT is set to PASS**.
- Click Finish to Save
- Bind a second Existing Stage 
- Bind the "default-source-authentication-login"
- Go to Policies for the same Flow and add "default-source-authentication-if-sso"

## Enrollment Flow Creation
- Create a new Flow and Name it Discord Enrollment
- Click on the Flow and click Stage Bindings.
- Bind an existing stage and select your Discord Verification Deny Stage created above.
- Expand the Deny Stage.
- Add your Discord Verification Policy
- Make sure the binding has **NEGATE RESULT ENABLED** and **FAILURE RESULT is set to PASS**.
- Create and Bind a New Stage
- Choose User Write Stage
- Name it Discord Enrollment Writes
- Checked the box next to Create Users when Required
- Uncheck "Create new users as inactive".
- Leave User Path Template empty (autofilled later by Authentik)
- Select the group you want users to go into when enrolled
- Increment your order
- Click Finish or Update
- Bind another existing stage and bind "default-source-authentication-login"
- Increment your order
- Click Finsih or Update
- Go to the Policy Section of the same Flow and add "default-source-enrollment-if-sso"

## Federation & Social Login Creation + Flows Attachment
- Navigate to Directory > Federation & Social Login
- Create your Discord Federation & Social Login Provider
- Under the Scopes Section, enter the following:
```
guilds guilds.members.read
```
- At the very bottom of your Federation & Social Login Provider, expand Flow Settings
- Select your Discord flows for Authentication and Enrollment
- Under this OAuth Settings Page, I personally also made sure that the USER MATCHING MODE is set to "Link to a user with an identical email address. Can have security implications when a source doesn't validate email addresses." SET TO MATCH YOUR PREFERENCE.

## Add SSO & Flow to Login Page
- Go back to Flows
- Click on "default-authentication-flow"
- Go to "stage bindings"
- Edit stage for "default-authentication-identification"
- Expand Source Settings at the bottom
- Select your SSO providers that you setup. Hold CTRL + CLICK for multiple.
