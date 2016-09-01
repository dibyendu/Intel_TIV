def GetOccurenceOfConditions(g,actionLibrary):
    occurenceOfConditions = {}
    eventNo = 1 
    for event in g: # for loop to identify which conditions have registers in their conditions in the given plan
        event = event.strip()
        event = event[:-6] + event[-6:].replace("(x)","(*)")
        event = event[:-6] + event[-6:].replace("(y)","(*)")
        event = event[:-6] + event[-6:].replace("(z)","(*)")
        pre = actionLibrary[event][0]
        post = actionLibrary[event][1]
        for cond in pre: # adding the pre conditions to occurenceOfConditions dict which is used to prepare intervals
           for i in range(0,13):
                if "REG("+str(i)+")" in cond:
                    if cond not in occurenceOfConditions:
                        occurenceOfConditions[cond] = {}
                    if "pre" not in occurenceOfConditions[cond]:
                        occurenceOfConditions[cond]["pre"] = []
                    occurenceOfConditions[cond]["pre"].append((eventNo,"REG("+str(i)+")"))
        for cond in post: # adding the post conditions to occurenceOfConditions dict which is used to prepare intervals
           for i in range(0,13):
                if "REG("+str(i)+")" in cond:
                    if cond not in occurenceOfConditions:
                        occurenceOfConditions[cond] = {}
                    if "post" not in occurenceOfConditions[cond]:
                        occurenceOfConditions[cond]["post"] = []
                    occurenceOfConditions[cond]["post"].append((eventNo,"REG("+str(i)+")"))
        eventNo += 1
    eventNo -= 1 # no of events in the plan
    return (eventNo,occurenceOfConditions)

def GetIntervalsOfConditions(occurenceOfConditions,eventNo):
    intervalsOfConditions = {} # dict containing the intervals of each condition which has registers in its pre or post conditions
    for cond in occurenceOfConditions: # for loop which calculates the intervals for each of the conditions based on the plan
        if "pre" in occurenceOfConditions[cond] and "post" not in occurenceOfConditions[cond]:
            if len(occurenceOfConditions[cond]["pre"])==1:
                initialOccurence = occurenceOfConditions[cond]["pre"][0]
                intervalsOfConditions[cond] = (initialOccurence[0],initialOccurence[0],initialOccurence[1])
            else :
                initialOccurence = occurenceOfConditions[cond]["pre"][0]
                finalOccurence = occurenceOfConditions[cond]["pre"][-1]
                intervalsOfConditions[cond] = (initialOccurence[0],initialOccurence[0],initialOccurence[1])
        if "pre" not in occurenceOfConditions[cond] and "post" in occurenceOfConditions[cond]:
                intervalsOfConditions[cond] = (occurenceOfConditions[cond]["post"][0][0],eventNo,occurenceOfConditions[cond]["post"][0][1])
        if "pre" in occurenceOfConditions[cond] and "post" in occurenceOfConditions[cond]:
                if occurenceOfConditions[cond]["pre"][0] <= occurenceOfConditions[cond]["post"][0]:
                    initialOccurence = occurenceOfConditions[cond]["pre"][0]
                else :
                    initialOccurence = occurenceOfConditions[cond]["post"][0]
                if occurenceOfConditions[cond]["pre"][-1] > occurenceOfConditions[cond]["post"][-1]:
                    finalOccurence = occurenceOfConditions[cond]["pre"][-1]
                    intervalsOfConditions[cond] = (initialOccurence[0],finalOccurence[0],initialOccurence[1])
                else :
                    intervalsOfConditions[cond] = (initialOccurence[0],eventNo,initialOccurence[1])
    return intervalsOfConditions

def GetRegistersAllocated(eventNo,intervalsOfConditions):
    registersAllocated = {} # allocating registers to conditions based on intervals which have them in their pre or post conditions
    eventConditionMapping = {}
    registersConditionsAllocated = {}
    noOfConflicts = 0
    for i in range(1,eventNo+1):
        eventConditionMapping[i] = []
        registersAllocated[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for cond in registersConditionsAllocated:
            j = registersConditionsAllocated[cond]
            registersAllocated[i][j]=1
            eventConditionMapping[i].append((cond,intervalsOfConditions[cond][2],"REG(" + str(j) + ")"))
        for cond in intervalsOfConditions:
            if intervalsOfConditions[cond][0] > i and cond in registersConditionsAllocated:
                registersConditionsAllocated.pop(cond,None)
            if intervalsOfConditions[cond][1] < i and cond in registersConditionsAllocated:
                registersConditionsAllocated.pop(cond,None)
            if cond in registersConditionsAllocated:
                continue
            if intervalsOfConditions[cond][0] <= i and intervalsOfConditions[cond][1] >= i:
                j = 0
                while j < 13:
                    if registersAllocated[i][j] == 1:
                        j += 1
                        continue
                    else:
                        eventConditionMapping[i].append((cond,intervalsOfConditions[cond][2],"REG(" + str(j) + ")"))
                        registersAllocated[i][j] = 1
                        registersConditionsAllocated[cond] = j
                        break
                if j == 13:
                    #print "TOO MANY SIMULTANEOUS CONFLICTS TO HANDLE!!"
                    print 14
                    exit(0)
        temp = 0 
        for k in registersAllocated[i]:
            if k == 1:
                temp += 1
        if temp > noOfConflicts:
            noOfConflicts = temp
    return (registersAllocated,eventConditionMapping,noOfConflicts)