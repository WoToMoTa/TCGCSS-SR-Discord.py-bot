# HPSR-Discord.py-bot
Discord bot for Harry Potter SpeedRunning community  
Moved from private account

## How does it work
Every predefined amount of time, the bot checks for newly verified runs on the leaderboards of specified game series on Speedrun.com. Whenever there's a one, it buidls an embed, and forwards it to predefined Discord channel. It's a great tool for the community to keep up with the new within the new top runs, and for moderators, to share their progress with the rest of the people.

![Example embed](https://cdn.discordapp.com/attachments/852890956306448394/1170826148700229702/image.png?ex=655a73d2&is=6547fed2&hm=3a2d0eff59a6519ffa006580a982c939a605bcf25f9b0372b1c7adc5ec96e7a6&)  
## Now using Speedrun.com API v2
The latest rewrite allows easier customisation. The `settings.py` file should contain all the details the program needs to handle the games. Huge shout-outs to [Jamie](https://github.com/ManicJamie) for the [python wrapper](https://github.com/ManicJamie/speedruncompy), it's a great help!

#### GAME_SETTINGS
Each game should have colour, server ID, emote, and wr ping role set.
Required parameters:
- colour:  `int`  - determines the colour of the side bar of the created embed.
- server:  `int`  - ID of the Discord channel the message about new run is posted to.
- emotes:  `dict[int, str]`  - dictionary mapping what Discord emotes should be displayed if the runner achieved specific spot on the leaderboard.
- wr_ping: `list[str]`  - list of roles and/or users that will be pinged when the run was in fact a world record.

#### IL_MODE
Determines how the bot handles the Individual Level runs.
- 0 - Ignores them completely,
- 1 - Forwards them to appropiate channel, but doesn't send pings in case of World Records,
- 2 - Treats them normally, like any other run.

#### FREQUENCY_MINUTES
How often does the program check for the new runs in the series. Not recommended to set it below 1 minute, though setting it below 15 is probably an overkill already.

#### SERIES_ID
List the IDs of series the bot is supposed to follow.