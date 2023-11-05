import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from random import randint
import tracemalloc
import discord
from discord.ext import commands, tasks
import speedruncompy
from settings import FREQUENCY_MINUTES, GAME_SETTINGS, IL_MODE, SERIES_ID


tracemalloc.start()
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class Run:
    def __init__(self, runData: dict, categoryData: dict, gameData: dict, levelData: dict|None, valuesData: list[dict], variablesData: list[dict], playersData: list[dict]) -> None:
        self.id = runData['id']
        self.position = runData['place']
        self.time = runData['time'] if 'time' in runData else runData['timeWithLoads']
        self.dateVerified = runData['dateVerified']

        self.gameInfo = {
            'id': gameData['id'],
            'name': gameData['name'],
            'abbreviation': gameData['url'],
            'cover': 'https://www.speedrun.com'+gameData['coverPath'],
        }
        self.settings = GAME_SETTINGS.get(self.gameInfo['id'], GAME_SETTINGS['default'])

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
        if self.position == 1 and (self.isFullGame or (not self.isFullGame and IL_MODE > 1)):
            self.pings = ' '.join(self.settings['wr_ping'])
        else:
            self.pings = ''


class RunEmbed(discord.Embed):
    def __init__(self, run: Run) -> None:
        self.run = run
        colour = self.run.settings['colour']
        description = self.runDescription()
        timestamp = datetime.fromtimestamp(self.run.dateVerified, timezone.utc)
        super().__init__(colour=colour, description=description, timestamp=timestamp)

        self.set_author(
            name = self.categoryDisplay(),
            url = self.run.leaderboardLink,
            icon_url = run.playersInfo[0]['image'] if len(run.playersInfo)==1 else None
        )
        self.set_thumbnail(url=self.run.gameInfo['cover'].replace('gameasset', 'static/game'))

    def runDescription(self) -> str:
        elements = []
        if self.run.position in self.run.settings['emotes']:
            elements.append(self.run.settings['emotes'][self.run.position])
        elements.append(f'{self.ordinalPosition(self.run.position)} place:')
        elements.append(f'[{self.convertTimeFormat(self.run.time)}]({self.run.weblink})')
        elements.append('by')
        elements.append(self.playersDisplay())
        
        return ' '.join(elements)
        
        
    def ordinalPosition(self, n: int) -> str:
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]

        return str(n) + suffix
    
    def convertTimeFormat(self, t: float) -> str:
        hours = int(t/60/60)
        minutes = int(t/60%60)
        seconds = int(t%60)
        milliseconds = round(t%1*1000)

        if 'lowcast' in self.run.categoryInfo['name'].lower():
            return "%d:%02d:%02d (%d casts)" % (minutes, seconds, milliseconds/10, hours)
        elif t > 600:
            return "%d:%02d:%02d" % (hours, minutes, seconds)
        else:
            return "%d:%02d.%03d" % (minutes, seconds, milliseconds) 
        
    def getFlagEmoji(self, countryCode: str|None) -> str:
        if countryCode == None: return ''
        codePoints = [127397 + ord(char) for char in countryCode.upper()]

        return ''.join(chr(codePoint) for codePoint in codePoints)
        
    def playersDisplay(self) -> str:
        playersInfo = self.run.playersInfo
        displayPlayers = ''
        for count, player in enumerate(playersInfo):
            if (len(playersInfo) > 1) and (count == len(playersInfo) - 1):
                displayPlayers += ' and '
            elif len(playersInfo) > 1 and count >= 1:
                displayPlayers += ', '
            if player['url'] is not None:
                flag = self.getFlagEmoji(player["country"]) + " " if player["country"] != "" else ""
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
    
    
def initialPrep():
    global rememberedRuns
    rememberedRuns = []

    for series in SERIES_ID:
        endpoint = speedruncompy.GetLatestLeaderboard(seriesId=series, limit=100)
        data = endpoint.perform()
        latestRuns = [run['id'] for run in data['runs']]
        rememberedRuns += latestRuns



client = commands.Bot(command_prefix='/', intents=discord.Intents.default(), allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=True))
rememberedRuns = []


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    initialPrep()
    mainloop.start()


@tasks.loop(minutes = FREQUENCY_MINUTES)
async def mainloop():
    global rememberedRuns

    newRuns: list[Run] = []
    for series in SERIES_ID:
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

                if IL_MODE == 0:
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
        reactionEmote = newRun.settings['emotes'].get(newRun.position, None)
        if reactionEmote != None:
            await sentMessage.add_reaction(reactionEmote)


client.run(DISCORD_TOKEN)
