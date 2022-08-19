"""
Plotting passes
==============

Making a pass map using Statsbomb data
"""

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen

##############################################################################
# Opening the dataset
# ----------------------------
# At first we have to open the data. To do this we use a parser SBopen available in mplsoccer. 
# Using method *event* and putting the id of the game as a parameter we load the data.
# Then, we filter the dataframe so that only passes  are left

parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

##############################################################################
# Making the pass map using iterative solution
# ----------------------------
# Draw the pitch, record that Statsbomb is the default value of Pitch class. Each provider uses different coordinate system.
# Useful links:
    
# * https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_pitches.html

# * https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_compare_pitches.html

# We iterate through the entire dataset. We check if a pass was made by Lucy Bronze
# If so, we take the starting coordinates of a pass and plot a circle. Then we subtract the coordinates beginning of the pass 
# from the end of passes to draw arrows. In the end, we set the title

#drawing pitch
pitch = Pitch(line_color = "black")
fig, ax = pitch.draw(figsize=(10, 7))

for i,thepass in passes.iterrows():
    #if pass made by Lucy Bronze
    if thepass['player_name']=='Lucy Bronze':
        x=thepass['x']
        y=thepass['y']
        #plot circle
        passCircle=plt.Circle((x,y),2,color="blue")      
        passCircle.set_alpha(.2)   
        ax.add_patch(passCircle)
        dx=thepass['end_x']-x
        dy=thepass['end_y']-y
        #plot arrow
        passArrow=plt.Arrow(x,y,dx,dy,width=3,color="blue")
        ax.add_patch(passArrow)

ax.set_title("Lucy Bronze passes against Sweden", fontsize = 24)     
fig.set_size_inches(10, 7)
plt.show()


###

##############################################################################
# Making the pass map using mplsoccer functions
# ----------------------------
# First, we filter out passes made by Lucy Bronze.
# Then, we take only the columns needed to plot passes  - coordinates of start and end of a pass.
# We draw a pitch and using arrows method we plot arrows.
# Using scatter method we draw circles where the pass started
# filter the dataset to completed passes for Lucy Bronze
mask_bronze = (df.type_name == 'Pass') & (df.player_name == "Lucy Bronze")
df_pass = df.loc[mask_bronze, ['x', 'y', 'end_x', 'end_y']]

pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.arrows(df_pass.x, df_pass.y,
            df_pass.end_x, df_pass.end_y, color = "blue", ax=ax['pitch'])
pitch.scatter(df_pass.x, df_pass.y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
fig.suptitle("Lucy Bronze passes against Sweden", fontsize = 30) 
plt.show()
