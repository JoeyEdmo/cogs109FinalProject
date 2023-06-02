import os

'''

only need to run script when you update the args or pull older than 2000 data.

Would also need to download the <2000 data from site and dump it into alldata.

currently not using argsdict but might be nice in future if just loading all values?

'''






# assign directory
directory = './alldata'
resultdir = "../processedData/"
eventArgsFile = 'eventArgs.txt'
nums = '0123456789'
#0 game id, #1 = visiting team, 2-6: inning, batting team, outs, balls, strikes,
# 8-9 visitor/home score respectively (to calc win w/ 79), 10 player id, 26-28: runners 1-3, 33:line up spot, 34:event type, 
#35:event flag (stolen base vs out), 36:at bat flag, 37:HIT VALUE, 38 sac hit, 39: sac fly,40: outs on play, 43:   RBI on play*, 58-61: batter + runner result
#79 End game flag, 
ARGS="0-6,8-10,26-28,33-40,43,58-61,79"
argsFile = open(eventArgsFile)
argsDict = {}
#fill argsDict with values so we can pass readable args larter (not using?)
for line in argsFile:
    vals = line.split("   ")
    vals[0] = vals[0].strip()
    vals[1] = vals[1].strip()
    argsDict[vals[1]] = vals[0]
    
    
#set up the data into the folder
os.chdir(directory)
for filename in os.listdir("."):
    numArg = ''.join(c for c in filename if c in nums)
    teamCode = "".join(c for c in (filename.split(".")[0]) if c not in nums)
    if(not numArg):
        continue
    if(".EV" not in filename):
        continue
    bashCommand = "cwevent -f " + ARGS  + " -y " + numArg + " " +  filename + " > " + resultdir + numArg + teamCode + "data.csv"
    print(bashCommand) 
    os.system(bashCommand)
os.chdir("..")


