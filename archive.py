def setUpHash(GameID):
    '''
        OBSOLETE, USE SETUPHASHALL
    
    '''
    allGamesDict = {} 
    team = GameID[:3]
    year = GameID[3:7]
    teamcsv = year + team + "data.csv"
    if not os.path.isfile("./processedData/" + teamcsv):
        raise Exception("bad arg to setUpHash")
    
    for line in open("./processedData/" + teamcsv):
        fields = line.split(',')
        fields[0] = fields[0].strip()
        if(fields[0] not in allGamesDict):
            allGamesDict[fields[0]] = list()
            allGamesDict[fields[0]].append(fields)
        else:
            allGamesDict[fields[0]].append(fields)

    #also need last years data
    year = str(int(year)-1)
    teamcsv = year + team + "data.csv"
    for line in open("./processedData/" + teamcsv):
        fields = line.split(',')
        fields[0] = fields[0].strip("\"")
        if(fields[0] not in allGamesDict):
            allGamesDict[fields[0]] = list()
            allGamesDict[fields[0]].append(fields)
        else:
            allGamesDict[fields[0]].append(fields)
   
    #difficult for away games
    for file in os.listdir("./processedData/"):
        if(year not in file and str(int(year)+1) not in file):
            continue
        for line in open("./processedData/" + file):
            fields = line.split(',')
            fields[1] = fields[1].strip("\"")
            
            if team != fields[1]:
                continue
            fields[0] = fields[0].strip("\"")
            newZero = "".join(team)
            newZero += fields[0][4:]
            fields[0] = newZero
            if(newZero not in allGamesDict):
                allGamesDict[fields[0]] = list()
                allGamesDict[fields[0]].append(fields)
            else:
                allGamesDict[fields[0]].append(fields)
        
    
    print(len(allGamesDict))
    return allGamesDict