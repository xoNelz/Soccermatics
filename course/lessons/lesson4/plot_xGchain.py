# -*- coding: utf-8 -*-
"""
xG chain
===========================
Calculate xG chain
"""
import pandas as pd
import numpy as np
import json
# plotting
import os
import pathlib
import warnings 
from joblib import load
from mplsoccer import Pitch
from itertools import combinations_with_replacement
from sklearn.linear_model import LinearRegression
##############################################################################
# Opening the dataset
# ----------------------------
#
# First we open the data. It is the file created from Possesion Chain segment.

df = pd.DataFrame()
for i in range(11):
    file_name = 'possesion_chains_England' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[0]), 'possesion_chain', file_name)
    with open(path) as f:
        data = json.load(f)
    df = pd.concat([df, pd.DataFrame(data)])
df = df.reset_index()

##############################################################################
# Preparing variables for models
# ----------------------------
#
# For our models we will use all non-linear combinations of the starting and ending
# x coordinate and *c* - distance from the middle of the pitch. First, we filter ones
# where only starting coordinate were saved, then we create separate columns for *x* and *c*
# start and end. We assign value 105 to shot x_1 and 0 for c_1. Then, we create combinations
# with replacement of these variables - to get their non-linear transfomations. As the next step,
# we multiply the columns in the combination and create a model with them. 

#model variables
var = ["x0", "x1", "c0", "c1"]

#combinations
inputs = []
inputs.extend(combinations_with_replacement(var, 1))
inputs.extend(combinations_with_replacement(var, 2))
inputs.extend(combinations_with_replacement(var, 3))

#make new columns
for i in inputs:
    if len(i) > 1:
        column = ''
        x = 1
        for c in i:
            column += c
            x = x*df[c]
        df[column] = x
        var.append(column)

##############################################################################
# Building models
# ----------------------------
#
# Now we can build models. First we create a logistic regression predicting if
# there was a shot in the end of the chain. Then, we build a linear regression 
# xG~model. 

#logistic regression
passes = df.loc[ df["eventName"].isin(["Pass"])]
X = passes[var].values
y = passes["shot_end"].values
path_model = os.path.join(str(pathlib.Path().resolve().parents[0]), 'possesion_chain', 'finalized_model.sav')
model = load(path_model) 
y_pred_proba = model.predict_proba(X)[::,1]

passes["shot_prob"] = y_pred_proba
#OLS
shot_ended = passes.loc[passes["shot_end"] == 1]
X2 = shot_ended[var].values
y2 = shot_ended["xG"].values
lr = LinearRegression()
lr.fit(X2, y2)
y_pred = lr.predict(X2)
shot_ended["xG_pred"] = y_pred
shot_ended["xGchain"] = shot_ended["xG_pred"]*shot_ended["shot_prob"]
##############################################################################
# Calculating xGchain values for events
# ----------------------------
#
# As the next step we calculate the xGchain value for action son the pitch. To do so, we
# multiply probability of the shot with goal probability. 



##############################################################################
# Finding out players with highest xGchain
# ----------------------------
# As the last step we want to find out which players who played more than 400 minutes
# scored the best in possesion-adjusted xGchain per 90. We repeat steps that you already know 
# from `Radar Plots <https://soccermatics.readthedocs.io/en/latest/gallery/lesson3/plot_RadarPlot.html>`_.
# We group them by player, sum, assign merge it with players database to keep players name,
# adjust per possesion and per 90. Only the last step differs, since we stored *percentage_df*
# in a .json file that can be found `here <https://github.com/soccermatics/Soccermatics/tree/main/course/lessons/minutes_played>`_.

summary = shot_ended[["playerId", "xGchain"]].groupby(["playerId"]).sum().reset_index()

path = os.path.join(str(pathlib.Path().resolve().parents[0]),"data", 'Wyscout', 'players.json')
player_df = pd.read_json(path, encoding='unicode-escape')
player_df.rename(columns = {'wyId':'playerId'}, inplace=True)
player_df["role"] = player_df.apply(lambda x: x.role["name"], axis = 1)
to_merge = player_df[['playerId', 'shortName', 'role']]

summary = summary.merge(to_merge, how = "left", on = ["playerId"])


path = os.path.join(str(pathlib.Path().resolve().parents[0]),"minutes_played", 'minutes_played_per_game_England.json')
with open(path) as f:
    minutes_per_game = json.load(f)
#filtering over 400 per game
minutes_per_game = pd.DataFrame(minutes_per_game)
minutes = minutes_per_game.groupby(["playerId"]).minutesPlayed.sum().reset_index()
summary = minutes.merge(summary, how = "left", on = ["playerId"])
summary = summary.fillna(0)
summary = summary.loc[summary["minutesPlayed"] > 400]
#calculating per 90
summary["xGchain_p90"] = summary["xGchain"]*90/summary["minutesPlayed"]




#adjusting for possesion
path = os.path.join(str(pathlib.Path().resolve().parents[0]),"minutes_played", 'player_possesion_England.json')
with open(path) as f:
    percentage_df = json.load(f)
percentage_df = pd.DataFrame(percentage_df)
#merge it
summary = summary.merge(percentage_df, how = "left", on = ["playerId"])

summary["xGchain_adjusted_per_90"] = (summary["xGchain"]/summary["possesion"])*90/summary["minutesPlayed"]
summary[['shortName', 'xGchain_adjusted_per_90']].sort_values(by='xGchain_adjusted_per_90', ascending=False).head(5)

##############################################################################
# Challenge
# ----------------------------
# 1. StatsBomb has recently released a dataset with Indian Superleague 2021/22 games. Calculate
# xGchain values for these player. Note that the possesion chains are already isolated. Which player stood out the most? 

