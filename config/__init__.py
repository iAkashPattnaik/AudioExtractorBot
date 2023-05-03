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

telegramChannel - telegram.dog/PhantomProjects
initialRelease - 21/06/21
relaunchDate - 3/5/23
"""

# Inbuilt
from os import environ

class Config(object):
    botToken: str = environ.get("botToken") # type: ignore
    apiId: str = environ.get("apiId") # type: ignore
    apiHash: str = environ.get("apiHash") # type: ignore
