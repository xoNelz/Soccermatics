#importing necessary libraries 
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

#1
parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)
passes = df.loc[df["type_name"] == "Pass"].loc[df['sub_type_name'] != 'Throw-in'].set_index('id')

#2
#keep only Sweden passes
sweden_passes = passes.loc[passes["team_name"] == "Sweden Women's"]
#plot pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#scatter passes
pitch.scatter(sweden_passes.x, sweden_passes.y, alpha = 0.2, s = 100, color = 'yellow', edgecolor = 'blue', ax = ax["pitch"])
#set title
ax['title'].text(0.5, 0.5, 'Sweden passes against England', ha='center', va='center', fontsize=30)
plt.show()

#3
#filter passes by C. Seger 
seger_passes = passes.loc[passes["player_name"] == "Sara Caroline Seger"]
#plot pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#scatter
pitch.scatter(seger_passes.x, seger_passes.y, alpha = 0.2, s = 500, color = 'yellow', edgecolor = 'blue', ax = ax["pitch"])
#set title
ax['title'].text(0.5, 0.5, 'Caroline Seger passes against England', ha='center', va='center', fontsize=30)
plt.show()

#4 - to do it you can just add line in the code above, repeating steps for educational purposes
#plot pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#scatter
pitch.scatter(seger_passes.x, seger_passes.y, alpha = 0.2, s = 500, color = 'yellow', edgecolor = 'blue', ax = ax["pitch"])
#plot arrows
pitch.arrows(seger_passes.x, seger_passes.y,
            seger_passes.end_x, seger_passes.end_y, color = "yellow", ax=ax["pitch"], width=3)

#set title
ax['title'].text(0.5, 0.5, 'Caroline Seger passes against England', ha='center', va='center', fontsize=30)
plt.show()
