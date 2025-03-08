# Discord - OAuth Authentication, Enrollment, & User Group Assignment Setup
### Original Documentation
- [Authentik Docs](https://goauthentik.io/integrations/sources/discord/)

### Explanation of Flow

This flow allows the use of Discord Login with Authentik. This explains how to create a deny stage to display a message to users if they are not part of your Discord Server. This flow creation will allow Authentik to verify a user against your Discord Server based on Server ID and Role ID, Assign them to an Authentik Group, and Add the Discord Login to the Main Authentik Login Page. Authentik will handle user creation upon a user's first login.

## Group Creation
- Login to Authentik Admin Panel
    - Navigate to `Directory > Groups`
    - Create a group for `Discord Users`

## Deny Stages

### Standard Deny Stage with No Discord Server Join Message
- Navigate to `Flows and Stages > Stages`
- Create a new stage
- Select Deny Stage
    - Enter your name as `Discord Deny Verification` and enter a message of your choosing.
- Select `Finish` to save

### Deny Stage with Join Discord Server Message
For Easier Setup, Create the `Authentication Flow` and the `Discord Expression Policy` in the next step, then come back to this step.

- Login to you Authentik Admin Panel
- Navigate to `Flows and Stages > Prompts`
  - Create a new Prompt
  - Put what you want in the `Name`, `Field Key` and `Label` boxes.
  - Select the Prompt Type as `Static: Static Value, Displayed as-is`
  - Scroll down to `Help Text`
  - Insert the following (Change what is needed):
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CHANGE ME</title>
    <style>
        /* Center the button horizontally */
        #join-button {
            height: 50%;
            width: 50%;
            margin: auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* Style the button */
        #join-button {
          background-color: #3498db;
          color: white;
          padding: 10px;
          border: none;
          border-radius: 15px;
          cursor: pointer;
          text-decoration: none;
        }
    </style>
</head>
<body>
  <p>
    <center>
      <b>
        INSERT YOUR MESSAGE HERE.
        <br>
        IN BASIC HTML CODE.
      </b>
      <br>
      JUST KEEP YOUR CODE BETWEEN THE <center> & </center>
    </center>
  </p>
    <a id="join-button" href="DISCORD JOIN URL" target="_blank" rel="noopener noreferrer">Join Join the Discord Server Now!</a>
</body>
</html>
```

- Navigate to `Flows and Stages > Stages`
- Create a New Prompt Stage
  - Name the Prompt whatever you want
  - Under `Fields` in the right column, if there is anything in it, remove everything except for the `Prompt` we just created. If the newly created `Prompt` is not selected, select it and move it to the right column.
  - Under `Validation Policies`, Do the same thing and remove everything from the right column except for the `Discord Verification Policy` created in the next step.
- Navigate to `Flows and Stages > Flows`
  - Find your `Discord Authentication` Flow and Click on it
    - Click on `Stage Bindings`
    - Bind an Existing Stage and Bind your `Discord Prompt` we just created, change the order to `0` or the lowest number, and click `Create`
    - Expand the Stage we just added
    - Click on `Bind Existing Policy / Group / User`
    - Under `Policy`, select your `Discord Verification` Policy
      - MAKE SURE THE `ENABLED` and `NEGATE RESULTS` are both checked.
      - SET `FAILURE RESULT` to `PASS`


## Authentication Flow Creation
- Navigate to `Flows and Stages > Flows`
- Create a new flow and name it `Discord Authentication`
- `Designation` is set as `Authentication`
- Click `Finish`
- Click on the new `Discord Authentication` flow and go to `Stage Bindings`
- `Bind an existing stage` and select the `Deny Stage` you just created. `Binding order should be 0`. Click `Finish` to save.
- Click the `Expand arrow` for the `Discord Verification Deny Stage` you just added, click `Create and Bind Policy`.
- Create an `Expression Policy`
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
- Click `Next` to Save the Policy
- Create the binding with `NEGATE RESULT ENABLED` and `FAILURE RESULT` is set to `PASS`.
- Click `Finish` to Save
- Bind a second Existing Stage 
- Bind the `default-source-authentication-login`
- Increment your Order to `10`
- Click `Finish` or `Update`
- Go to `Policies` for the same Flow and add `default-source-authentication-if-sso`

## Enrollment Flow Creation
- Create a new Flow and Name it `Discord Enrollment`
- Click on the Flow and click `Stage Bindings`.
- Bind an existing stage and select your `Discord Verification Deny Stage` created above.
- Click the Expand arrow on the `Deny Stage`.
- Add your `Discord Verification Policy`
- Make sure the binding has `NEGATE RESULT ENABLED` and `FAILURE RESULT` is set to `PASS`.
- Bind an existing stage and bind `default-source-authentication-login`
- Increment your order to `10`
- Click `Finish` or `Update`
- Create and Bind a New Stage
- Choose `User Write Stage`
- Name it `Discord Enrollment Writes`
- Checked the box next to `Create Users when Required`
- Uncheck `Create new users as inactive`.
- Leave `User Path Template empty` (autofilled later by Authentik)
- Select the group you want users to go into when enrolled
- Increment your order to `20`
- Click `Finish` or `Update`
- Go to the `Policy Section` of the same Flow and add `default-source-enrollment-if-sso`

## Federation & Social Login Creation + Flows Attachment
- Navigate to `Directory > Federation & Social Login`
- Create your `Discord Federation & Social Login Provider`
- Under the `Scopes Section`, enter the following:
```
guilds guilds.members.read
```
- At the very bottom of your Federation & Social Login Provider, **Expand** `Flow Settings`
- Select your Discord flows we just created above for `Authentication` and `Enrollment`
- Under this OAuth Settings Page, I personally also made sure that the `USER MATCHING MODE` is set to `Link to a user with an identical email address. Can have security implications when a source doesn't validate email addresses.` CHANGE TO MATCH YOUR PREFERENCE.

## Add SSO & Flow to Login Page
- Navigate to `Flows & Stage > Flows`
- Click on `default-authentication-flow`
- Go to `Stage Bindings`
- Edit stage for `default-authentication-identification`
- **Expand** `Source Settings` at the bottom
- Select your SSO providers that you setup. Hold CTRL + CLICK for multiple.
