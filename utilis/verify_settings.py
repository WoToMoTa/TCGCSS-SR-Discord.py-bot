def verifySettings(fileName: str) -> None:
    try:
        settingsFile = open(fileName, 'r')

        import json
        settings = json.load(settingsFile)

        from requests import get
        for seriesID in settings['series']: 
            seriesData = get('https://www.speedrun.com/api/v1/series/'+seriesID).json()
            if 'data' not in seriesData:
                raise SettingsSeriesNotFoundError

        
        for game in settings['games']:
            if not {'colour', 'server', 'emotes', 'wr_ping', 'stream_notif', 'il_mode', 'emote'}.issubset(settings['games'][game]):
                raise SettingsGameMissingParameterError(game)
            
        if 'default' not in settings['games']: raise SettingsDefaultMissingError
        if settings['loop_period'] < 5: raise SettingsLoopTooShortError
        6
        
    except FileNotFoundError:
        raise SettingsNotFoundError
    except json.decoder.JSONDecodeError:
        raise SettingsIncorrectFormatError
    

class SettingsNotFoundError(Exception):
    def __init__(self):
        super().__init__('Settings file not found.')

class SettingsIncorrectFormatError(Exception):
    def __init__(self):
        super().__init__('Settings file has incorrect format.')

class SettingsSeriesNotFoundError(Exception):
    def __init__(self):
        super().__init__('Provided series ID not found.')

class SettingsDefaultMissingError(Exception):
    def __init__(self):
        super().__init__('The settings are missing default parameters.')

class SettingsGameMissingParameterError(Exception):
    def __init__(self, id):
        super().__init__(f'The game ({id}) settings are missing required parameters.')

class SettingsLoopTooShortError(Exception):
    def __init__(self):
        super().__init__('The loop shouldn\'t be shorter than 5 minutes.')
