CHANNEL_ID_TEST = 1029384953189896322
CHANNEL_ID_MAIN = 597203792055894016
CHANNEL_ID_HL = 1064229439627604119
CHANNEL_ID_HL_STREAM = 1072152126781915167
CHANNEL_ID_STREAM = 365236143815655434
CHANNEL_ID_LEGO_TEST = 1215705818129899520  

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

GAME_ICON_EMOTE = {
    'hp1': '<:HP1:1024667981294354432>',
    'hp2': '<:HP2:1024667976487678023>',
    'hp3': '<:HP3:1024667984620429413>',
    'hp4': '<:HP4:1024667978115055626>',
    'hp5': '<:HP5:1024667986579177502>',
    'hp6': '<:HP6:1024667980115738634>',
    'hp7': '<:HP7:1024667983370530846>',
    'hp8': '<:HP8:1024667975531372714>',
    'qwc': '<:QWC:1024727842170359890>',
    'lego': '<:HPLego:1024263615513116702>',
    'hl': '<:Legacy:1064269545130434640>',
    'fan': '<:PS1modding:1071105913735360512>',
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

GROUP_SETTINGS_PB = {
    'GBA': {
        'colour': COLOUR_CODING['GBA'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'GBC': {
        'colour': COLOUR_CODING['GBC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'PC': {
        'colour': COLOUR_CODING['PC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['PC_WR'], PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'PS1': {
        'colour': COLOUR_CODING['PS1'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    '6th': {
        'colour': COLOUR_CODING['6th'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'DS': {
        'colour': COLOUR_CODING['DS'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'CE': {
        'colour': COLOUR_CODING['CE'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'multi': {
        'colour': COLOUR_CODING['multi'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['FS_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'HL': {
        'colour': COLOUR_CODING['HL'],
        'server': CHANNEL_ID_HL,
        'emotes': POSITION_EMOTES_HL,
        'wr_ping': [],
        'stream_notif': [],
        'il_mode': 1,
        },
    'Lego': {
        'colour': COLOUR_CODING['Lego'],
        'server': CHANNEL_ID_LEGO_TEST,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [],
        'stream_notif': [CHANNEL_ID_LEGO_TEST],
        'il_mode': 0,
        },
    'fangame': {
        'colour': COLOUR_CODING['fangame'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [],
        'stream_notif': [],
        'il_mode': 1,
        },
    'QWC_PC': {
        'colour': COLOUR_CODING['PC'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['PC_WR'], PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'QWC_GBA': {
        'colour': COLOUR_CODING['GBA'],
        'server': CHANNEL_ID_MAIN,
        'emotes': POSITION_EMOTES_PC,
        'wr_ping': [PING_ROLE['WR']],
        'stream_notif': [CHANNEL_ID_STREAM],
        'il_mode': 1,
        },
    'default': {
        'colour': 0x000000,
        'server': CHANNEL_ID_TEST,
        'emotes': {},
        'wr_ping': [],
        'stream_notif': [],
        'il_mode': 0,
    }
}

GROUP_SETTINGS_STREAM = {
    'hp1': {
        'emote': GAME_ICON_EMOTE['hp1'],
        'display_name': 'Harry Potter and the Philosopher\'s Stone',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp2': {
        'emote': GAME_ICON_EMOTE['hp2'],
        'display_name': 'Harry Potter and the Chamber of Secrets',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp3': {
        'emote': GAME_ICON_EMOTE['hp3'],
        'display_name': 'Harry Potter and the Prisoner of Azkaban',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp4': {
        'emote': GAME_ICON_EMOTE['hp4'],
        'display_name': 'Harry Potter and the Goblet of Fire',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp5': {
        'emote': GAME_ICON_EMOTE['hp5'],
        'display_name': 'Harry Potter and the Order of the Phoenix',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp6': {
        'emote': GAME_ICON_EMOTE['hp6'],
        'display_name': 'Harry Potter and the Half-Blood Prince',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp7': {
        'emote': GAME_ICON_EMOTE['hp7'],
        'display_name': 'Harry Potter and the Deathly Hallows: Part 1',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'hp8': {
        'emote': GAME_ICON_EMOTE['hp8'],
        'display_name': 'Harry Potter and the Deathly Hallows: Part 2',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'qwc': {
        'emote': GAME_ICON_EMOTE['qwc'],
        'display_name': 'Quidditch World Cup',
        'stream_notif': [CHANNEL_ID_STREAM],
    },
    'lego': {
        'emote': GAME_ICON_EMOTE['lego'],
        'stream_notif': [CHANNEL_ID_LEGO_TEST],
    },
    'hl': {
        'emote': GAME_ICON_EMOTE['hl'],
        'stream_notif': [CHANNEL_ID_HL_STREAM],
    },
    'fan': {
        'emote': GAME_ICON_EMOTE['fan'],
        'stream_notif': [],
    },
    'default': {
        'emote': '',
        'stream_notif': [],
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
	'nj1nvw6p': {**GROUP_SETTINGS_PB['GBA'], **GROUP_SETTINGS_STREAM['hp2']},
    'vo6g2n12': {**GROUP_SETTINGS_PB['GBA'], **GROUP_SETTINGS_STREAM['hp4']},
    'nd2w73d0': {**GROUP_SETTINGS_PB['GBA'], **GROUP_SETTINGS_STREAM['hp5']},
    'n4d72367': {**GROUP_SETTINGS_PB['GBA'], **GROUP_SETTINGS_STREAM['hp1']},
    'om1m9k62': {**GROUP_SETTINGS_PB['GBA'], **GROUP_SETTINGS_STREAM['hp3']},
    'm1mm2j12': {**GROUP_SETTINGS_PB['QWC_GBA'], **GROUP_SETTINGS_STREAM['qwc']},
    'xlde4513': {**GROUP_SETTINGS_PB['GBC'], **GROUP_SETTINGS_STREAM['hp2']},
    '29d30ydl': {**GROUP_SETTINGS_PB['GBC'], **GROUP_SETTINGS_STREAM['hp1']},
    'qw6jrxdj': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp2']},
    '3698v0dl': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp7']},
    'qw6jqx1j': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp8']},
    'kyd49x1e': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp4']},
    'xv1p4m18': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp6']},
    'm1mx5k62': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp5']},
    '4pdvor1w': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp1']},
    'n26877dp': {**GROUP_SETTINGS_PB['PC'], **GROUP_SETTINGS_STREAM['hp3']},
    'l3dx4g6y': {**GROUP_SETTINGS_PB['QWC_PC'], **GROUP_SETTINGS_STREAM['qwc']},
    'xkdklg6m': {**GROUP_SETTINGS_PB['PS1'], **GROUP_SETTINGS_STREAM['hp2']},
    '8m1zpm60': {**GROUP_SETTINGS_PB['PS1'], **GROUP_SETTINGS_STREAM['hp1']},
    'ok6q7odg': {**GROUP_SETTINGS_PB['6th'], **GROUP_SETTINGS_STREAM['hp2']},
    'pd0n7o21': {**GROUP_SETTINGS_PB['6th'], **GROUP_SETTINGS_STREAM['hp2']},
    '8nd2l560': {**GROUP_SETTINGS_PB['6th'], **GROUP_SETTINGS_STREAM['hp1']},
    'm9dozm1p': {**GROUP_SETTINGS_PB['6th'], **GROUP_SETTINGS_STREAM['hp3']},
    'y65yg7de': {**GROUP_SETTINGS_PB['DS'], **GROUP_SETTINGS_STREAM['hp7']},
    '369p90l1': {**GROUP_SETTINGS_PB['DS'], **GROUP_SETTINGS_STREAM['hp8']},
    'o1yypv1q': {**GROUP_SETTINGS_PB['DS'], **GROUP_SETTINGS_STREAM['hp6']},
    '3dx2xov1': {**GROUP_SETTINGS_PB['CE'], **GROUP_SETTINGS_STREAM['default']},
    '46wr3831': {**GROUP_SETTINGS_PB['CE'], **GROUP_SETTINGS_STREAM['default']},
    'v1plmp68': {**GROUP_SETTINGS_PB['multi'], **GROUP_SETTINGS_STREAM['default']},
    '9d389v91': {**GROUP_SETTINGS_PB['HL'], **GROUP_SETTINGS_STREAM['hl']},
    'j1lqeej6': {**GROUP_SETTINGS_PB['HL'], **GROUP_SETTINGS_STREAM['hl']},
    'nd288rvd': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    'w6jkx51j': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    '946w031r': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    '3dx2keg1': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    'k6qoom1g': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    'kdkmzmx1': {**GROUP_SETTINGS_PB['Lego'], **GROUP_SETTINGS_STREAM['lego']},
    'k6qwyx06': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'nd280wrd': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    '3dxkejp1': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'v1pxvez6': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'ldej38l1': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    '76r3wk46': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'kdk5jedm': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'kdkmo5q1': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    '46w38ml1': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'o6gkk2n1': {**GROUP_SETTINGS_PB['fangame'], **GROUP_SETTINGS_STREAM['fan']},
    'default' : {**GROUP_SETTINGS_PB['default'], **GROUP_SETTINGS_STREAM['default']},
}

"""
Determines how the bot handles the IL runs.
0 - Ignore IL runs
1 - Disable pings for ILs
2 - Display normally
"""


"""
Main Discord loop frequency, in minutes per action. 
"""
FREQUENCY_MINUTES = 5


"""
List the IDs of series the bot is supposed to follow.
"""
SERIES_ID = ['15ndxp7r', 'v7odlz9n']

SETTINGS = {
    'loop_period': FREQUENCY_MINUTES,
    'series': SERIES_ID,
    'games': GAME_SETTINGS,
}

if __name__ == '__main__':
    import json
    with open('settings.json', 'w') as settingsFile:
        json.dump(SETTINGS, settingsFile)
