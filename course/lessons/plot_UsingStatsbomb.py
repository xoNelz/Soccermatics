"""
Using Statsbomb
=====================

Getting familiar with Statsbomb data
"""

#CODE WAITING FOR FILE CONFIRMATION - until then it's a total mess
#importing necessary libraries
import pandas as pd
from mplsoccer import Sbopen
from tabulate import tabulate
#declaring the parser to open the data
parser = Sbopen()
#first open and explore competitions to find the competition we are interested in exploring - we open it using competition method

df_competition = parser.competition()
#explore structure - print out 3 first records and info (if there are more columns)
df_competition.head(3)
#structure (if more columns and not all were shown previously)
df_competition.info()

# the most important information for us is in the *competition_id* (id of competition) and *season_id*
# the first one is id in Statsbomb database of competition, the second one of a season of this competition (for example 
# WC 2018 would have a different *season_id* than WC 2014, but the same *competition_id*)

# now we open the dataframe with matches
# we know (but if you can also open the entire competitions dataframe and check *competition_id*  and *season_id*
# of different leagues) that for Women World Cup *competition_id* is 72 and *season_id* is 30
df_match = parser.match(competition_id=72, season_id=30)
df_match.head(3)
df_match.info()

# from this dataframe for us the most important are *match_id*, *home_team_id* and *home_team_name* and adequately 
# *away_team_id* and *away_team_name* 

# To check the lineups we use the *lineup* method. We do it for England Sweden WWC 2019 game - *game_id* is 69301 
# - you can check that in the df_match. In this dataframe you will find all players who played in this game, their teams 
# and jersey numbers
df_lineup = parser.lineup(69301)
df_lineup.head(3)
df_lineup.info()

# The Statsbomb data that we will use the most during the course is event data. 
# Knowing *game_id* you can open all the events that occured on the pitch
# In the event dataframe you will find events with additional information, we will mostly use this dataframe.
# Tactics dataframe provides information about player position on the pitch. 'Related' dataframe provides information
# on events that were related to each other - for example ball pass and pressure applied. *df_freeze* consists of freezed
# frames with player position in the moment of shots. We will learn more about tracking data later in the course

df_event, df_related, df_freeze, df_tactics = parser.event(69301)

# exploring the data
df_event.head(3)
df_event.info()
df_related.head(3)
df_related.info()
df_freeze.head(3)
df_freeze.info()
df_tactics.head(3)
df_tactics.info()

# Statsbomb offers 360 data which track not only location of an event but also players' location. To open them we need
# an id of freezed frame. In the *df_frame* we find information on players' position (but only if teammate, not all information)
# and in *df_visible* it is provided which part of the pitch was tracked during an event.

df_frame, df_visible = parser.frame(3788741)

# exploring the data
df_frame.info()
df_frame.head(3)
df_visible.info()
df_visible.head(3)

# Before you start 
# ---
# run this lines in Spyder/Jupyter notebook and explore dataframes more to get more familiar before you start working on the course