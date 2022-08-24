"""
Using Wyscout 
=====================

Getting familiar with Wyscout data
"""
#CODE WAITING FOR FILE CONFIRMATION - until then it's a total mess
#importing necessary libraries

# If you are trying it locally, comment  ..... active lines (put # in front lines path = ...) and comment out (delete #)
#commented out lines
import pathlib
import os
import pandas as pd
import json


# Competitions dataframe 
# In this dataframe you will find information about the id of a competition and available competitions 
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'competitions.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'Wyscout', 'competitions.json') # delete #

with open(path) as f:
    data = json.load(f)
df_competitions = pd.DataFrame(data)
df_competitions.head(3)
df_competitions.info()

# Matches dataframe 
# In this dataframe you can find information about all games that were played in Premier League 2017/18 season.
#*wyId* is the unique id in the Wyscout database. 
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'matches_England.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'matches_England.json') # delete #
with open(path) as f:
    data = json.load(f)
df_matches = pd.DataFrame(data)
df_matches.head(3)
df_matches.info()

#Players dataframe
# In this dataframe you can find information about all players available for Wyscout public dataset. *wyId* is 
# the player id in the Wyscout database. In the *currentTeamId* you can find the id of a team that the player plays form.
#*shortName* is an important column for vizualisations and rankings since player's name is written in a shorter way.
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'players.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'players.json')  
with open(path) as f:
    data = json.load(f)
df_players = pd.DataFrame(data)
df_players.head(3)
df_players.info()

#Events dataframe
# In this dataframe you can find information about all events that occured in all the games during 2017/18 Premier League
# season. *matchId* matches the wyId from *df_matches*, *playerId* matches *wyId* from *df_players*.*tags* provide information on additional characteristics of an event, for example
# if the pass was accurate. The location on the pass can be found in *positions*, but remeber, that the data are collected
# on 100x100 square with reverted y-axis. In the *eventName* you will find the basic name of an event, whereas *subEventName*
# provide more information. *eventSec* is the time of an event.
# 
# If you want to learn more about Wyscout data, you can explore 
# `WyScout API <https://apidocs.wyscout.com/>`_, but remember to switch the version to 2.0 at the top of the page.
# 
#
# This code is adjusted to the webpage with file size limit. If you want to open the data that is stored in the working
# directory, comment (put '#') before the following code and comment out the lines below them (delete '#').

df_events = pd.DataFrame() # put # in front if used locally
for i in range(13): # put # in front if used locally
    file_name = 'events_England_' + str(i+1) + '.json' # put # in front if used locally
    path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', file_name) # put # in front if used locally
    with open(path) as f: # put # in front if used locally
        data = json.load(f) # put # in front if used locally
    df_events = pd.concat([df_events, pd.DataFrame(data)]) # put # in front if used locally


#path = os.path.join(str(pathlib.Path().resolve()), 'Wyscout', 'events_England_.json') # delete #
#with open(path) as f: # delete #
    #data = json.load(f) # delete #
#df_events = pd.DataFrame(data) # delete #

df_events.head(3)
df_events.info()