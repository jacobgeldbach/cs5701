# Task: Implement learning decision tree algorithm using python to guide a robot on whether it needs to ask a human for help.

# Information: Information gain theory calculation will need to be used in order to choose which attribute to use as the root of the tree and which attribute to use next until the tree is complete. Based on which attribute gives the most amount of information gained. The Inforamtion calculation theory: I(p(v1) ... p(vn)) = E-p(vi)log2(p(vi)

# Context: The problem is for a robot to decide whether to ask for help in a given 
situation: "yes" means ask for help, "no" means don't ask for help, i.e. the
robot makes its own decision.
The attributes are all binary, they are:

Familiar situation - the robot has the seen this situation before.
In a hurry - whether the robot's mission time critical, which relates to whether it has time to request assistance.
Long delay - is there a long delay in getting help when its requested.
Safe situation - is the current situation generally safe.
Confident - is the robot confident it knows the right decision.
Safety critical decision - does the decision effect a critical safety feature.
Asked before - has the robot asked for help before in a similar situation.

Data and learning: There are 100 examples.  To train the decision tree you should use the information-based approach we went over in class, arranging the tree by the options that supply the most information. I will provide the data file later it is in .csv format with each row a run and each column a 1 or 0 for that columns attribute.
