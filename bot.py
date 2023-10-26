import discord
from discord.ext import commands
from discord.ext import tasks
from requests import get
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
from dotenv import load_dotenv
import tracemalloc


tracemalloc.start()
load_dotenv()
BASE_LINK = 'https://www.speedrun.com/api/v1/'
FREQUENCY_MINUTES = 5
CHANNEL_ID_TEST = 1029384953189896322
CHANNEL_ID_MAIN = 597203792055894016
CHANNEL_ID_HL = 1064229439627604119
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


class Player:
	def __init__(self, rel: str, apiLink: str) -> None:
		apiInfo = apiResponse(apiLink)
		if rel == 'user':
			self.name = apiInfo['names']['international']
			self.weblink = apiInfo['weblink']
			self.displayName = "[%s](%s)" % (self.name, self.weblink)
			self.picture = apiInfo['assets']['image']['uri']
		elif rel == 'guest':
			self.name = apiInfo['name']
			self.weblink = ''
			self.displayName = self.name
			self.picture = ''


class Run:
	def __init__(
			self,
			id: str,
			weblink: str,
			time: float,
			submittedTime: str,
			game,
			categoryID: str,
			players: list,
			values: dict,
			) -> None:
		self.id = id
		self.weblink = weblink
		self.game = game
		self.categoryID = categoryID
		self.category = self.getCategoryName()
		self.players = self.getPlayers(players)
		self.displayPlayers = self.getDisplayPlayers()
		self.variables = list(values)
		self.values = values
		self.displayCategory, self.leaderboardLink, self.leaderboardApi = self.handleVariables()
		self.position = self.getPosition()
		self.displayPosition = self.getDisplayPosition()
		self.playerIcon = self.getPlayerIcon()
		self.time = self.convertTimeFormat(time)
		self.submittedTime = self.convertDateFormat(submittedTime)
		if 'lowcast' in self.displayCategory.lower():
			self.submittedTime

	def convertTimeFormat(self, t: float) -> str:
		hours = int(t/60/60)
		minutes = int(t/60%60)
		seconds = int(t%60)
		milliseconds = round(t%1*1000)
		if 'lowcast' in self.displayCategory.lower():
			return "%d:%02d:%02d (%d casts)" % (minutes, seconds, milliseconds/10, hours)
		elif t > 600:
			return "%d:%02d:%02d" % (hours, minutes, seconds)
		else:
			return "%d:%02d.%03d" % (minutes, seconds, milliseconds) 

	def convertDateFormat(self, date: str) -> datetime:
		return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)
	
	def getCategoryName(self) -> str:
		return apiResponse(BASE_LINK + 'categories/' + self.categoryID)['name']
	
	def getPlayers(self, playersRaw: list) -> list[Player]:
		players = []
		for player in playersRaw:
			players.append(Player(player['rel'], player['uri']))
		
		return players
	
	def getDisplayPlayers(self) -> str:
		displayPlayers = ''
		for count, player in enumerate(self.players):
			if (len(self.players) > 1) and (count == len(self.players) - 1):
				displayPlayers += ' and '
			elif len(self.players) > 1:
				displayPlayers += ', '
			displayPlayers += player.displayName

		return displayPlayers

	def handleVariables(self) -> str:
		displayCategory = self.game.name + '\n'
		displayCategory += self.getCategoryName()
		leadeboardLink = 'https://www.speedrun.com/%s?x=%s' % (self.game.abbreviation, self.categoryID)
		leadeboardApi = BASE_LINK + 'leaderboards/%s/category/%s?' % (self.game.abbreviation, self.categoryID)

		for variable in self.variables:
			valueName = self.getValueName(variable, self.values[variable])
			if len(valueName) > 0:
				displayCategory += ', ' + valueName
				leadeboardLink += '-%s.%s' % (variable, self.values[variable])
				leadeboardApi += 'var-%s=%s&' % (variable, self.values[variable])

		return [displayCategory, leadeboardLink, leadeboardApi]

	def getValueName(self, variable: str, value: str) -> str:
		response = apiResponse(BASE_LINK + 'variables/' + variable)
		if response['is-subcategory']:
			return response['values']['values'][value]['label']
		else:
			return ''
		
	def getPosition(self) -> int:
		leaderboard = apiResponse(self.leaderboardApi)['runs']
		for run in leaderboard:
			if run['run']['id'] == self.id:
				return run['place']
		
		return 0
	
	def getDisplayPosition(self) -> str:
		if self.position == 0:
			return ''
		else:
			return ordinal(self.position) + ' place: '
		
	def getPlayerIcon(self):
		if len(self.players) != 1:
			return None
		picture =  self.players[0].picture
		if picture:
			return picture.replace('userasset', 'static/user')
		return picture



class Game:
	def __init__(self, id: str, platform: str) -> None:
		self.id = id
		self.platform = platform
		apiInfo = apiResponse(BASE_LINK + 'games/' + self.id) 
		self.name = apiInfo['names']['international']
		self.abbreviation = apiInfo['abbreviation']
		self.image = apiInfo['assets']['cover-tiny']['uri'].replace('gameasset', 'static/game')
		self.latestRuns = self.initialLatestRuns()
	
	def getColour(self) -> int:
		colourCoding = {
			'GBA':     0x00FFFF,
			'GBC':     0x00FF00,
			'PC':      0xFF0000,
			'PS1':     0xFFA500,
			'6th':     0xFFFF00,
			'DS':      0x5C5CFF,
			'CE':      0xFF92A5,
			'multi':   0xA020F0,
			'HL':      0x000000,
			'Lego':    0xFFFFFF,
			'fangame': 0xFF1493,
		}

		return colourCoding.get(self.platform, 0x7d7a00)
	
	def initialLatestRuns(self) -> list[Run]:
		initial = []
		latestRunsResponse = apiResponse(BASE_LINK + 'runs?status=verified&orderby=verify-date&direction=desc&game=' + self.id)
		for run in latestRunsResponse:
			initial.append(run['id'])

		return initial

	def handleNewRuns(self) -> list[Run]:
		latestRunsResponse = apiResponse(BASE_LINK + 'runs?status=verified&orderby=verify-date&direction=desc&game=' + self.id)
		newRuns = []
		for run in latestRunsResponse:
			if run['id'] in self.latestRuns:
				break            
			self.latestRuns = [run['id']] + self.latestRuns[:-1]
#			try:
			if run['level'] is None:
				newRun = Run(
					run['id'],
					run['weblink'],
					run['times']['primary_t'],
					run['submitted'],
					self,
					run['category'],
					run['players'],
					run['values']
				)
				newRuns.append(newRun)
#			except KeyError:
#				print(run['id'], 'broke')
		
		return newRuns


def apiResponse(link: str) -> dict:
	sleep(0.6)
	return get(link).json()['data']


def ordinal(n: int) -> str:
	if 11 <= (n % 100) <= 13:
		suffix = 'th'
	else:
		suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
	return str(n) + suffix


def createRunEmbed(run: Run) -> discord.Embed:
	if run.game.platform == 'HL':
		if run.position == 3:
			embedMessage = '<:3rd:1089029027186085990> '
		elif run.position == 2: 
			embedMessage = '<:2nd:1089029014385082378> '
		elif run.position == 1: 
			embedMessage = '<:1st:1089028989441556685> '
		else:
			embedMessage = ''
	else:
		if run.position == 3:
			embedMessage = '<:health3rd:1035612307574751254> '
		elif run.position == 2: 
			embedMessage = '<:health2nd:1035612311412543609> '
		elif run.position == 1: 
			embedMessage = '<:health1st:1035612309571244032> '
		else:
			embedMessage = ''

	embedMessage += '%s [%s](%s) by %s' % (
		run.displayPosition,
		run.time,
		run.weblink,
		run.displayPlayers
	)

	embed = discord.Embed(
		colour = discord.Colour(run.game.getColour()),
		description = embedMessage,
		timestamp = run.submittedTime,
	)

	embed.set_author(
		name = run.displayCategory,
		url = run.leaderboardLink,
		icon_url = run.playerIcon,
	)

	embed.set_thumbnail(url=run.game.image)

	return embed


gamesInit = [
	['nj1nvw6p', 'GBA'],
	['vo6g2n12', 'GBA'],
	['nd2w73d0', 'GBA'],
	['n4d72367', 'GBA'],
	['om1m9k62', 'GBA'],
	['m1mm2j12', 'GBA'],
	['xlde4513', 'GBC'],
	['29d30ydl', 'GBC'],
	['qw6jrxdj', 'PC'],
	['3698v0dl', 'PC'],
	['qw6jqx1j', 'PC'],
	['kyd49x1e', 'PC'],
	['xv1p4m18', 'PC'],
	['m1mx5k62', 'PC'],
	['4pdvor1w', 'PC'],
	['n26877dp', 'PC'],
	['l3dx4g6y', 'PC'],
	['xkdklg6m', 'PS1'],
	['8m1zpm60', 'PS1'],
	['ok6q7odg', '6th'],
	['8nd2l560', '6th'],
	['m9dozm1p', '6th'],
	['y65yg7de', 'DS'],
	['369p90l1', 'DS'],
	['o1yypv1q', 'DS'],
	['3dx2xov1', 'CE'],
	['46wr3831', 'CE'],
	['v1plmp68', 'multi'],
	['9d389v91', 'HL'],
	['nd288rvd', 'Lego'],
	['w6jkx51j', 'Lego'],
	['946w031r', 'Lego'],
	['3dx2keg1', 'Lego'],
	['k6qoom1g', 'Lego'],
	['kdkmzmx1', 'Lego'],
	['k6qwyx06', 'fangame'],
	['nd280wrd', 'fangame'],
	['3dxkejp1', 'fangame'],
	['v1pxvez6', 'fangame'],
	['ldej38l1', 'fangame'],
	['76r3wk46', 'fangame'],
	['kdk5jedm', 'fangame'],
	['kdkmo5q1', 'fangame'],
	['46w38ml1', 'fangame'],
]

print(datetime.utcnow(), 'init')
games = [Game(id, platform) for id, platform in gamesInit]

client = commands.Bot(command_prefix='/', intents=discord.Intents.default(), allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=True))

@client.event
async def on_ready():
	print("Bot Online!")
	print("Name: {}".format(client.user.name))
	print("ID: {}".format(client.user.id))
	handleNewRuns.start()	
		

@tasks.loop(minutes = FREQUENCY_MINUTES)
async def handleNewRuns():
	print(datetime.utcnow(), 'start')
	newRuns = []
	for game in games:
		newRuns += game.handleNewRuns()
	for run in newRuns:
		try:
			runEmbed = createRunEmbed(run)
			if run.game.platform == 'HL':
				await client.get_channel(CHANNEL_ID_HL).send(embed=runEmbed)
			else:
				wrNotification = ''
				if run.position == 1:
					if run.game.platform in ['GBA', 'GBC', 'PC', 'DS', 'multi', '6th', 'PS1']:
						if run.game.platform == 'PC':
							wrNotification += '<@&1060270747756540035> '
						wrNotification += '<@&1060270605057929358> '
					wrNotification += '<@&1142161543367237642>'
				sentMessage = await client.get_channel(CHANNEL_ID_MAIN).send(wrNotification, embed=runEmbed)
				if run.position == 1:
					await sentMessage.add_reaction('<:health1st:1035612309571244032>')
				elif run.position == 2:
					await sentMessage.add_reaction('<:health2nd:1035612311412543609>')
				elif run.position == 3:
					await sentMessage.add_reaction('<:health3rd:1035612307574751254>')
		except Exception as e:
			await client.get_channel(CHANNEL_ID_TEST).send(e)
	print(datetime.utcnow(), 'done')


client.run(DISCORD_TOKEN)
