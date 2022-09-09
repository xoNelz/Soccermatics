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
import statsmodels.api as sm
import statsmodels.formula.api as smf


pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

df = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[0]), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    df = pd.concat([df, pd.DataFrame(data)])
df = df.reset_index()
next_event = df.shift(-1, fill_value=0)
df["nextEvent"] = next_event["subEventName"]

df["kickedOut"] = df.apply(lambda x: 1 if x.nextEvent == "Ball out of the field" else 0, axis = 1)
#interruptions out
interruption = df.loc[df["eventName"] == "Interruption"]
#probably need to drop "others on the ball event" - nope
# filter out non-accurate duels - in wyscout they are 2 way - attacking and defending
lost_duels = df.loc[df["eventName"] == "Duel"]
lost_duels = lost_duels.loc[lost_duels.apply (lambda x:{'id':1802} in x.tags, axis = 1)]
df = df.drop(lost_duels.index)
# filter ball out of the field - I can get this anyways
out_of_ball = df.loc[df["subEventName"] == "Ball out of the field"]
df = df.drop(out_of_ball.index)
# save attempts can be dropped
goalies = df.loc[df["subEventName"].isin(["Goalkeeper leaving line", "Save attempt", "Reflexes"])]
df = df.drop(goalies.index)                                           
# treat Touch like pass but unintended
# well, treat others on the ball like passes
# drop offsides 
# treat free kicks like passes
df["nextTeamId"] = df.shift(-1, fill_value=0)["teamId"]
#potential +0s
chain_team = df.iloc[0]["teamId"]
period = df.iloc[0]["matchPeriod"]
stop_criterion = 0
chain = 0
df["possesion_chain"] = 0
df["possesion_chain_team"] = 0

for i, row in df.iterrows():
    df.at[i, "possesion_chain"] = chain
    df.at[i, "possesion_chain_team"] = chain_team
    
    if row["eventName"] == "Pass" or row["eventName"] == "Duel":
        if row["teamId"] == chain_team and {"id": 1802} in row["tags"]:
                stop_criterion += 1
        if row["teamId"] != chain_team and {"id": 1801} in row["tags"]:
                stop_criterion += 1    
    if row["eventName"] == "Others on the ball":
           if row["teamId"] == row["nextTeamId"]:
               stop_criterion += 2
               
    if row["eventName"] in ["Shot", "Foul", "Offside"]:
            stop_criterion += 2
    if row["kickedOut"] == 1:
            stop_criterion += 2
    #tu musi wlecieć next match period 
    if row["matchPeriod"] != period:
            chain += 1
            stop_criterion = 0
            chain_team = row['teamId']
            period = row["matchPeriod"] 
            df.at[i, "possesion_chain"] = chain
            df.at[i, "possesion_chain_team"] = chain_team
    
    if stop_criterion >= 2:
        chain += 1
        stop_criterion = 0
        chain_team = row['nextTeamId']
    

df["xG"] = 0 
def calulatexG(df):
    """
    Parameters
    ----------
    df : dataframe
        dataframe with Wyscout event data.
    npxG : boolean
        True if xG should not include penalties, False elsewhere.

    Returns
    -------
    xG_sum: dataframe
        dataframe with sum of Expected Goals for players during the season.

    """
    #very basic xG model based on 
    shots = df.loc[df["eventName"] == "Shot"].copy()
    shots["X"] = shots.positions.apply(lambda cell: (100 - cell[0]['x']) * 105/100)
    shots["Y"] = shots.positions.apply(lambda cell: cell[0]['y'] * 68/100)
    shots["C"] = shots.positions.apply(lambda cell: abs(cell[0]['y'] - 50) * 68/100)
    #calculate distance and angle 
    shots["Distance"] = np.sqrt(shots["X"]**2 + shots["C"]**2)
    shots["Angle"] = np.where(np.arctan(7.32 * shots["X"] / (shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)) > 0, np.arctan(7.32 * shots["X"] /(shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)), np.arctan(7.32 * shots["X"] /(shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)) + np.pi)
    #if you ever encounter problems (like you have seen that model treats 0 as 1 and 1 as 0) while modelling - change the dependant variable to object 
    shots["Goal"] = shots.tags.apply(lambda x: 1 if {'id':101} in x else 0).astype(object)
        #headers have id = 403
    headers = shots.loc[shots.apply (lambda x:{'id':403} in x.tags, axis = 1)]
    non_headers = shots.drop(headers.index)
    
    headers_model = smf.glm(formula="Goal ~ Distance + Angle" , data=headers, 
                               family=sm.families.Binomial()).fit()
    #non-headers
    nonheaders_model = smf.glm(formula="Goal ~ Distance + Angle" , data=non_headers, 
                               family=sm.families.Binomial()).fit()
    #assigning xG
    #headers
    b_head = headers_model.params
    xG = 1/(1+np.exp(b_head[0]+b_head[1]*headers['Distance'] + b_head[2]*headers['Angle'])) 
    headers = headers.assign(xG = xG)
    for index, row in headers.iterrows():
        df.at[index, "xG"] = row["xG"]
    #non-headers 
    b_nhead = nonheaders_model.params
    xG = 1/(1+np.exp(b_nhead[0]+b_nhead[1]*non_headers['Distance'] + b_nhead[2]*non_headers['Angle'])) 
    non_headers = non_headers.assign(xG = xG)
    for index, row in non_headers.iterrows():
        df.at[index, "xG"] = row["xG"]

    penalties = df.loc[df["subEventName"] == "Penalty"]
    #treating penalties like shots 
    penalties["X"] = 11
    #calculate distance and angle 
    penalties["Distance"] = 11
    penalties["Angle"] = np.arctan(7.32 * 11 /(11**2 - (7.32/2)**2))
    #if you ever encounter problems (like you have seen that model treats 0 as 1 and 1 as 0) while modelling - change the dependant variable to object 
    penalties["Goal"] = penalties.tags.apply(lambda x: 1 if {'id':101} in x else 0).astype(object)
    penalties = penalties.assign(xG = xG)
    for index, row in penalties.iterrows():
        df.at[index, "xG"] = row["xG"]
    return df
        
df = calulatexG(df)
df["shot_end"] = 0
no_chains = max(df["possesion_chain"].unique())
indicies = []
for i in range(no_chains+1):
    possesion_chain_df = df.loc[df["possesion_chain"] == i]
    if len(possesion_chain_df) > 0:
        if possesion_chain_df.iloc[-1]["eventName"] == "Shot":        
            df.loc[df["possesion_chain"] == i, "shot_end"] = 1
            xG = possesion_chain_df.iloc[-1]["xG"]
            df.loc[df["possesion_chain"] == i, "xG"] = xG
        team_indicies = possesion_chain_df.loc[possesion_chain_df["teamId"] == possesion_chain_df.teamId.mode().iloc[0]].index.values.tolist()
        indicies.extend(team_indicies)    

df = df.loc[indicies]
df = df.loc[df.apply(lambda x: len(x.positions) == 2, axis = 1)]            
df["x0"] = df.positions.apply(lambda cell: (cell[0]['x']) * 105/100)
df["c0"] = df.positions.apply(lambda cell: abs(50 - cell[0]['y']) * 68/100)
df["x1"] = df.positions.apply(lambda cell: (cell[1]['x']) * 105/100)
df["c1"] = df.positions.apply(lambda cell: abs(50 - cell[1]['y']) * 68/100)

df.loc[df["eventName"] == "Shot", "x1"] = 105
df.loc[df["eventName"] == "Shot", "c1"] = 0

var = ["x0", "x1", "c0", "c1"]

from itertools import combinations_with_replacement
inputs = []
inputs.extend(combinations_with_replacement(var, 1))
inputs.extend(combinations_with_replacement(var, 2))
inputs.extend(combinations_with_replacement(var, 3))


for i in inputs:
    if len(i) > 1:
        column = ''
        x = 1
        for c in i:
            column += c
            x = x*df[c]
        df[column] = x
        var.append(column)
model = ''
for v in var[:-1]:
    model = model  + v + ' + '
model = model + var[-1]


df["shot_end"] = df["shot_end"].astype(object)

shot_model = smf.glm(formula="shot_end ~ " + model, data=df,
                           family=sm.families.Binomial()).fit()
print(shot_model.summary())
b_log = shot_model.params

#evalueate
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import roc_curve, roc_auc_score
#logmodel = LogisticRegression()
#X = df[['x','y','end_x','end_y']].values
#y = df["shot_end"].values
#logmodel.fit(X, y)
#predictions = logmodel.predict(X)
#y_score = logmodel.fit(X_train, y_train).decision_function(X_test)
#model_probs = logmodel.predict_proba(X)
#y_score = model_probs[:, 1]
#fpr, tpr, _ = roc_curve(y, y_score)
#auc = roc_auc_score(y, y_score)

#plt.plot(fpr, tpr, marker='.', label= 'ROC curve (area = %0.2f)' % auc)
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.legend(loc='lower right')
shot_ended = df.loc[((df["shot_end"] == 1) & df["eventName"].isin(["Shot", "Pass"])) | (df["subEventName"] == "Penalty")]
goal_model = smf.ols(formula='xG ~ ' + model, data=shot_ended).fit()
print(goal_model.summary())
b_lin = goal_model.params


def calculate_xGChain(sh):
    bsum = b_log[0]
    for i,v in enumerate(var):
        bsum = bsum+b_log[i+1]*sh[v]
    p_shot = 1/(1+np.exp(bsum))
   
    bsum=b_lin[0]
    for i,v in enumerate(var):
       bsum=bsum+b_lin[i+1]*sh[v]
    p_goal = bsum
    return p_shot*p_goal

xGchain = shot_ended.apply(calculate_xGChain, axis=1)
shot_ended = shot_ended.assign(xGchain=xGchain)

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











