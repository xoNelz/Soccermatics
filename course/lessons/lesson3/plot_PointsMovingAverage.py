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
for year in range(5,23,1):
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
        
    team_df['PointsRA'] = team_df['Points'].rolling(window=10, win_type='triang').mean()
    team_dfs[team] = team_df


fig,ax=plt.subplots()
big_6 = ['Man City', 'Liverpool', 'Arsenal', ]
comparison1='Man City'
comp_color1='lightblue'
comparison3='Liverpool'
comp_color3='red'
comparison2='Man United'
comp_color2='darkred'


ax.plot(team_dfs[comparison1]['Game'],  team_dfs[comparison1]['PointsRA'], linewidth=2, linestyle='-',color=comp_color1)
ax.plot(team_dfs[comparison2]['Game'],  team_dfs[comparison2]['PointsRA'], linewidth=2 , linestyle='-',color=comp_color2)
ax.plot(team_dfs[comparison3]['Game'],  team_dfs[comparison3]['PointsRA'], linewidth=2 , linestyle='-',color=comp_color3)

ax.set_title(str(10) + ' game moving average')
plt.gcf().autofmt_xdate()

ax.legend([comparison1,comparison2,comparison3])

ax.set_ylim(1,3.2)

ax.set_xticks(np.arange(0,max(team_dfs[comparison2]['Game']),38))
ax.set_xticklabels(seasonst)
ax.set_xlim(0,max(team_dfs[comparison2]['Game'])+40)
ax.set_ylim(0,3.2)


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



ax.set_ylabel('Rolling Average Points Per Game')
ax.set_xlabel('Season')
fig.show()