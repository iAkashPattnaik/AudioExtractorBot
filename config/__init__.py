r"""
    _                _  _        
   / \    _   _   __| |(_)  ___
  / _ \  | | | | / _` || | / _ \
 / ___ \ | |_| || (_| || || (_) |
/_/   \_\ \__,_| \__,_||_| \___/
     _____        _                       _
    | ____|__  __| |_  _ __   __ _   ___ | |_   ___   _ __
    |  _|  \ \/ /| __|| '__| / _` | / __|| __| / _ \ | '__|
    | |___  >  < | |_ | |   | (_| || (__ | |_ | (_) || |
    |_____|/_/\_\ \__||_|    \__,_| \___| \__| \___/ |_|
                 ____          _
                | __ )   ___  | |_
                |  _ \  / _ \ | __|
                | |_) || (_) || |_
                |____/  \___/  \__|

telegramChannel - t.me/IndianBots
initialRelease - 21/06/21
"""

# Inbuilt
from os import environ

class Config(object):
    botToken: str = environ.get("botToken")
    apiId: str = environ.get("apiId")
    apiHash: str = environ.get("apiHash")
