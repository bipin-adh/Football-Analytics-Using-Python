#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:34:46 2020

Data is used from Statsbomb (competitions , events , matches):¶

1. competitions - eg : UCL , worldcup , etc
2. matches - take in competition id and see the matches of the required competition.
3. events - take match id and visualize and analyze all the detailed events of every min (passes, shots,build up play,etc)

@author: bpn8adh
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from FCPython import createPitch

BASE_DIR = 'statsbomb-data/open-data/data'

# Load the competition file .
with open(BASE_DIR +'/competitions.json') as f:
    competitions = json.load(f)
    
competitions_df = pd.read_json(BASE_DIR + '/competitions.json')

ucl_df = competitions_df[competitions_df['competition_name'] == 'Champions League'].head()

# UEFA Champions League 2018/2019 has competition ID = 16
competition_id = 16

# Load spurs vs liverpool json file from the list of final matches(json) of Champions League. 
matches = pd.read_json(BASE_DIR+'/matches/'+
                      str(competition_id)+'/4.json')

# Champions league final id : Spurs vs Liverpool
match_id = matches['match_id'][0]

"""

Start Match Analysis:¶
Importing FcPython code for pitch drawing.
length = 120 yards ,
 width = 80 yards 
 (Statsbomb data default pitch unit is in yards. While metrica sports is in metres.)

"""

# Size of the pitch in yards.
pitchLengthX = 120
pitchWidthY = 80

# Load in all match events data.
spursVsLfc_match = str(match_id)+'.json' 


events_df = pd.read_json(BASE_DIR+'/events/'+spursVsLfc_match)

"""
Function for type of play: goal, pass,etc
"""
def get_shot_type(type_dict):
    return type_dict.get('name')

# unpacking type column dictionary for knowing type of play.
events_df['shot_type'] = events_df['type'].apply(get_shot_type)

# events_df.iloc[33]['shot_type']

total_shots_df = events_df[events_df['shot_type'] == 'Shot']
# All shots in first half of the game. period = 1 .. 2nd half means period = 2
first_half_shots = total_shots_df[total_shots_df['period'] == 1]
shot_details_1st_df = pd.DataFrame(first_half_shots['location'])
shot_details_1st_df['shot_details'] = pd.DataFrame(first_half_shots['shot'])

def get_shot_end_location(shot_details_dict):
    return shot_details_dict.get('end_location')

def get_shot_outcome(shot_details_dict):
    return shot_details_dict.get('outcome')
    
def get_shot_type(shot_details_dict):
    return shot_details_dict.get('type')


shot_details_1st_df['end_location'] = shot_details_1st_df['shot_details'].apply(get_shot_end_location)

shot_details_1st_df['outcome'] = shot_details_1st_df['shot_details'].apply(get_shot_outcome)

shot_details_1st_df['type'] = shot_details_1st_df['shot_details'].apply(get_shot_type)

"""
Colors for shot type:
goal : red
saved : green
blocked : yellow
"""

#Draw the pitch

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','white')

fig.patch.set_facecolor('#006400')
fig.patch.set_alpha(0.7)
# Plot the shot
circleSize = 2

home_team_required = "Liverpool"
away_team_required = "Tottenham Hotspur"

for i,row in shot_details_1st_df.iterrows():
    x = row['location'][0] # shot location x-axis
    y = row['location'][1]  # shot location y-axis
    
    shotCircle = plt.Circle((x,y),circleSize,color = "red")
    shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)
    
    dx = row['end_location'][0] - x # 120
    dy = row['end_location'][1] - y # 42.5
    
    if row['outcome'].get('name') == 'Goal' :
        passArrow = plt.arrow(x, y, dx, dy, width = 0.5 ,color = "red")
    elif row['outcome'].get('name') == 'Saved':
        passArrow = plt.arrow(x, y, dx, dy, width = 0.5 ,color = "green")
    elif row['outcome'].get('name') == 'Blocked':
        passArrow = plt.arrow(x, y, dx, dy, width = 0.5 ,color = "yellow")
    else:
        passArrow = plt.arrow(x, y, dx, dy, width = 0.5 ,color = "blue")
    
    ax.add_patch(passArrow)        
        

fig.set_size_inches(10, 7)
# savefig('figname.png', facecolor=fig.get_facecolor(), transparent=True)
fig.savefig('Output/spursvslfc_ucl_final_1sthalf_goal.pdf',facecolor='#006400',dpi=100) 
plt.show()










