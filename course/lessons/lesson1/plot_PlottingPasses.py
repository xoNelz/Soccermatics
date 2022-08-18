import matplotlib.pyplot as plt
import numpy as np
from pandas.io.json import json_normalize
from mplsoccer import Pitch
import json

pitchLengthX=120
pitchWidthY=80

from mplsoccer import Pitch, Sbopen

# Load in the data
parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)

passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

# Draw the pitch, record that Statsbomb is the default value of Pitch class. Each provider uses different coordinate system.
# Useful links
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_pitches.html
# https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_compare_pitches.html
pitch = Pitch(line_color = "black")
fig, ax = pitch.draw(figsize=(10, 7))

for i,thepass in passes.iterrows():
    #if thepass['team_name']==away_team_required: #
    if thepass['player_name']=='Lucy Bronze':
        x=thepass['x']
        y=thepass['y']
        passCircle=plt.Circle((x,y),2,color="blue")      
        passCircle.set_alpha(.2)   
        ax.add_patch(passCircle)
        dx=thepass['end_x']-x
        dy=thepass['end_y']-y

        passArrow=plt.Arrow(x,y,dx,dy,width=3,color="blue")
        ax.add_patch(passArrow)

ax.set_title("Lucy Bronze passes against Sweden", fontsize = 20) 
     
fig.set_size_inches(10, 7)
#fig.savefig('Output/shots.pdf', dpi=100) 
plt.show()


###

#Plotting it using mplsoccer

# filter the dataset to completed passes for Lucy Bronze
mask_bronze = (df.type_name == 'Pass') & (df.player_name == "Lucy Bronze")
df_pass = df.loc[mask_bronze, ['x', 'y', 'end_x', 'end_y']]

pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.arrows(df_pass.x, df_pass.y,
            df_pass.end_x, df_pass.end_y, color = "blue", ax=ax['pitch'])
pitch.scatter(df_pass.x, df_pass.y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
#fig.savefig('Output/shots.pdf', dpi=100)
fig.suptitle("Lucy Bronze passes against Sweden", fontsize = 20) 
plt.show()
