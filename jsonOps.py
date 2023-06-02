import handleData as hd
import json 
import sys

# with open("./teamJsons/MON.json", "r") as rfile:
#     data = json.loads(json.load(rfile))





def writeTeams(lyear=2021):
    for line in open('./teamCodes.csv'):
        fields = line.split(',')
        fields[0] = fields[0].strip()
        fields = [s.strip('\"|\'') for s in fields]
        allGames = hd.setUpHashAll(fields[0], lowestYear=lyear)
        teamjson = fields[0] + '.json'
        #print(fields[0])
        jsonformat = json.dumps(allGames) 
        with open("./teamJsons/" + teamjson, "w") as outfile:
            json.dump(jsonformat, outfile)

#make a team loader

def writeDeltas(deltas):
    with open("./deltas/" + 'delta', "w") as outfile:
            json.dump(deltas, outfile)
            
def readDeltas(): #reads our json list of deltas
    with open("./deltas/" + 'delta', "r") as rfile:
        data = json.load(rfile)
    print(data)
    return data

def loadTeams():
    pulledJson = {}
    print(type(pulledJson))
    for line in open('./teamCodes.csv'):
        fields = line.split(',')
        fields[0] = fields[0].strip()
        fields = [s.strip('\"|\'') for s in fields]
        teamjson = fields[0] + '.json'
        #print(fields[0])
        with open("./teamJsons/" + teamjson, "r") as rfile:
            tmp = json.loads(json.load(rfile))
            pulledJson.update(tmp)
        #print(type(pulledJson))
    return pulledJson

#loadTeams()
