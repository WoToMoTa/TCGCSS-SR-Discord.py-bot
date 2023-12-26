import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from random import randint
import tracemalloc
import discord
from discord.ext import commands, tasks
import speedruncompy
import json
from utilis.verify_settings import *


tracemalloc.start()
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
verifySettings('settings.json')
with open('settings.json', 'r') as settingsFile:
    settings = json.load(settingsFile) 

class Run:
    def __init__(self, runData: dict, categoryData: dict, gameData: dict, levelData: dict|None, valuesData: list[dict], variablesData: list[dict], playersData: list[dict]) -> None:
        self.id = runData['id']
        self.position = runData['place']
        self.time = runData['time'] if 'time' in runData else runData['timeWithLoads']
        self.dateSubmitted = runData['dateSubmitted']

        self.gameInfo = {
            'id': gameData['id'],
            'name': gameData['name'],
            'abbreviation': gameData['url'],
            'cover': 'https://www.speedrun.com'+gameData['coverPath'],
        }
        self.settings = settings['games'].get(self.gameInfo['id'], settings['games']['default'])

        self.categoryInfo = {
            'id': categoryData['id'],
            'name': categoryData['name'],
        }

        self.isFullGame = levelData == None
        if not self.isFullGame:
            self.levelInfo = {
                'id': levelData['id'],
                'name': levelData['name'],
            }

        self.subcategories = {
            variableData['id']: variableData['isSubcategory'] for variableData in variablesData
        }
        
        self.valuesInfo = [
            {
                'id': valueData['id'],
                'name': valueData['name'],
                'variableId': valueData['variableId'],
            } for valueData in valuesData if self.subcategories[valueData['variableId']]
        ]
        
        self.playersInfo = [
            {
                'id': playerData['id'],
                'name': playerData['name'],
                'url': f'https://www.speedrun.com/users/{playerData["url"]}' if 'url' in playerData else None,
                'image': f'https://www.speedrun.com/static/user/{playerData["id"]}/image' if 'url' in playerData else None,
                'country': (playerData['areaId'].split('/')[0] if playerData['areaId'] != '' else None) if 'areaId' in playerData else None,
            } for playerData in playersData
        ]

        self.weblink = f'https://www.speedrun.com/{self.gameInfo["abbreviation"]}/runs/{self.id}'
        self.leaderboardLink = f'https://www.speedrun.com/{self.gameInfo["abbreviation"]}?x={"l_"+self.levelInfo["id"]+"-" if not self.isFullGame else ""}{self.categoryInfo["id"]}{"".join(["-"+value["variableId"]+"."+value["id"] for value in self.valuesInfo])}'
        if self.position == 1 and (self.isFullGame or (not self.isFullGame and self.settings['il_mode'] > 1)):
            self.pings = ' '.join(self.settings['wr_ping'])
        else:
            self.pings = ''


class RunEmbed(discord.Embed):
    def __init__(self, run: Run) -> None:
        self.run = run
        colour = self.run.settings['colour']
        description = self.runDescription()
        timestamp = datetime.fromtimestamp(self.run.dateSubmitted, timezone.utc)
        super().__init__(colour=colour, description=description, timestamp=timestamp)

        self.set_author(
            name = self.categoryDisplay(),
            url = self.run.leaderboardLink,
            icon_url = run.playersInfo[0]['image'] if len(run.playersInfo)==1 else None
        )
        self.set_thumbnail(url=self.run.gameInfo['cover'].replace('gameasset', 'static/game'))

    def runDescription(self) -> str:
        elements = []
        if str(self.run.position) in self.run.settings['emotes']:
            elements.append(self.run.settings['emotes'][str(self.run.position)])
        elements.append(f'{FormatText.ordinalPosition(self.run.position)} place:')
        elements.append(f'[{self.convertTimeFormat(self.run.time)}]({self.run.weblink})')
        elements.append('by')
        elements.append(self.playersDisplay())
        
        return ' '.join(elements)
          
    def convertTimeFormat(self, t: float) -> str:
        hours = int(t/60/60)
        minutes = int(t/60%60)
        seconds = int(t%60)
        milliseconds = round(t%1*1000)

        if 'lowcast' in self.categoryDisplay().lower():
            return "%d:%02d:%02d (%d casts)" % (minutes, seconds, milliseconds/10, hours)
        elif t > 600:
            return "%d:%02d:%02d" % (hours, minutes, seconds)
        else:
            return "%d:%02d.%03d" % (minutes, seconds, milliseconds) 
        
    def playersDisplay(self) -> str:
        playersInfo = self.run.playersInfo
        displayPlayers = ''
        for count, player in enumerate(playersInfo):
            if (len(playersInfo) > 1) and (count == len(playersInfo) - 1):
                displayPlayers += ' and '
            elif len(playersInfo) > 1 and count >= 1:
                displayPlayers += ', '
            if player['url'] is not None:
                flag = FormatText.getFlagEmoji(player["country"]) + " " if player["country"] != "" else ""
                displayPlayers += f'{flag}[{player["name"]}]({player["url"]})'
            else:
                displayPlayers += player['name']

        return displayPlayers
    
    def categoryDisplay(self) -> str:
        elements = []
        elements.append(self.run.gameInfo['name'])
        if not self.run.isFullGame:
            elements.append(self.run.levelInfo['name'])
        categoryElements = [self.run.categoryInfo['name']] + [value['name'] for value in self.run.valuesInfo]
        elements.append(', '.join(categoryElements))
        
        return '\n'.join(elements)
    

class streamEmbed(discord.Embed):
    def __init__(self, streamData, gameData, userData) -> None:
        super().__init__()
        authorName = userData['name']
        userAssets = [asset for asset in userData['staticAssets'] if asset['assetType'] == 'image']
        authorIcon = 'https://www.speedrun.com' + userAssets[0]['path'] if userAssets else None
        authorLink = 'https://www.speedrun.com/user/'+userData['url']
        twitchLink = 'https://www.twitch.tv/' + streamData['channelName']
        title = streamData['title']
        gameSettings = settings['games'][gameData['id']]
        gameName = gameSettings.get('display_name', gameData['name'])
        self.colour = 0xffffff if streamData['hasPb'] else 0x000000
        self.title = title
        self.url = twitchLink
        self.area = streamData['areaId']
        self.set_image(url=streamData['previewUrl'])
        self.message = f'{FormatText.getFlagEmoji(self.area)} [{streamData["channelName"]}]({twitchLink}) is streaming {gameSettings["emote"]} {gameName}!'
        self.set_author(
            name = authorName,
            icon_url = authorIcon,
            url = authorLink
        )
        self.servers = gameSettings['stream_notif']


class FormatText:
    @staticmethod
    def ordinalPosition(n: int) -> str:
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]

        return str(n) + suffix
    
    @staticmethod
    def getFlagEmoji(countryCode: str|None) -> str:
        if countryCode == None: return ''
        codePoints = [127397 + ord(char) for char in countryCode.upper()]

        return ''.join(chr(codePoint) for codePoint in codePoints)


class GetRun(speedruncompy.GetRequest):
    def __init__(self, runId: str = None, **params) -> None:
        super().__init__("GetRun", runId=runId, **params)


class GetStreamList(speedruncompy.GetRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetStreamList", **params)


async def initialPrep() -> None:
    global rememberedRuns
    rememberedRuns = []
    for series in settings['series']:
        endpoint = speedruncompy.GetLatestLeaderboard(seriesId=series, limit=100)
        data = endpoint.perform()
        latestRuns = [run['id'] for run in data['runs']]
        rememberedRuns += latestRuns



client = commands.Bot(command_prefix='/', intents=discord.Intents.default(), allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=True))
rememberedRuns = []
rememberedStreams: dict[str, discord.Message] = {}


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    try: 
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    await initialPrep()
    print("Ready!")
    mainloop.start()


@tasks.loop(minutes = settings['loop_period'])
async def mainloop():
    await checkForNewRuns()
    await checkForNewStreams()


async def checkForNewRuns():
    global rememberedRuns

    newRuns: list[Run] = []
    for series in settings['series']:
        endpoint = speedruncompy.GetLatestLeaderboard(
            seriesId=series, 
            limit=20,
            vary=randint(0, 1_000_000)
            )
        data = endpoint.perform()
        for run in data['runs']:
            if run['id'] not in rememberedRuns:
                newRun = Run(
                    run,
                    [categoryData for categoryData in data['categories'] if categoryData['id'] == run['categoryId']][0],
                    [gameData for gameData in data['games'] if gameData['id'] == run['gameId']][0],
                    [levelData for levelData in data['levels'] if levelData['id'] == run['levelId']][0] if 'levelId' in run else None,
                    [valueData for valueData in data['values'] if valueData['id'] in run['valueIds']],
                    data['variables'],
                    [playerData for playerData in data['players'] if playerData['id'] in run['playerIds']]
                ) 

                if newRun.settings['il_mode'] == 0:
                    if not newRun.isFullGame:
                        continue

                newRuns.append(newRun)
                if len(rememberedRuns) < 1000:
                    rememberedRuns = [newRun.id] + rememberedRuns
                else:
                    rememberedRuns = [newRun.id] + rememberedRuns[999:]

    for newRun in newRuns:
        print(datetime.utcnow(), 'new run:', newRun.weblink)
        sentMessage = await client.get_channel(newRun.settings['server']).send(newRun.pings, embed=RunEmbed(newRun))
        reactionEmote = newRun.settings['emotes'].get(str(newRun.position), None)
        if reactionEmote != None:
            await sentMessage.add_reaction(reactionEmote)

async def checkForNewStreams():
    seriesId = '15ndxp7r'
    endpoint = GetStreamList(seriesId=seriesId, vary=randint(0, 1_000_000))
    data = endpoint.perform()
    streamsToDelete = []
    for user in rememberedStreams.keys():
        if user not in [streamData['channelName'] for streamData in data['streamList']]:
            streamsToDelete.append(user)
    for user in streamsToDelete:
        print(f"Deleting {user}'s stream")
        await rememberedStreams[user].delete()
        del rememberedStreams[user]
    for streamData in data['streamList']:
        if streamData['channelName'] not in rememberedStreams.keys():
            gameData = [game for game in data['gameList'] if streamData['gameId'] == game['id']][0]
            userData = [user for user in data['userList'] if streamData['userId'] == user['id']][0]
            embed = streamEmbed(streamData, gameData, userData)
            for server in embed.servers:
                message: discord.Message = await client.get_channel(server).send(embed.message, embed=embed)
                rememberedStreams[streamData['channelName']] = message


@client.tree.command(name='run_to_embed')
@discord.app_commands.describe(run_id = 'ID of the run you want to embed')
async def run_to_embed(interaction: discord.Interaction, run_id: str):
    endpoint = GetRun(runId=run_id)
    data = endpoint.perform()
    runToEmbed = Run(
        data['run'],
        data['category'],
        data['game'],
        data['level'] if 'levelId' in data['run'] else None,
        data['values'],
        data['variables'],
        data['players']
    ) 

    await interaction.response.send_message(embeds=[RunEmbed(runToEmbed)])


client.run(DISCORD_TOKEN)
