from statistics import median
from requests import get
from math import log, sqrt
from datetime import datetime
import gspread
import asyncio
import tracemalloc
from time import time


tracemalloc.start()

class Game:
    def __init__(self, id, name, abbreviation, segregation):
        self.id = id
        self.name = name 
        self.abbreviation = abbreviation
        self.segregation = segregation
        self.categories = []
        self.runs = []
        self.runners = []

    def __str__(self):
        return self.name

    def getGameWeight(self):
        if len(self.runs) == 0:
            return 0
        #self.cleanCategories()
        return log(len(self.runners), 10) * 100 #/ sqrt(len(self.categories))

    def cleanCategories(self):
        for category in self.categories:
            if len(category.runs) == 0:
                self.categories.remove(category)



class Category:
    def __init__(self, id, name, variables, game: Game):
        self.id = id
        self.name = name 
        self.variables = variables
        self.game = game
        self.runs = []
        self.runners = []

    def __str__(self):
        return self.name

    def getCatWeight(self):
        if len(self.runs) == 0:
            return 0
        runTimes = []
        for run in self.runs:
            runTimes.append(run.time)
        med = median(runTimes)
        if 'Lowcast' in self.name:
            med /= 30
        return log(med, 3600) * self.game.getGameWeight()
    
    def printPP(self):
        print(self.name, ': ', self.getCatWeight())


class Run:
    def __init__(self, id, runners, time, position, category: Category):
        self.id = id
        self.runners = runners 
        self.time = time      
        self.position = position
        self.category = category 
        self.game = self.category.game
        self.game.runs.append(self)
        self.category.runs.append(self)
        for runner in self.runners:
            runner.runs.append(self)

    def __str__(self):
        return self.name
      
    def getRunWeight(self):
        if self.category.getCatWeight() == 0 or self.position == 0:
            return 0
        return sqrt(len(self.category.runs)/(self.position + len(self.category.runs)*0.05)) * self.category.getCatWeight()



class Runner:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.runs = []
        self.score = 0
        self.multiplier = 0.9

    def __str__(self):
        return self.name

    def totalPP(self):
        self.sortRunsByPP()
        total = 0
        multi = 1
        uniqueCoops = []
        for run in self.runs:
            if len(run.runners) > 1:
                if run.category in uniqueCoops:
                    self.runs.remove(run)
                    continue
                uniqueCoops.append(run.category)
            total += run.getRunWeight() * multi
            multi *= self.multiplier
        return total

    def printPP(self):
        for run in self.runs:
            print(run.category.name, end=': ')
            print(run.getRunWeight())
    
    def sortRunsByPP(self):
        runsDict = []
        runsDictSort = {}
        for run in self.runs:
            runsDictSort[run] = run.getRunWeight()
        runsDictSort = sorted(runsDictSort.items(), key=lambda x: x[1], reverse=True)
        for run in runsDictSort:
            runsDict.append(run[0])
        self.runs = list(runsDict)

    def generateLinesCSV(self, position):
        line1 = '%d|%s|%d|%d' % (position, self.name, len(self.runs), int(self.totalPP()))
        line2 = '|||'
        weigth = 1
        for run in self.runs:
            score = run.getRunWeight()
            line1 += '|%s||' % (run.category.name)
            line2 += '|%.2f|%.4f|%.2f' % (score, weigth, score * weigth)   
            weigth *= self.multiplier
        line1 += '\n'
        line2 += '\n'
        return line1, line2
    
    def generateLinesGSpread(self, position):
        line1 = [position, self.name, len(self.runs), int(self.totalPP())]
        line2 = [''] * 4
        weigth = 1
        for run in self.runs:
            score = run.getRunWeight()
            line1 += [run.category.name, '', '']
            line2 += [f'{score:.2f}', f'{(weigth*100):.2f}%', f'{(score * weigth):.2f}']
            weigth *= self.multiplier
        while len(line1) < 157:
            line1 += ['']
        while len(line2) < 157:
            line2 += ['']
        return line1[0:157], line2[0:157]


async def updateSheet(worksheet: gspread.Worksheet, segregation: int):
    gameSegregationCodes = {
        'nj1nvw6p' : 1,         # 0 for all games
        'xlde4513' : 1,         # 1 for FS games
        'qw6jrxdj' : 2,         # 2 for PC 
        'xkdklg6m' : 1,
        'ok6q7odg' : 1,
        '3698v0dl' : 2,
        'y65yg7de' : 1,
        'qw6jqx1j' : 2,
        '369p90l1' : 1,
        'kyd49x1e' : 2,
        'vo6g2n12' : 1,
        'xv1p4m18' : 2,
        'o1yypv1q' : 1,
        'm1mx5k62' : 2,
        'nd2w73d0' : 1,
        'n4d72367' : 1,
        '29d30ydl' : 1,
        '4pdvor1w' : 2,
        '8m1zpm60' : 1,
        '8nd2l560' : 1,
        'om1m9k62' : 1,
        'n26877dp' : 2,
        'm9dozm1p' : 1,
        '3dx2xov1' : 2,
        'v1plmp68' : 2,
        'l3dx4g6y' : 0,
        'm1mm2j12' : 0,
        '9d389v91' : 0,
        'nd288rvd' : 0,
        'w6jkx51j' : 0,
        'kdk5jedm' : 0,
        '946w031r' : 0,
        '3dx2keg1' : 0,
        'k6qoom1g' : 0,
        'kdkmzmx1' : 0,
    }

    series = 'harrypotter'     #harrypotter harry_the_hamster
    games = {}
    players = {}
    

    getSeries = get('https://www.speedrun.com/api/v1/series/%s/games?_bulk=yes' % (series)).json()['data']
    #getSeries = [get('https://www.speedrun.com/api/v1/games/hpmulti').json()['data']]

    for game in getSeries:
        gameName = game['names']['international']
        gameID = game['id']
        if gameSegregationCodes.get(gameID, 0) < segregation:
            continue
        games[gameID] = Game(gameID, gameName, game['abbreviation'], gameSegregationCodes.get(gameID, 0))
        getCategories = get('https://www.speedrun.com/api/v1/games/%s/categories' % (gameID)).json()['data']
        await asyncio.sleep(0.6)
        for category in getCategories:
            if category['type'] == 'per-level':
                continue

            catName = gameName + ' ' + category['name']
            catID = category['id']
            getVariables = get('https://www.speedrun.com/api/v1/categories/%s/variables' % (catID)).json()['data']
            await asyncio.sleep(0.6)
            if len(getVariables) > 0:
                variables = []
                values = []
                valuesNames = []
                indexes = []
                for variable in getVariables:
                    varID = variable['id']
                    valuesNamesElement = []
                    if variable['is-subcategory']:
                        variables.append(varID)
                        values.append(list(variable['values']['values']))  
                        for value in variable['values']['values']:
                            valuesNamesElement.append(variable['values']['values'][value]['label'])  
                        valuesNames.append(valuesNamesElement[:])
                        indexes.append(0)
                
                runVars = True
                while runVars:
                    varDict = {}
                    catName = gameName + ' ' + category['name']
                    for i in range(len(indexes)):
                        catName = catName + ', ' + valuesNames[i][indexes[i]]
                        varDict[variables[i]] = values[i][indexes[i]]
                    try:
                        indexes[0] += 1
                        for index in range(len(indexes)):
                            if indexes[index] == len(values[index]):
                                indexes[index] = 0
                                indexes[index+1] += 1
                    except IndexError:
                        runVars = False
                    if (segregation == 2 and (
                            (gameID == 'v1plmp68' and not ('PC' in catName or 'Full Series' in catName)) or
                            (gameID == '3dx2xov1' and not ('PC' in catName or 'Single Year' in catName or 'Custom Map' in catName))
                        )):
                        continue
                    games[gameID].categories.append(Category(catID, catName, varDict, games[gameID]))
                    #print(catName)
                    #print(varDict)
            
            else:
                #print(catName)
                games[gameID].categories.append(Category(catID, catName, {}, games[gameID]))
        
        for category in games[gameID].categories:
            getLeaderboardAPI = 'https://www.speedrun.com/api/v1/leaderboards/%s/category/%s?' % (gameID, category.id)
            for var in category.variables:
                getLeaderboardAPI +=  "var-%s=%s&" % (var, category.variables[var])
            getLeaderboard = get(getLeaderboardAPI).json()['data']['runs']
            await asyncio.sleep(0.6)
            for runOnBoard in getLeaderboard:
                runRunners = []
                for runner in runOnBoard['run']['players']:
                    if runner['rel'] == 'user':
                        runnerID = runner['id']
                        if runnerID not in players:
                            runnerName = get(runner['uri']).json()['data']['names']['international']
                            await asyncio.sleep(0.6)
                            players[runnerID] = Runner(runnerID, runnerName)
                        if players[runnerID] not in games[gameID].runners:
                            category.game.runners.append(players[runnerID])
                        if players[runnerID] not in category.runners:
                            category.runners.append(players[runnerID])
                        runRunners.append(players[runnerID])
                Run(runOnBoard['run']['id'], runRunners, runOnBoard['run']['times']['primary_t'], runOnBoard['place'], category)


    allRunners = {}
    for player in players:
        allRunners[players[player].id] = players[player].totalPP()
    allRunners = sorted(allRunners.items(), key=lambda x: x[1], reverse=True)

    newData = []
    for i, player in enumerate(allRunners):
        runner = players[player[0]]
        newLine1, newLine2 = runner.generateLinesGSpread(i+1)
        newData += [newLine1, newLine2]

    start_row = 3
    end_row = len(newData)+3
    start_column = 1
    end_column = 157

    start_cell = gspread.utils.rowcol_to_a1(start_row, start_column)
    end_cell = gspread.utils.rowcol_to_a1(end_row, end_column)
    range_to_update = f'{start_cell}:{end_cell}'

    print(range_to_update)

    worksheet.update(range_to_update, newData)


async def updateRanking():
    serviceAccount = gspread.service_account(filename='hp-ranking-creds.json')
    sheet = serviceAccount.open('Harry Potter Speedrun ranking')
    
    await updateSheet(sheet.worksheet('Ranking PC only'), 2)
    await updateSheet(sheet.worksheet('Ranking FS games'), 1)
    await updateSheet(sheet.worksheet('Ranking'), 0)

    explanationSheet = sheet.worksheet('Explanation')
    currentTime = datetime.now().strftime('%d %b %Y, %H:%M')
    explanationSheet.update('A23', currentTime)

    
if __name__ == '__main__':  
    start = time()
    asyncio.run(updateRanking())
    print(time()-start)