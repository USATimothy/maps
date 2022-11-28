#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on 26 Feb 2021

@author: Timothy Fleck

This python script takes two files and merges them into a third file.
File 1 is a .csv file containing 2020 presidential election returns for each state.
File 2 is a geojson file containing geographic data for each state.
The third file (the output) is a javascript file containing all the data from file 2,
plus the two-way vote share (Democrat vote / (D+R vote) ) for each state.
"""
import pandas
import numpy
import json

#Import the election returns and calculate two-way vote share
def str2num(s):
    s1=str(s)
    s2=s1.replace(",","")
    try:
        return int(s2)
    except:
        return numpy.nan

votes=pandas.read_csv('Popular vote backend.csv')

#dem_votes=pandas.Series(map(str2num,votes['dem_votes']))
#rep_votes=pandas.Series(map(str2num,votes['rep_votes']))
votes['two-way share']=votes['dem_votes']/(votes['dem_votes']+votes['rep_votes'])

votes.set_index('state',inplace=True)

#Import the geojson data
stategeojson=open('state_densities.js')
stategeodata=stategeojson.read()
first_brace=stategeodata.index("{")
prologue=stategeodata[:first_brace]
stateJSON=stategeodata[first_brace:-2]
stategeojson.close()

JSONdict=json.loads(stateJSON)

for feature in JSONdict["features"]:
    state = feature["properties"]["name"]
    try:
        share2=votes.loc[state,"two-way share"]
        feature["properties"]["voteshare"]=share2
    except:
        pass
JSONnew=json.dumps(JSONdict)
statevotes=prologue + JSONnew + ";"

votesjs=open('state_voteshares.js','w')
votesjs.write(statevotes)
