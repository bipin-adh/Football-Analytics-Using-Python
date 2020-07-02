#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:56:48 2020

 Data is used from Statsbomb (competitions , events , matches):

* competitions - eg : UCL , worldcup , etc
* matches - take in competition id and see the matches of the required competition.
* events - take match id and visualize and analyze all the detailed events of every min (passes, shots,build up play,etc)

@author: Bipin Adhikari ( @bpn8adh )
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the competition file .
with open('/home/bpn8adh/My-Football-Analytics-Python/statsbomb-data/open-data/data/competitions.json') as f:
    competitions = json.load(f)

# Convert into a dataframe for table look.
competitions_df = pd.read_json('/home/bpn8adh/My-Football-Analytics-Python/statsbomb-data/open-data/data/competitions.json')

# competitions_df[competitions_df['competition_name'] == 'Champions League']

# UEFA Champions League 2018/2019 has competition ID = 16
competition_id = 16

# Load Spurs vs liverpool match json file from the list of matches(json) of Champions League finals. 

matches = pd.read_json('/home/bpn8adh/My-Football-Analytics-Python/statsbomb-data/open-data/data/matches/'+
                      str(competition_id)+'/4.json')

# Champions league final id : Spurs vs Liverpool
match_id = matches['match_id'][0]

"""
Drawing the Pitch:
    
    Import FcPython code .
    length = 120 yards
    width = 80 yards
     (Statsbomb data default pitch unit is in yards. While metrica sports is in metres.)
"""

# Size of the pitch in yards.
pitchLengthX = 120
pitchWidthY = 80

home_team_required = "Liverpool"
away_team_required = "Tottenham Hotspur"

# Load in all match events data.
spursVsLfc_final = str(match_id)+'.json' 
events_df = pd.read_json('/home/bpn8adh/My-Football-Analytics-Python/statsbomb-data/open-data/data/events/'+spursVsLfc_final)


