Visualising football
====================

In this section we look at a variety of ways of analysing event data in football. 
Event data is everything that happens on the ball. It is sometimes supplemented with information,
such as whether a pass is made under pressure, but the focus is very firmly on individual ball 
events: tackles, passes, shots, interceptions etc. 

What we will learn  is how to create useful visualistions of this data. 
Start by watching the video!

VIDEO HERE

### Shot and pass maps




### Passing networks



### Heat maps





### Key Performance Indices (KPI)

It is important for clubs to develop a culture around Key Performance Indices (KPIs). 
These should be set by the coaching staff, working together with data scientists, to find 
an aspects of the game that is measureable and can be communicated in a simple visulaisation. 


Below are a few examples of visualisations of KPIs for Liverpool's last ten games in the Premier League season 2021-22
using the [twelve.football](https://twelve.football) platform. These are measured over 10 matches (the last 10 of the season). 
Usually measurements between six and ten matches gives a reliable idea of form.

#### Expected Goals

The first visualisation is a shot map where and report on expected goals.

<img src="../images/lesson1/Liverpool_shot_map.png" alt="fishy" width="300px" class="bg-primary">
<img src="../images/lesson1/Liverpool_xg_trend.png" alt="fishy" width="300px" class="bg-primary">

We will cover [expected goals](../lesson2/introducingExpectedGoals) in the next section,
but for now you can think of the area of the dots below as measuring the quality of a chance.
Notice that Liverpool mainly shoot from an area in the middle of the penalty area. 
They aim to create high quality chances. Their xG performance on is a
rolling presentation of expected goal differences for the 
last 10 matches. This shows they created better chances than their opponents in 
all but one of their matches (against Manchester City).

#### Entries in to the final third

Again building on expected goals, this visualisation shows the quality of chances Liverpool had when they entered the final third in 
various ways. Notice that balls arriving first on the wings (to Salah and Alexander-Arnold on the right,
and Mane and Robertson on the left) are most dangerous. Centrally, they are less of a risk. Turning to the entries against we see (of course) that their opponents enter 
Liverpool's final third less often, but are slightly more dangerous when attacking on the right.

<img src="../images/lesson1/final_3rd_entries_zones_for.png" alt="fishy" width="300px" class="bg-primary">
<img src="../images/lesson1/final_3rd_entries_zones_against.png" alt="fishy" width="300px" class="bg-primary">

### Transitions

An important part of Liverpool's game is pressing high up the field, regaining the ball and creating chances from this. 
The map on the left shows where they are making these regains and the quality of the chance they generate.
Again, area of the circle is quality of chance and a star indicates a goal. 
Slightly more of these successful regains occur on Liverpool's left wing than on the right. A striking aspect 
is how well they convert regains in their own half in to successful attacks.


Turning to the map on the right, we see that although other teams regain the ball 
from Liverpool while they are attacking, the opposition seldom create danger from these 
regains. It is very difficult to win the ball back from Liverpool in their half of the pitch!

<img src="../images/lesson1/SeasonTransitionForLiverpool.png" alt="fishy" width="300px" class="bg-primary">
<img src="../images/lesson1/SeasonTransitionAgainstLiverpool.png" alt="fishy" width="300px" class="bg-primary">
