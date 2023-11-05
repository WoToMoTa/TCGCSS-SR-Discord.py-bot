CHANNEL_ID_TEST = 1029384953189896322
CHANNEL_ID_MAIN = 597203792055894016
CHANNEL_ID_HL = 1064229439627604119

POSITION_EMOTES_PC = {
    1: '<:health1st:1035612309571244032>',
    2: '<:health2nd:1035612311412543609>',
    3: '<:health3rd:1035612307574751254>',
}

POSITION_EMOTES_HL = {
    1: '<:1st:1089028989441556685>',
    2: '<:2nd:1089029014385082378>',
    3: '<:3rd:1089029027186085990>',
}

PING_ROLE = {
    'PC_WR': '<@&1060270747756540035>',
    'FS_WR': '<@&1060270605057929358>',
    'WR'   : '<@&1142161543367237642>',
}

COLOUR_CODING = {
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

GROUP_SETTINGS = {
    'GBA': {
        'colour': COLOUR_CODING['GBA'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'GBC': {
        'colour': COLOUR_CODING['GBC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'PC': {
        'colour': COLOUR_CODING['PC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['PC_WR'], PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'PS1': {
        'colour': COLOUR_CODING['PS1'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    '6th': {
        'colour': COLOUR_CODING['6th'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'DS': {
        'colour': COLOUR_CODING['DS'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'CE': {
        'colour': COLOUR_CODING['CE'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['WR']],
        },
    'multi': {
        'colour': COLOUR_CODING['multi'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        },
    'HL': {
        'colour': COLOUR_CODING['HL'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [],
        },
    'Lego': {
        'colour': COLOUR_CODING['Lego'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['WR']],
        },
    'fangame': {
        'colour': COLOUR_CODING['fangame'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['WR']],
        },
    'QWC_PC': {
        'colour': COLOUR_CODING['PC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['PC_WR'], PING_ROLE['WR']],
        },
    'QWC_GBA': {
        'colour': COLOUR_CODING['GBA'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['WR']],
        },
    'default': {
        'colour': 0x000000,
        'server': CHANNEL_ID_TEST,
        'emotes': {},
        'wr_ping': [],
    }
}

"""
Each game should have colour, server ID, emote, and wr ping role set.
Required parameters:
· colour:  int
· server:  int
· emotes:  dict[int, str]
· wr_ping: list[str]
"""
GAME_SETTINGS = {
	'nj1nvw6p': GROUP_SETTINGS['GBA'],
    'vo6g2n12': GROUP_SETTINGS['GBA'],
    'nd2w73d0': GROUP_SETTINGS['GBA'],
    'n4d72367': GROUP_SETTINGS['GBA'],
    'om1m9k62': GROUP_SETTINGS['GBA'],
    'm1mm2j12': GROUP_SETTINGS['QWC_GBA'],
    'xlde4513': GROUP_SETTINGS['GBC'],
    '29d30ydl': GROUP_SETTINGS['GBC'],
    'qw6jrxdj': GROUP_SETTINGS['PC'],
    '3698v0dl': GROUP_SETTINGS['PC'],
    'qw6jqx1j': GROUP_SETTINGS['PC'],
    'kyd49x1e': GROUP_SETTINGS['PC'],
    'xv1p4m18': GROUP_SETTINGS['PC'],
    'm1mx5k62': GROUP_SETTINGS['PC'],
    '4pdvor1w': GROUP_SETTINGS['PC'],
    'n26877dp': GROUP_SETTINGS['PC'],
    'l3dx4g6y': GROUP_SETTINGS['QWC_PC'],
    'xkdklg6m': GROUP_SETTINGS['PS1'],
    '8m1zpm60': GROUP_SETTINGS['PS1'],
    'ok6q7odg': GROUP_SETTINGS['PS1'],
    '8nd2l560': GROUP_SETTINGS['PS1'],
    'm9dozm1p': GROUP_SETTINGS['PS1'],
    'y65yg7de': GROUP_SETTINGS['PS1'],
    '369p90l1': GROUP_SETTINGS['PS1'],
    'o1yypv1q': GROUP_SETTINGS['PS1'],
    '3dx2xov1': GROUP_SETTINGS['CE'],
    '46wr3831': GROUP_SETTINGS['CE'],
    'v1plmp68': GROUP_SETTINGS['multi'],
    '9d389v91': GROUP_SETTINGS['HL'],
    'j1lqeej6': GROUP_SETTINGS['HL'],
    'nd288rvd': GROUP_SETTINGS['Lego'],
    'w6jkx51j': GROUP_SETTINGS['Lego'],
    '946w031r': GROUP_SETTINGS['Lego'],
    '3dx2keg1': GROUP_SETTINGS['Lego'],
    'k6qoom1g': GROUP_SETTINGS['Lego'],
    'kdkmzmx1': GROUP_SETTINGS['Lego'],
    'k6qwyx06': GROUP_SETTINGS['fangame'],
    'nd280wrd': GROUP_SETTINGS['fangame'],
    '3dxkejp1': GROUP_SETTINGS['fangame'],
    'v1pxvez6': GROUP_SETTINGS['fangame'],
    'ldej38l1': GROUP_SETTINGS['fangame'],
    '76r3wk46': GROUP_SETTINGS['fangame'],
    'kdk5jedm': GROUP_SETTINGS['fangame'],
    'kdkmo5q1': GROUP_SETTINGS['fangame'],
    '46w38ml1': GROUP_SETTINGS['fangame'],
    'o6gkk2n1': GROUP_SETTINGS['fangame'],
    'default' : GROUP_SETTINGS['default'],
}

"""
Determines how the bot handles the IL runs.
0 - Ignore IL runs
1 - Disable pings for ILs
2 - Display normally
"""
IL_MODE = 1


"""
Main Discord loop frequency, in minutes per action. Anything below 10 min not recommended due to caching
"""
FREQUENCY_MINUTES = 5


"""
List the IDs of series the bot is supposed to follow.
"""
SERIES_ID = ['15ndxp7r', 'v7odlz9n']
