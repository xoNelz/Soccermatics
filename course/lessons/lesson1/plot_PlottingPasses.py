""""
# TO DO ALEKSANDER: DO A PLOT THE SHOTS VERSION USING 'QUERY' INSTEAD
# ALSO USE MPL SOCCER INSTEAD OF CURRENT VERSION.
# ALSO, CHECK THIS IS RIGHT DIRECTIONS. I THINK I GOT SOME THINGS WRONG.
"""

#Find the passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

#Draw the pitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thepass in passes.iterrows():
    #if thepass['team_name']==away_team_required: #
    if thepass['player_name']=='Lucy Bronze':
        x=thepass['location'][0]
        y=thepass['location'][1]
        passCircle=plt.Circle((x,pitchWidthY-y),2,color="blue")      
        passCircle.set_alpha(.2)   
        ax.add_patch(passCircle)
        dx=thepass['pass_end_location'][0]-x
        dy=thepass['pass_end_location'][1]-y

        passArrow=plt.Arrow(x,pitchWidthY-y,dx,-dy,width=3,color="blue")
        ax.add_patch(passArrow)

fig.set_size_inches(10, 7)
fig.savefig('Output/passes.pdf', dpi=100) 
plt.show()
