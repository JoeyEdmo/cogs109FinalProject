import numpy as np
import pandas as pd
import constants as cons

'''
For each game passed in it calcs the stats for that game and returns it. Currently only used for 30 games.
totalData is a list of games in the constants.py format.
'''
def stats30(totalData):
    df = pd.DataFrame(columns=['gameid','avg', 'obp', 'slg', 'runs', 'runsopposing', 'win'])
    for data in totalData:
        tmp = stats(data)
        df = pd.concat(
            [df,tmp],
            ignore_index=True,
            copy=False,
            ) 
    return df


def stats(data):
    '''
    data is an array of values of a game. We want a df with the args from constants.py
    
    we make a df from the 30 games of data
    
    fields in order
    
    ['gameid', 'visiting', 'vscore', 'hscore', 'batter', 'r1', 'r2', 'r3',
                      'lineupspot', 'eventtype', 'eventflag','atbatflag', 'hitvalue','sachit',
                      'sacfly', 'batterresult','r1res','r2res','r3res','endgameflag']
    '''
    
    avg = calcAvg(data)
    obp = calcObp(avg, data)
    slg = calcSlg(data)
    runs = getRuns(data)
    runsOpposingTeam = getOpposingRuns(data)
    win = getWin(data)
    gameID = data[0][0]
    
    df = pd.DataFrame(zip([gameID], [avg],[obp],[slg],[runs],[runsOpposingTeam], [win]), columns=[ 'gameid', 'avg', 'obp', 'slg', 'runs', 'runsopposing', 'win'])
    return df

def calcAvg( data):
    homeGame = not 'v' in data[0][1]
    denom = 0 #total at bat events
    numer = 0 #total hits
    for event in data:
        if(event[cons.STATISTICAL_FIELDS.index('atbatflag')] == 'F'):
            continue
        if(homeGame and event[3] == '0'): #if homegame and visitors batting we dont care
            continue
        if(not homeGame and event[3] == '1'): #if visitor game and home batting we dont care
            continue
        denom += 1
        hitval = int(event[cons.STATISTICAL_FIELDS.index('eventtype')])
        if(hitval < 20):
            continue
        numer += 1
    return numer/denom

def calcSlg(data):
    homeGame = not 'v' in data[0][1]
    denom = 0 #total at bat events
    numer = 0 #total hits
    for event in data:
        if(event[cons.STATISTICAL_FIELDS.index('atbatflag')] == 'F'):
            continue
        if(homeGame and event[3] == '0'): #if homegame and visitors batting we dont care
            continue
        if(not homeGame and event[3] == '1'): #if visitor game and home batting we dont care
            continue
        denom += 1
        hitval = int(event[cons.STATISTICAL_FIELDS.index('eventtype')])
        if(hitval < 20):
            continue
        numer += 1 * int(event[cons.STATISTICAL_FIELDS.index('hitvalue')])
    return numer/denom

def calcObp(avg, data):
    homeGame = not 'v' in data[0][1]
    denom = 0 #total at bat events
    numer = 0 #total hits
    dip = {}
    for event in data:
        if(homeGame and event[3] == '0'): #if homegame and visitors batting we dont care
            continue
        if(not homeGame and event[3] == '1'): #if visitor game and home batting we dont care
            continue
        denom +=1
        hitval = int(event[cons.STATISTICAL_FIELDS.index('eventtype')])
        if(hitval > 13  and hitval <19):
            numer += 1
    return numer/denom + avg

def getRuns(data):
    if(data[len(data)-1][cons.STATISTICAL_FIELDS.index('endgameflag')] != 'T'):
        print('error at eog flag')
        print(data)
        print(data[len(data)-1])
        print(data[len(data)-1][cons.STATISTICAL_FIELDS.index('endgameflag')])
        raise KeyError
    if('v' in data[0][1]):
        return int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('vscore')])
    return int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('hscore')])
    
def getOpposingRuns(data):
    if(data[len(data)-1][cons.STATISTICAL_FIELDS.index('endgameflag')] != 'T'):
        print('error at eog flag')
        print(data)
        raise KeyError
    if('v' in data[0][1]):
        return int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('hscore')])
    return int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('vscore')])

def getWin(data):
    if(data[len(data)-1][cons.STATISTICAL_FIELDS.index('endgameflag')] != 'T'):
        print('error at eog flag')
        print(data)
        raise KeyError
    hscore = int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('hscore')])
    vscore = int(data[len(data)-1][cons.STATISTICAL_FIELDS.index('vscore')])
    if('v' in data[0][1]):

        return int((vscore > hscore)) #if visiting we win if visitor score > home score. If not opposite.
    return int((vscore < hscore))
