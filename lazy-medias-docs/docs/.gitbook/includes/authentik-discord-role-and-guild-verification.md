---
title: Authentik - Discord Role & Guild Verification
---

{% code expandable="true" %}
```py
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
{% endcode %}
