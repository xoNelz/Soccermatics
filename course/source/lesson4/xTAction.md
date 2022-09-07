Expected Threat - Action-based
==============================

We now move away from a position-based approach and take an approach based on chains of possession. 
To do this, we first need to look at the idea of a possession chain: a sequence of events 
where the same team has unbroken control of the ball. We then use this possession chain as the 
building block for an expected threat based on actions within that chain.

VIDEO HERE. COMING 19th SEPTEMBER

The logic of focussing on actions in a chain instead of position comes from the fact that
football is a dynamic game: the threat then lies in how the ball is moved, 
rather than where the ball is. A pass does not just have value because of where the ball ends up, 
it also has value on how it shifts the defence. Cross-field balls, which don't move the ball 
forward, should still give positive value. A method which evaluates passses 
should also assign positive value to back passes, since they can be a step 
toward moving the ball forward later on. By looking at the actions within a chain, we can start 
to look at this context. We can also include qualifiers, 
such as whether it was a cross or a through ball. This prevents, for example, us 
overvaluing ‘hopeful’ crosses in to the box. 

Thats the overall philosophy. We now look at how to build this approach.

### Possession chains



xG chain



### Evaluating actions in a chain

Here we see how the model picks up the value Trent Alexander Arnold adds with cross balls. 
He was ranked 3rd in the Premier League per 90 during the last third of the season. 
Mount’s threat (ranked 5th) comes from shorter passes in to the box. 
If you are wondering, Thiago was ranked first in the last part of the season.
We include much more than just the start and end co-ordinates when fitting the model. 
Here are the top xT producers through passing and dribbling per 90 for the whole of last season .

The method we use exploits the power of possession chains. Every sequence 
of play is grouped together based on who had the ball. A chain is broken if the team scores, the ball goes out of play or the opposition touch it two times or more. The video below explains how we use that to measure the value of a pass.

This method, for which Twelve have made player rankings publicly available for over four years now. Although we now keep our online ratings site a bit hidden (because we would like you to download the lovely, colourful app) you can look at them here.
I never really used the term Expected Threat that much, preferring Pass Impact or Pass Value or even Markov Model. But I think its important we use the same terminology, so that we understand each other. So, I am going to follow Tom Worville from the Athletic on this one: from now on I will call this statistic — which (attempts to) measure the probability that an action will lead to a goal, which was invented by Sarah Rudd and can be implemented in a variety of ways (of which some are better than others) — Expected Threat.
And just to prove my commitment here is a Twelve xT for Brentford against Arsenal.

Maybe slightly nicer than, as highlighted by Tom, Oracle systems attempt.
In my next Medium post I will present our professional scouting version of expected threat, which includes tracking data (player positions). Stay tuned!