import zoneinfo

import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os

# Load necessary libraries for the time zones, databases, etc.
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import datetime
import json

validTimezones = zoneinfo.available_timezones()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

# Need to manually enable intents both in the Discord page and here
intents.message_content = True
intents.members = True
allowed_mentions = discord.AllowedMentions(users=False)

bot = commands.Bot(command_prefix='/', intents=intents, allowed_mentions=allowed_mentions)

# Autocomplete possible timezones
async def timezoneCompletion(interaction, current:str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=option, value=option)
        for option in validTimezones if current.lower() in option.lower()
    ][:25] # Solution online: limit the list to 25 entries to comply with Discord's rate limits

# Bot capabilities
@bot.event
async def on_ready():
    print(f"Test test test 1 2 3, {bot.user.name}")


@bot.hybrid_command()
async def sync(ctx):
    await bot.tree.sync()


@bot.hybrid_group()
async def timezone(ctx):
    await ctx.send("Timezone command detected")


@timezone.command(name="set", description="Set a user's timezone")
@app_commands.autocomplete(timezone=timezoneCompletion)
async def set(ctx, timezone, user: discord.Member):

    # Validate the timezone provided
    try:
        ZoneInfo(timezone)
        #await ctx.send(f"Setting {user.mention}'s timezone to {timezone}")

        # Some JSON file to store all the user data for now because there is only twelve testers
        with open("testerTimezones.json", "r") as file:
            existingUsers = json.load(file)

        existingUsers[str(user.id)] = {
            "timezone": timezone
        }

        with open("testerTimezones.json", "w", encoding="utf-8") as newFile:
            json.dump(existingUsers, newFile, indent=4)

        await ctx.send(f"Successfully updated {user.mention}'s timezone to `{timezone}`!")
    except ZoneInfoNotFoundError:
        await ctx.send("Invalid IANA timezone. Please select from the list provided.")


@timezone.command(name="remove", description="Remove a user from the list")
async def remove(ctx, user: discord.Member):
    with open("testerTimezones.json", "r") as file:
        existingUsers = json.load(file)

    # Verify that the mentioned user exists in the JSON file
    if str(user.id) in existingUsers:
        del existingUsers[str(user.id)]

        with open("testerTimezones.json", "w", encoding="utf-8") as newFile:
            json.dump(existingUsers, newFile, indent=4)

        await ctx.send(f"Successfully removed {user.mention} from the list!")
    else:
        await ctx.send(f"{user.mention} is not in the list. Original list is maintained.")


@timezone.command(name="clear", description="Clear all timezones saved")
async def clear(ctx):
    with open("testerTimezones.json", "r") as file:
        existingUsers = json.load(file)

    # Clear dictionary
    existingUsers.clear()

    with open("testerTimezones.json", "w", encoding="utf-8") as newFile:
        json.dump(existingUsers, newFile, indent=4)

    await ctx.send(f"Successfully cleared all saved timezones!")


@timezone.command(name="availability", description = "Get an overview of everyone's availability")
async def availability(ctx):
    with open("testerTimezones.json", "r") as file:
        allUsers = json.load(file)

    availableMembers = []
    possiblyAvailableMembers = []
    unavailableMembers = []

    # Sort members based on the hour of day in their timezone
    # TODO: New parameter to outright declare unavailability, which will override the timezone
    for i in allUsers:
        #await ctx.send(f"<@{int(i)}>'s current time is {datetime.now(ZoneInfo(allUsers[i]["timezone"]))}")
        if datetime.now(ZoneInfo(allUsers[i]["timezone"])).hour <= 6:
            unavailableMembers.append(i)
        elif datetime.now(ZoneInfo(allUsers[i]["timezone"])).hour <= 9:
            possiblyAvailableMembers.append(i)
        elif datetime.now(ZoneInfo(allUsers[i]["timezone"])).hour <= 17:
            availableMembers.append(i)
        elif datetime.now(ZoneInfo(allUsers[i]["timezone"])).hour <= 23:
            possiblyAvailableMembers.append(i)
        else:
            unavailableMembers.append(i)

    # Format all members nicely based on their availability
    availableString = ""
    possiblyAvailableString = ""
    unavailableString = ""

    for i in availableMembers:
        currentTime = datetime.now(ZoneInfo(allUsers[i]["timezone"]))
        availableString = availableString + f"<@{int(i)}> - {currentTime.hour:02d}:{currentTime.minute:02d}\n"

    for i in possiblyAvailableMembers:
        currentTime = datetime.now(ZoneInfo(allUsers[i]["timezone"]))
        possiblyAvailableString = possiblyAvailableString + f"<@{int(i)}> - {currentTime.hour:02d}:{currentTime.minute:02d}\n"

    for i in unavailableMembers:
        currentTime = datetime.now(ZoneInfo(allUsers[i]["timezone"]))
        unavailableString = unavailableString + f"<@{int(i)}> - {currentTime.hour:02d}:{currentTime.minute:02d}\n"

    # Create and display the Discord Embed message
    newEmbed = discord.Embed(title="Tester Timezones", description="NOTE: The following is based on normal work hours, and does not indicate anyone's actual availability!", color=5793266)
    newEmbed.add_field(name="🟢 Available", value=availableString, inline=False)
    newEmbed.add_field(name="🟡 Possibly Available", value=possiblyAvailableString, inline=False)
    newEmbed.add_field(name="🔴 Unavailable", value=unavailableString, inline=False)
    await ctx.send(embed=newEmbed)

    # Idea: save region with flags, display flag in the Embed
bot.run(token, log_handler=handler, log_level=logging.DEBUG)