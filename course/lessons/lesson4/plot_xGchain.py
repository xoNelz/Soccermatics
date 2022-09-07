# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:12:00 2022

@author: aleks
"""
#TODO
#1) Logistic regression for shot in the end probability
#2) Implement xG
#3) OLS xG~coordinates.

#chain - either one team two contacts or ball out of play 
#importing necessary libraries 
import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
#opening data
import os
import pathlib
import warnings 
#used for plots
from mplsoccer import Pitch
from scipy.stats import binned_statistic_2d

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

df = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[0]), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    df = pd.concat([df, pd.DataFrame(data)])

see = df.iloc[:1000]
next_event = see.shift(-1, fill_value=0)
see["nextEvent"] = next_event["subEventName"]

see["kickedOut"] = see.apply(lambda x: 1 if x.nextEvent == "Ball out of the field" else 0, axis = 1)
#interruptions out
interruption = see.loc[see["eventName"] == "Interruption"]
#probably need to drop "others on the ball event" - nope
# filter out non-accurate duels - in wyscout they are 2 way - attacking and defending
lost_duels = see.loc[see["eventName"] == "Duel"].loc[see.apply (lambda x:{'id':1802} in x.tags, axis = 1)]
see = see.drop(lost_duels.index)
# filter ball out of the field - I can get this anyways
out_of_ball = see.loc[see["subEventName"] == "Ball out of the field"]
see = see.drop(out_of_ball.index)

# save attempts can be dropped
goalies = see.loc[see["subEventName"].isin(["Goalkeeper leaving line", "Save attempt", "Reflexes"])]
see = see.drop(goalies.index)                                           
# treat Touch like pass but unintended
# well, treat others on the ball like passes
# drop offsides 
# treat free kicks like passes
see["nextTeamId"] = see.shift(-1, fill_value=0)["teamId"]
#potential +0s
chain_team = see.iloc[0]["teamId"]
period = see.iloc[0]["matchPeriod"]
stop_criterion = 0
chain = 0
see["possesion_chain"] = 0


#napisać waruneczek na zmienianie się chain teamu i będzie banglało 
for i, row in see.iterrows():
    
    if row["eventName"] == "Pass" or row["eventName"] == "Duel" :
        if row["teamId"] == chain_team and {"id": 1802} in row["tags"]:
                stop_criterion += 1
        if row["teamId"] != chain_team and {"id": 1801} in row["tags"]:
                stop_criterion += 1    
    if row["eventName"] in ["Shot", "Foul", "Offside"]:
            stop_criterion += 2
    if row["kickedOut"] == 1:
            stop_criterion += 2
    #tu musi wlecieć next match period 
    if row["matchPeriod"] != period:
            stop_criterion += 2
            period = row["matchPeriod"] 
            
    
    if stop_criterion >= 2:
        chain += 1
        stop_criterion = 0
        chain_team = row['nextTeamId']
    see.at[i, "possesion_chain"] = chain
    print(chain)

see2 = see[["subEventName", "tags", "teamId", "possesion_chain", "matchPeriod", 'nextTeamId']]
# won duel by the same team
# pass by the same team
# lost duel by the other team

# jeli hand pass po evencie to +2
# +2 działa 
# z podaniami jakis problem 
# jesli niecelne podanie +1, jesli rywal zrobi cokolwiek potem +1
# jesli rywal wygra pojedynek +1, jesli zrobi cokolwiek po tym +1
#  lepiej ustawić zapisywanie chaina
#no trzeba na tych next teamach podziałać
# wez kartke, jeszcze raz see2 sobie ogarnij i jedź case gdzie chainy nie działają przez +1ki 


















#potential +1s
# other team wins duel/neutral duel - mamy to 
# inaccurate pass
# pass by the other team 

# potential +2s
# ball out of the field - unsuccessful pass with one of the .nan coordinates 
# shot 
# faul by the same team as over possesion chain
# foul by another team
# offside
#if inaccurate pass + pass by other team -> start counting possesion by the pass by other team. 
#chain = 0, sprawdzamy wszystkie warunki eventu - ify, jeli którys spelnia to dodajemy k=k+1
# najpierw dochodzi do dwóch, dodajemy +1 do chaina, df.at[i, chain] = chain
#dodatkowa zmienna was previous accurate -> zabezpieczenie eventu po wybiciu piłki!!!
