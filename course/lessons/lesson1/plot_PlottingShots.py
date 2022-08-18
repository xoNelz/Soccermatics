""""
Hello
"""
#Make a shot map and a pass map using Statsbomb data
#Set match id in match_id_required.

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen, VerticalPitch


#ID for England vs Sweden Womens World Cup
match_id_required = 69301
home_team_required ="England Women's"
away_team_required ="Sweden Women's"

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
file_name=str(match_id_required)+'.json'

#Load in all match events 
parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
    

# Draw the pitch, record that Statsbomb is the default value of Pitch class. Each provider uses different coordinate system.
# Useful links
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_pitches.html
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_compare_pitches.html

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

pitch = Pitch(line_color = "black")
fig, ax = pitch.draw(figsize=(10, 7))


#Plot the shots by looping through them.
for i,shot in shots.iterrows():
    x=shot['x']
    y=shot['y']
    
    goal=shot['outcome_name']=='Goal'
    team_name=shot['team_name']
    
    circleSize=2
    #circleSize=np.sqrt(shot['shot_statsbomb_xg'])*12

    if (team_name==home_team_required):
        if goal:
            shotCircle=plt.Circle((x,y),circleSize,color="red")
            plt.text(x+1,y-2,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue") 
            plt.text(pitchLengthX-x+1,pitchWidthY - y -2 ,shot['player_name']) 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)


fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 20)     
fig.set_size_inches(10, 7)
#fig.savefig('Output/shots.pdf', dpi=100) 
plt.show()

#Plotting it without looping through rows and using Statsbomb parser
#Reading Statsbomb data using the parser - 69301 is the id of the game in the database
# Record that Statsbomb is the default value of Pitch class 'pitch_type' variable. Each provider uses different coordinate system.
# Useful links
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_pitches.html
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_compare_pitches.html

#create pitch - let's explore more options using mplsoccer than black and white pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

#make a query to get a dataframe with England shots
team1, team2 = df.team_name.unique()
#query
mask_england = (df.type_name == 'Shot') & (df.team_name == team1)
#finding rows in the df and keeping only necessary columns
df_england = df.loc[mask_england, ['x', 'y', 'outcome_name', "player_name"]]

#plot them - if shot ended with Goal - alpha 1 and add name
#for England
for i, row in df_england.iterrows():
    if row["outcome_name"] == 'Goal':
       pitch.scatter(row.x, row.y, alpha = 1, s = 500, color = "red", ax=ax['pitch']) 
       pitch.annotate(row["player_name"], (row.x + 1, row.y - 2), ax=ax['pitch'], fontsize = 12)
    else: 
       pitch.scatter(row.x, row.y, alpha = 0.2, s = 500, color = "red", ax=ax['pitch']) 
       
mask_sweden = (df.type_name == 'Shot') & (df.team_name == team2)
df_sweden = df.loc[mask_sweden, ['x', 'y', 'outcome_name', "player_name"]]   

#for sweden we need to revert coordinates
for i, row in df_sweden.iterrows():
    if row["outcome_name"] == 'Goal':
       pitch.scatter(120 - row.x, 80 - row.y, alpha = 1, s = 500, color = "blue", ax=ax['pitch']) 
       pitch.annotate(row["player_name"], (120 - row.x + 1, 80 - row.y - 2), ax=ax['pitch'], fontsize = 12)
    else: 
       pitch.scatter(120 - row.x, 80 - row.y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch']) 
       
fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 20)           
#fig.savefig('Output/shots.pdf', dpi=100)
plt.show()




#Note that using pitch.scatter we could have plotted all shots using one line, however, since name of a player and alpha differs if goal was scored, it was more convenient to loop through a small loop.
#Showing it using VerticalPitch for England, half = True plots only one half of the pitch, nice option if you are plotting shots
pitch = VerticalPitch(line_color='black', half = True)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#plotting all shots
pitch.scatter(df_england.x, df_england.y, alpha = 1, s = 500, color = "red", ax=ax['pitch'], edgecolors="black") 
fig.suptitle("England shots against Sweden", fontsize = 20)           
#fig.savefig('Output/shots.pdf', dpi=100)
plt.show()

#Exercise:

#1, Create a dataframe of passes which contains all the passes in the match
#2, Plot the start point of every Sweden pass. Attacking left to right.
#3, Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
#4, Plot arrows to show where the passes we

