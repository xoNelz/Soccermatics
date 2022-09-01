"""
Points Moving Average
=====================
Investigate Points Moving Average
"""


import datetime 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#downloading data and saving it in pandas dataframe for all seasons
dflist=[]
seasonst = []
#taking to last year because United hasn't played yet for the day of code develop
for year in range(5,22,1):
    if year<9:
        yeartext='0'+str(year)+'0'+str(year+1)
        yeartext2='0'+str(year)+'-0'+str(year+1)
    elif year==9:
        yeartext='0910'
        yeartext2='09-10'
    else:
        yeartext=str(year)+str(year+1)
        yeartext2=str(year)+'-'+str(year+1)
    #For England
    performance_year = pd.read_csv("https://www.football-data.co.uk/mmz4281/"+yeartext+"/E0.csv",delimiter=',') 
    seasonst.append(yeartext2)
    dflist.append(performance_year)

performance = pd.concat(dflist).reset_index()

#get all the teams
teams = performance["AwayTeam"].unique()
teams = teams[~pd.isnull(teams)]

team_dfs = dict()
for team in teams:
    team_df = pd.DataFrame(columns = ["Points", "Date", "Game"])
    matches = performance.loc[(performance['AwayTeam']==team) | (performance['HomeTeam']==team)]
    game = 0
    for i, match in matches.iterrows():
        game +=1
        date = match["Date"]
        if match['AwayTeam'] == team:
            goalsfor = match['FTAG']
            goalsagainst = match['FTHG']
            if match['FTR'] == 'A':
                points = 3
            elif match['FTR'] == 'D':
                points = 1
            else:
                points = 0
        if match['HomeTeam'] == team:
            goalsfor = match['FTHG']
            goalsagainst = match['FTAG']
            if match['FTR'] == 'H':
                points = 3
            elif match['FTR'] == 'D':
                points = 1      
            else:
                points = 0
    
        team_df.at[i, "Points"] = points
        team_df.at[i, "Date"] = date
        team_df.at[i, "Game"] = game
        
    team_df['PointsRA'] = team_df['Points'].rolling(window=30, win_type='triang').mean()
    team_dfs[team] = team_df


fig,ax=plt.subplots(figsize=(20, 15))
fig.set_facecolor("darkgrey")
ax
big_6 = ['Man City', 'Liverpool', 'Arsenal', 'Chelsea', 'Tottenham', 'Man United']
#arsenal got yellow because of those 2004 jerseys 
colors = ['lightblue', 'red', 'yellow', 'darkblue', 'lightgrey', 'darkred']

for club, color in zip(big_6, colors):
    ax.plot(team_dfs[club]['Game'],  team_dfs[club]['PointsRA'], linewidth=3, linestyle='-',color=color, alpha = 0.4)

ax.set_title(str(10) + ' game moving average')
plt.gcf().autofmt_xdate()

ax.legend(big_6)



ax.set_xticks(np.arange(0, max(team_dfs["Liverpool"]['Game']) ,38))
ax.set_xticklabels(seasonst)
ax.set_xlim(0,max(team_dfs["Liverpool"]['Game'])+40)
ax.set_ylim(0,3.2)


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



ax.set_ylabel('Rolling Average Points Per Game')
ax.set_xlabel('Season')
fig.show()