# EZ-TZ Discord Bot

## Introduction

As the solo developer of [Get the Vote on Roblox](https://www.roblox.com/games/123438982105045/Get-the-Vote), I am fortunate to have a team of testers who are able to give feedback on upcoming updates.
However, we all live in different parts of the world, including North America, Europe, and  Asia.

It's important for me to know who is awake at a minute's notice, such as when I make last minute changes before a scheduled release. Going off of someone's online status on Discord is not reliable enough. Some may not have Discord open, while others may have set their status to Invisible.

Also, tester gaming sessions have been more common lately. Currently, members usually ping all other testers to see who would be down to play, which has annoyed a few testers who think they're being pinged for something important.

Both of these things have led me to creating EZ-TZ, a simple Discord bot that allows users to set their timezone, which allows others to get their local time and possible availability. While this bot doesn't indicate anyone's actual availability, it allows the team to be more mindful of everyone's local time instead of pinging someone in the middle of the night.

## Features
EZ-TZ contains the following features:
- Timezone management
- Local-time conversion
- Availability overviews and indicators
- Persistent user data (via a JSON file)

## Getting started

To get this bot running, you will need to create your own application on the Discord Developer Portal.

1. Create an application on the Discord Development Portal
2. Copy your bot's token
3. Replace `your_token_here` in .env with your copied bot token
4. Install the requirements using `pip install -r requirements.txt` 
5. Run the Python script!

## Commands

You can assign a timezone using the following command
`/timezone set [timezone: String] [user: discord.Member]`

To get a comprehensive overview of all members with defined timezones, use the command
`/timezone availability`

To remove a user from the list, use
`/timezone remove [user: discord.Member]`

And to clear the entire list, use
`/timezone clear`
