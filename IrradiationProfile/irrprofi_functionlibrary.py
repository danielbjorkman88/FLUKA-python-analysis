# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:57:08 2020

@author: dbjorkma
"""

# -*- coding: utf-8 -*-
"""
Script developed to create an interface for modelling of FLUKA irradiation profiles and 
to calculate the irradiation profiles of the LHC and its corresponding experiments.
By Daniel Björkman 2018 - 2021
daniel.bjorkman@cern.ch
"""



import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from copy import deepcopy
import pandas as pd
import datetime

def calcTimeline(experiment):

    lastidx = len(experiment)-3
    
    experiment[len(experiment)-2,2] = - experiment[len(experiment)-2,0]
    for i in range(lastidx,-1,-1):
        
        experiment[i,2] = -experiment[i,0] - abs(experiment[i+1,2])
    return experiment;
 
        

def readProfile(filename):
    
    #Column 1 = Time [days]
    #Column 2 = Beam intensity [particles/s] or [collisions/s]
    #Column 3 = to be filled as inverse time by function calcTimeline
    
    data = np.loadtxt(filename)
    
    ATLAS = np.zeros([data.shape[0]+2,3])
    
    ATLAS[1:len(ATLAS)-1,0:2] = data
    
    ATLAS[0:,0] = ATLAS[0:,0]/(60*60*24)

    ATLAS = calcTimeline(ATLAS)

    return ATLAS







def readLumi(filename,origo):
    

    data = pd.read_csv(filename)

    lumi = np.zeros([len(data),2])
        

    for i in range(len(data)):
        
        time = data['Date Time']

        instant = datetime.datetime( int(time[i].split('-')[0].strip()), int(time[i].split('-')[1].strip()), int(time[i].split('-')[2][0:2]), int(time[i].split('-')[2].split()[1][0:2]), int(time[i].split('-')[2].split()[1].split(':')[1]), int(time[i].split('-')[2].split()[1].split(':')[2][0:2]))

        timedifference = instant - origo
        timeindays = timedifference.total_seconds()/(60*60*24)
        lumi[i,0] = timeindays
        global experiment
        lumi[i,1] = data[experiment][i]
        

    return lumi




def sinceOrigo(instant):
    return (instant -origo).total_seconds()/(60*60*24)



    
    ATLAS = np.zeros([1,3])
    

def setMagnitude(lumi):
    
    from scipy.interpolate import interp1d
    x = lumi[0:,0]
    y = lumi[0:,1]
    lumiprofile = interp1d(x,y)
    
    def calcCollisions(ATLAS,tau2, tau1, xsec):
        timediff = (tau2 - tau1).total_seconds() 
        lumidiff = lumiprofile(sinceOrigo(tau2)) - lumiprofile(sinceOrigo(tau1)) #picobarn
        collisions = 1e12*lumidiff*xsec
        newrow = [timediff/(60*60*24),collisions/timediff,0]
        ATLAS = np.vstack([ATLAS,newrow])
        ATLAS = np.vstack([ATLAS,[0,0,0]])
        return ATLAS;
        

    
    #2011
    xsec = 72E-3 #mbarn
    ATLAS = calcCollisions(ATLAS,end2011,start2011, xsec)
   
    
    #2012
    xsec = 75E-3 #mbarn
    ATLAS = calcCollisions(ATLAS,end2012,start2012, xsec)
  

    xsec = 80E-3 #mbarn
    
    #2015
    ATLAS = calcCollisions(ATLAS,end2015,start2015, xsec)

    
    #2016
    ATLAS = calcCollisions(ATLAS,end2016,start2016, xsec)

    
    #2017
    ATLAS = calcCollisions(ATLAS,end2017,start2017, xsec)
 
    
    #2018, divided into T1, T2,T3 and T4
    
    #T1
    ATLAS = calcCollisions(ATLAS,T1end,T1start, xsec)


    #T2
    ATLAS = calcCollisions(ATLAS,T2end,T2start, xsec)    

    
    #T3
    ATLAS = calcCollisions(ATLAS,T3end,T3start, xsec)    

    
    #T4
    global T4end
    global T4start
    ATLAS = calcCollisions(ATLAS,T4end,T4start, xsec)    

    
    global experiment
    if experiment == 'ALICE':
    
        #Ion run
        xsec = 8. #barn
        protonIonFactor = 500/float(6)
        
        
        timediff = (ionEnd- ionStart).total_seconds() 
        lumidiff = 1E9 #barn 
        collisions = lumidiff*xsec
        newrow = [timediff/(60*60*24),protonIonFactor*collisions/timediff,0]
        ATLAS = np.vstack([ATLAS,newrow])
        ATLAS = np.vstack([ATLAS,[0,0,0]])
    
    return ATLAS;





def calcTimingNewprofile(dates,experimentMagnitudes, origo):
    experiment = np.zeros(experimentMagnitudes.shape)
    experiment[0:,1] = experimentMagnitudes[0:,1]    
    for i in range(len(experiment)-2,0,-1):
        if experiment[i,1] == 0:
            instance = dates.pop(0)
            timediff = (origo - instance).total_seconds() - sum(experiment[i:,0])
            experiment[i,0] = timediff
            
        else:
            
            experiment[i,0] = (60*60*24)*experimentMagnitudes[i,0]
    
    experiment[0:,0] = experiment[0:,0]/(60*60*24)
    
    experiment = calcTimeline(experiment)
    return experiment



def numberCollisions(experiment):
    return sum(experiment[0:,1]*experiment[0:,0])*24*60*60




def plot(profile, config):
    
    
    origo = config["origo"]
    experiment = config["experiment_name"]
    title = config["title"] 
    lumi = config["lumi"]
    

    


      
    
    
    #newyear2018 = datetime.datetime(2018,12,31,23,59,59)
    newyear2024 = datetime.datetime(2024,12,31,23,59,59)
    timedifference = origo - newyear2024
    newyearsOrigodifference = timedifference.total_seconds()/(60*60*24)
    
    xticks = []
    for i in range(1,15):
        xticks.append(-365*i - newyearsOrigodifference)
    
    
    #xticks = list(range(int(-365*1 - newyearsOrigodifference), int( -365*15 - newyearsOrigodifference), -365))
    xlabels = list("           " + str(item) for item in range(2024,2024-14, -1))
    

    
    fig = plt.figure()
    
    
    ax = fig.add_subplot(111)
    
    label = "{} and LHC LSS1 profile, #Collisons= ".format(experiment)  + "%.5g" % numberCollisions(profile) 
    ax.step(profile[0:,2], profile[0:,1]/(1E9) , label = label,where='post'  ) 



    lines_1, labels_1 = ax.get_legend_handles_labels()
    

    plt.xlabel("Time [years]",  fontsize = 18)
    
    ax.set_ylabel('Collision Rate [1E9 collisions/s]',  fontsize = 18)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=12)
    
    ax2 = ax.twinx()
    lumicolor = 'm'
    #Lumi divided by 1000 to be expressed in fb-1 instead of pb-1
    ax2.plot(lumi[0:,0],lumi[0:,1]/1000, label = 'Integrated Luminosity = ' +  str(round(lumi[-1,1]/1000,5))  + " fb-1", linestyle = '--', color = lumicolor)
    ax2.tick_params(axis='y', colors=lumicolor)    
    ax2.set_ylabel('Integrated luminosity [fb-1]',  fontsize = 18)



    
    
    for i in range(1,15):
        plt.axvline(x=-365*i - newyearsOrigodifference, color = 'k', linestyle = '--', linewidth=0.1, alpha = 0.5)        

        
    lines_2, labels_2 = ax2.get_legend_handles_labels()

    
    
    plt.title(title, fontsize = 18)

    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    ax.legend(lines, labels, loc=2 , prop={'size': 16})
    
   

    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    plt.yticks(fontsize=12)

    
    xlength = 10
    fig.set_size_inches(xlength, xlength/1.618)
    plt.show()
    try:
        plt.savefig(config["output_filename"],  bbox_inches = 'tight', pad_inches = 0.1)
    except:
        pass;





def collisionsCheck(ATLAS, lumi):
    
    
    x = lumi[0:,0]
    y = lumi[0:,1]
    lumiprofile = interp1d(x,y)
    
    #2011
    xsec = 72E-3 #barn
    endfirstxsec = sinceOrigo(datetime.datetime(2011, 12, 30, 00, 00))
    lumiCollisions = 1e12*lumiprofile(endfirstxsec)*xsec
    
    #2012
    xsec = 75E-3 #barn
    endsecondxsec = sinceOrigo(datetime.datetime(2012, 12, 30, 00, 00))
    lumiCollisions = lumiCollisions + 1e12*(lumiprofile(endsecondxsec) - lumiprofile(endfirstxsec))*xsec
    
    #2015 - 2018    
    xsec = 80E-3 #barn
    endlastxsec = sinceOrigo(datetime.datetime(2018, 10, 30, 00, 00))
    lumiCollisions = lumiCollisions +  1e12*(lumiprofile(endlastxsec) - lumiprofile(endsecondxsec))*xsec
    
    global experiment
    
    if experiment == 'ALICE':
        #Ion run  
        xsec = 8. #barn
        protonIonFactor = 500/float(6)
        lumidiff = 1E9 #barn-1
        collisions = lumidiff*xsec
        ppcollisionsOfIonRun = collisions*protonIonFactor
        lumiCollisions = lumiCollisions + ppcollisionsOfIonRun
    
    print(experiment + ' #Collisions/Lumi collisions = ')
    print(str(numberCollisions(ATLAS)/lumiCollisions))

    print(' ')
    
    


def writeProfile(experiment, outname):

    
    f = open(outname, 'w')
    f.write('* ..+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8\n')
    now = datetime.datetime.now()
    f.write('* Profile written by irradiation profile script on ' + str(now) + '\n')
    for i in range(len(experiment)):
        if experiment[i,0] == 0:
            pass
        else:
            if i  % 3 == 1:
                string = 'IRRPROFI  '
  
            #round to closest second/integer
            val1 = int(round(experiment[i,0]*24*60*60))
            val2 = int(round(experiment[i,1]))
            
            if len(str(val1)) >10: 
                string = string + ("%.4e" % val1).rjust(10)
            else:
                string = string + str(val1).rjust(10)
            
            if len(str(val2)) >10:
                string = string + ("%.4e" % val2).rjust(10)
            else:
                string = string + str(val2).rjust(10)
            
            if i  % 3 == 0 or  i +2 == len(experiment):
                f.write(string + '\n')
                
            
    f.close()



def calcCollisionsFromExpectedLumi(ATLAS,tau2, tau1, xsec, lumidiff):
    timediff = (tau2 - tau1).total_seconds() 
    collisions = lumidiff*xsec*1E12
    newrow = [timediff/(60*60*24),collisions/timediff,0]
    ATLAS = np.vstack([ATLAS,newrow])
    return ATLAS;


def calcCollisionsFromExpectedCollisions(ATLAS,tau2, tau1, collisions):
    timediff = (tau2 - tau1).total_seconds() 
    newrow = [timediff/(60*60*24),collisions/timediff,0]
    ATLAS = np.vstack([ATLAS,newrow])
    return ATLAS;

def calcShutdownTime(ATLAS,tau2, tau1):
    timediff = (tau2 - tau1).total_seconds() 
    newrow = [timediff/(60*60*24),0,0]
    ATLAS = np.vstack([ATLAS,newrow])
    return ATLAS;



def constructProfileFromPredictedOperations(experiment, predictedOperations):
    experiment = experiment[:-1,:] # Removes bottom padding

    

    for item in predictedOperations:
        
        if len(item) == 4:
            experiment = calcCollisionsFromExpectedCollisions(experiment,item[0],item[1], item[3])
        elif item[2] == 0:
            experiment = calcShutdownTime(experiment,item[0],item[1])
        else:
            experiment = calcCollisionsFromExpectedLumi(experiment,item[0],item[1], xsecRun3, item[2])
        
            
    newrow = [0,0,0] # the padding
    experiment = np.vstack([experiment,newrow]) #Adds bottom padding
    return experiment




def lumiFromPredictedOperations(lumi, predictedOperations, origo ):
    
    integradedLumi = lumi[-1,1]
    time = origo + datetime.timedelta(lumi[-1,0])
    currTime = lumi[-1,0]
    
    for item in predictedOperations:
        #print(time)
        timediff = (item[0] - time).total_seconds()/(60*60*24)
        time += datetime.timedelta(timediff)
        currTime += timediff        
        
        integradedLumi = integradedLumi + item[2]
        newrow = [currTime , integradedLumi]
        lumi = np.vstack([lumi,newrow])
        

    
    
    return lumi






LS2 = datetime.datetime(2018,10,23,13,22,00) #end of proton-proton run
LS2ion = datetime.datetime(2018,12,3,6,00,00) # end of ion run



end2011 = datetime.datetime(2011,10,30,9,57,00)
end2012 = datetime.datetime(2012,12,16,11,58,00)
end2015 = datetime.datetime(2015,11,21,19,22,00)
end2016 = datetime.datetime(2016,10,26,7,49,00)
end2017 = datetime.datetime(2017,11,26,00,29,00)



start2011 = datetime.datetime(2011,3,13,13,35,9)
start2012 = datetime.datetime(2012,4,6,23,15,36)
start2015 = datetime.datetime(2015,6,5,23,17,23)
start2016 = datetime.datetime(2016,4,22,22,38,37)
start2017 = datetime.datetime(2017,5,23,14,45,27)




#2018
T1end = datetime.datetime(2018,6,11,23,39,11)
T1start = datetime.datetime(2018,4,17,11,00,23)

T2end =  datetime.datetime(2018,7,22,18,22,43)
T2start = datetime.datetime(2018,6,26,19,22,10)

T3end = datetime.datetime(2018,9,10,3,18,45)
T3start = datetime.datetime(2018,8,1,2,8,37)

T4end =  LS2 #end of proton-proton run
T4start = datetime.datetime(2018,9,23,17,55,33)


# 2018 Ion run
ionEnd = LS2ion
ionStart = datetime.datetime(2018,11,8,00,00,00)

operationsScheduleAtlas = []
operationsScheduleAtlas.append(T3end)
operationsScheduleAtlas.append(T2end)
operationsScheduleAtlas.append(T1end)
operationsScheduleAtlas.append(end2017)
operationsScheduleAtlas.append(end2016)
operationsScheduleAtlas.append(end2015)
operationsScheduleAtlas.append(end2012)
operationsScheduleAtlas.append(end2011)


operationsScheduleAlice = deepcopy(operationsScheduleAtlas)
operationsScheduleAlice.insert(0,T4end) #add ion run
operationsScheduleCMS = deepcopy(operationsScheduleAtlas)
operationsScheduleLHCb = deepcopy(operationsScheduleAtlas)



#Predicted operational parameters --------------------------------------------------------------

#Info predicted by by Jorg Wenninger <Jorg.Wenninger@cern.ch> on 4/9/2020

# Dates are estimated
LS3 = datetime.datetime(2024,10,23,13,22,00) #end of proton-proton run
end2022 = datetime.datetime(2022,10,26,7,49,00)
end2023 = datetime.datetime(2023,11,26,00,29,00)
end2024 = LS3

approxYearlyOperationTime = datetime.timedelta(days=160)

start2022 = end2022 - approxYearlyOperationTime
start2023 = end2023 - approxYearlyOperationTime
start2024 = end2024 - approxYearlyOperationTime


xsecRun3 = 80E-3 #barn
instLumi = 2e34 # cm-2 s-1

lumidiff2022 = 60E3 #pb-1
lumidiff2023 = 100E3 #pb-1
lumidiff2024 = 100E3 #pb-1


#----------------------------------------------------------------------------------------------
predictedOperations = []
predictedOperations.append((start2022, LS2, 0))
predictedOperations.append((end2022, start2022, lumidiff2022))
predictedOperations.append((start2023, end2022, 0))
predictedOperations.append((end2023, start2023, lumidiff2023))
predictedOperations.append((start2024, end2023, 0))

# 2024 divided up into normal operations and a 12 h last fill at instantaneous luminosity 2e34 cm-2 s-1
collisions2024 = lumidiff2024*xsecRun3*1E12 # number of collisons 2024
xsecRun3Percm2 = xsecRun3*1E-24 # barn = 10−24 cm-2
lastFillCollisions = instLumi*(12*60*60)*xsecRun3Percm2 # number of collisons for last fill
assert lastFillCollisions < collisions2024
lastfillStart = LS3 - datetime.timedelta(hours=12)

predictedOperations.append((lastfillStart, start2024, (collisions2024 - lastFillCollisions)/(xsecRun3*1E12), collisions2024 - lastFillCollisions))
predictedOperations.append((LS3, lastfillStart, lastFillCollisions/(xsecRun3*1E12), lastFillCollisions))

#ATLAS = constructProfileFromPredictedOperations(ATLAS, predictedOperations)
#CMS = constructProfileFromPredictedOperations(CMS, predictedOperations)


