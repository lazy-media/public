# Discord Verification Flow Setup
This is assuming you have followed the guide from [Authentik OAuth Setup](https://gitlab.lazymedia.media/lazymedia/authentik/-/blob/9236f51bc5693c6812d89e5000ae9487e0fdc96e/Flows%20Setup/OAuth%20Flow%20Setup.md) and have setup separate Authentication and Enrollment Flows for Discord.
## Discord Guild & Role Verification Setup
## Editing Authentication Flow
- Go to Flows & Stages
- Click on Flows
- Find your Discord Authentication Flow and Click on it.
- Click on Stage Bindings
- Expand default-source-authentication-login
- Create and Bind an Existing Policy
- Create an Expression Policy
- I named mine Discord Guild and Role Verification
- Copy and paste the last Expression from the Authentik Docs making sure to change the fields that are required.
- Click Save.
- This should put a Policy Under the default-source-authentication-login.
## Authentik Docs & Discord Code
[Authentik Docs](https://goauthentik.io/integrations/sources/discord/)
---
**MAKE SURE TO CHANGE THE FIRST 4 UNCOMMENTED (#) LINES WITHIN THE PARENTHESIS ("") TO MATCH YOUR DISCORD INFORMATION!**

- Guild ID = Server ID
- Role ID = Role ID
```
# To get the role and guild ID numbers for the parameters, open Discord, go to Settings > Advanced and
# enable developer mode.
# Right-click on the server/guild title and select "Copy ID" to get the guild ID.
# Right-click on the server/guild title and select server settings > roles, right click on the role and click
# "Copy ID" to get the role ID.

ACCEPTED_ROLE_ID = "123456789123456789"
ACCEPTED_GUILD_ID = "123456789123456789"
GUILD_NAME_STRING = "The desired server/guild name in the error message."
ROLE_NAME_STRING = "The desired role name in the error message."

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
## Editing Authentication & Enrollment Flows
- Go to Flows & Stages
- Click on Flows
- Find your Discord Enrollment Flow and Click on it.
- Click on Stage Bindings
- Expand default-source-authentication-login
- Bind existing Policy and choose the Policy you created above.
- Do the same for your Custom Discord Authentication Flow too.

## Editing Discord OAuth Federation & Social Login Settings
If using the code above, you will need to edit the following:
- Go to Authentik Admin Panel
- Go to Directory
- Go to Federation & Social Login
- Click the edit button on the right side of your Discord OAuth
- Under SCOPES, add ```guilds guilds.members.read```

## Explanation
This will at least verify a user against your Discord Server and the Role you selected. If they are not authenticated on your Discord Server, Authentik will toss the user back to the Authentik Login screen. This does not display a message to the user saying they need to join the Discord Server in order to gain access (still trying to figure this out). This will also create an Authentik user too but not allow login until verified on Discord.
