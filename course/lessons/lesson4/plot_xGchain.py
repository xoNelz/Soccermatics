# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:12:00 2022

@author: aleks
"""
#TODO
#1) Logistic regression for shot in the end probability
#2) Implement xG
#3) OLS xG~coordinates.

#chain - either one team two contacts or ball out of play 
#importing necessary libraries 
import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
#opening data
import os
import pathlib
import warnings 
#used for plots
from mplsoccer import Pitch
from scipy.stats import binned_statistic_2d

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

df = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[0]), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    df = pd.concat([df, pd.DataFrame(data)])

see = df.iloc[:1000]