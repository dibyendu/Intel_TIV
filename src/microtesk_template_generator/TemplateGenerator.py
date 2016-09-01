import sys
#import pickle
#import os
import ConditionsModule

def GetActionLibrary(actions):
    actionLibrary={} # Dictionary of actions and their pre and post conditions
    for line in actions: # populating actionLibrary and registers dictionaries
        line = line.replace('\n','')
        line = line.split('\t')
        pre = list(set(line[1].split(',')))
        post = list(set(line[2].split(',')))
        actionLibrary[line[0]] = (pre,post)
    return actionLibrary

testPlan = str(sys.argv[1])
#PlanInitialCondition = pickle.load(open('PlanInitialCondition','rb')) # loaded the PlanInitialCondition dumped by Algo1.py
f = open(testPlan,'r')   # open the plan file generated.
g = f.readlines()          # read the plan.txt file
h = open('TestTemplate.rb','w+')   # create the test template file to be generated
#armInstructions = getInstructions()
templateFile = open('Template_Database.txt','r') # Open the template database
templates = templateFile.readlines() # read all lines in the template database
actionFile = open('Action_Database.txt','rb') # Open the action database
actions = actionFile.readlines() # read all lines in the action database
registersActive = [0,0,0,0,0,0,0,0,0,0,0,0,0]  # shows what registers are active currently, 0= inactive, 1= active

actionLibrary = GetActionLibrary(actions) # Dictionary of actions and their pre and post conditions

occurencePair = ConditionsModule.GetOccurenceOfConditions(g,actionLibrary)
occurenceOfConditions = occurencePair[1]
eventNo = occurencePair[0]

intervalsOfConditions = ConditionsModule.GetIntervalsOfConditions(occurenceOfConditions,eventNo) # dict containing the intervals of each condition which has registers in its pre or post conditions

registersTuple = ConditionsModule.GetRegistersAllocated(eventNo,intervalsOfConditions)

registersAllocated = registersTuple[0] # allocating registers to conditions based on intervals which have them in their pre or post conditions

eventConditionMapping = registersTuple[1]

print "Number of simultaneous conflicts in the test plan are ", registersTuple[2]
#print registersTuple[2]

h.write('require ENV[\'TEMPLATE\']\nrequire_relative \'arm_base\'\nclass ArmTest < ArmBase\ndef run\n') # write the initial lines of the test template
templateLibrary={}  # action: template dictionary
variables={} # variable : memory location dictionary
variables['x']='67' # assigning random memory locations to variables 'x' and 'y' and 'z'
variables['y']='99'
variables['z']='24'
for line in templates:  # forming the action:template dictionary
    line=line.split('###')
    if len(line)>1: # if the action has rules in the database
        templateLibrary[line[0]]=line[1:]
    else: # if the action doesnt have any rules in the database just keep a \n as its rule
        templateLibrary[line[0]]='\n'
eventNo = 0
for line in g: # iterating through the plan and writing the template for each action
    eventNo += 1
    line=line.split()[0]
    if "(y)" in line: # replacing the variable with '*' to search the templateLibrary
        line=line[:-3]+line[-3:].replace('y','*')
        index='y'
    elif "(x)" in line:
        line=line[:-3]+line[-3:].replace('x','*')
        index='x'
    elif "(z)" in line:
        line=line[:-3]+line[-3:].replace('z','*')
        index='z'
    registersActive = registersAllocated[eventNo]
    stringReplace = []
    if len(eventConditionMapping[eventNo]) > 0:
        for tup in eventConditionMapping[eventNo]:
            stringReplace.append((tup[1],tup[2]))
    tempRegsUsed = []  # list of temporary registers
    noOfTempRegs = int(templateLibrary[line][-1]) # no of temp Regs used by the event
    count = 0
    for i in registersActive: # checking if requisite no of temp registers available
        if i==0:
            count +=1
    if count < noOfTempRegs:
        print " REQUIRED NUMBER OF REGISTERS NOT AVAILABLE!"
        exit(0)
    else :
        tempRegsAssigned = 0
        for i in range(0,13):
            if tempRegsAssigned >= noOfTempRegs:
                break
            if registersActive[i] == 0 :
                tempRegsUsed.append(i)
                tempRegsAssigned += 1
                registersActive[i]=1
    for act in templateLibrary[line][:-1]: # writing each rule of the action in the test template file
        print act, line
        asd = act.replace('$$$',variables[index])
        fgh = asd.split()
        fgh = [x for x in fgh if x!='']
        regs = 0
        for tup in stringReplace:
            asd = asd.replace(tup[0],tup[1])
        for jkl in fgh:
            for i in range(0,noOfTempRegs): # replacing temp registers with their assigned registers if present in any instruction
                if 't' + str(i) in jkl:
                    asd = asd.replace('t' + str(i),'REG(' + str(tempRegsUsed[i]) + ')')
        h.write(asd+'\n')
    for i in tempRegsUsed:
        registersActive[i]=0
h.write('end\nend') # writing the last parts of the test template file and closing it.
h.close()
#print "OPENING THE COMPILED TEST TEMPLATE..."
#os.system("gnome-open TestTemplate.rb")
