import datetime
import os
import stats

def getGameDeltas(ourGameID, theirGameID, allGamesDict):
    h = getTeam30DayNums(ourGameID, allGamesDict) #our data, or 'home' data 
    v = getTeam30DayNums(theirGameID, allGamesDict) #their data, or 'visitor' data
    if(type(h) == int or type(v) == int):
        return -1
    deltaavg = h['avg'].mean()- v['avg'].mean() #get diff of averages of averages for last 30
    deltaobp = h['obp'].mean()- v['obp'].mean() 
    deltaslg = h['slg'].mean()- v['slg'].mean()
    deltaruns = h['runs'].mean()- v['runs'].mean()
    deltarunsopposing = h['runsopposing'].mean()- v['runsopposing'].mean()
    deltawins = h['win'].mean()- v['win'].mean()
    gameResult = stats.getWin(allGamesDict[ourGameID])
    return [deltaavg,deltaobp,deltaslg,deltaruns, deltarunsopposing, deltawins, gameResult]


def getTeam30DayNums(GameID, allGamesDict):
    '''
    will take a game ID and the dict and return the stats for the last 30 games in pandas.
    stats will be mean avg, mean obp, mean homers/hits, mean slugger, mean runs/hits, mean runs allowed
    '''
    team = GameID[:3]
    year = GameID[3:7]
    month = GameID[7:9]
    day = GameID[9:11]
    num = GameID[11:] #double headers
    
    #build start time
    date = datetime.date(int(year), int(month), int(day))
    # delta time, we increment per day backwards
    delta = datetime.timedelta(days=1)
    # iterate until 30 games
    count = 0
    timeSearched = 0
    totalData = []
    while (count <= 30):
        date -= delta
        year = date.year
        month = date.month
        day = date.day
        if(month<10): #keep lengths the same, 0 pad <10 nums. same for days
            month = '0' + str(month)
        else:
            month = str(month)
        if(day<10):
            day = '0' + str(day)
        else:
            day = str(day)
        curID = team + str(year) + month + str(day) + '0' #rn ignoring double headers
        data = search(curID, allGamesDict)
        if(timeSearched > 3000):
            return -1
        if(data == -1):
            timeSearched += 1
            continue
        totalData.append(data)
        count += 1
    df = stats.stats30(totalData)
    return df
        
        
#may be obsolete?        
def search(GameID, allGamesDict):
    team = GameID[:3]
    year = GameID[3:7]
    month = GameID[7:9]
    day = GameID[9:11]
    num = GameID[11:] #double headers
    val =  allGamesDict.get(GameID)
    if(not val):
        return -1
    return val
    
    
    
    

        
def setUpHashAll(teamID, lowestYear= 2021):
    '''
        allGamesDict will contain A mapping for every game from 2022 to lowestYear (default is 2018 currently).
                
        GAMENAME (ARI20004040) => stats that have been picked.
    
    '''
    allGamesDict = {}
    team = teamID
    year = 2022
    teamcsv = str(year) + team + "data.csv"
    while year >= lowestYear:
        teamcsv = str(year) + team + "data.csv"
        if(not os.path.isfile("./processedData/" + teamcsv)): #if team DNE skip
            year -=1
            continue
        for line in open("./processedData/" + teamcsv): #else get the data and plop in the fields to the dict
            fields = line.split(',')
            for i in range(0,len(fields)):
                fields[i] = fields[i].strip()
                fields[i] = fields[i].strip("\"")
            if(fields[0] not in allGamesDict): #if no val for key yet add one, then append
                allGamesDict[fields[0]] = list()
                allGamesDict[fields[0]].append(fields)
            else:
                allGamesDict[fields[0]].append(fields)
        for file in os.listdir("./processedData/"): #same thing but for away games, search every other team for games played against us
            if(str(year) not in file):
                continue
            for line in open("./processedData/" + file): #example file would be 2022SDNdata.CSV, searching for games against curteam
                fields = line.split(',')
                for i in range(0,len(fields)):
                    fields[i] = fields[i].strip()
                    fields[i] = fields[i].strip("\"")
                if str(team) != fields[1][:3]:
                    continue
                newZero = "".join(team)
                newZero += fields[0][3:]
                newOne = fields[0][:3] + 'v'
                fields[1] = newOne
                fields[0] = newZero
                if(newZero not in allGamesDict): #addgame but change game code to have our tag and set other team as away team. 
                    allGamesDict[fields[0]] = list()
                    allGamesDict[fields[0]].append(fields)
                else:
                    allGamesDict[fields[0]].append(fields)
                

        year -=1
        
    
    return allGamesDict

    
#SDN201709030
#SDN201709030
#getTeam30DayNums("SDN201804040")
