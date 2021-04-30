# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:01:33 2020

@author: dbjorkma
"""

import glob, os
import pandas as pd
import matplotlib.pyplot as plt
from USRBIN import USRBIN
from scipy.interpolate import interp1d
import matplotlib.patches as patches
import numpy as np
import math
from statistics import mean, stdev



class Survey():
    
    def __init__(self, filenameSurvey, path, origo):
        self.filename = filenameSurvey
        self.path = path
        self.origo = origo
        self.elementDict = {}
        self.surveyElements = []
        self.surveyElementsCount = {}
        self.doseRateContact = {}
        self.doseRate1meter = {}
        self.xes = []
        self.yesContact = []
        self.yes1meter = []

        self.xesContact = []
        self.yesContact = []
        
        self.xes40cm = []
        self.yes40cm = []



        # self.readElements()
        # self.correctDB(position_corrections)
        # self.readSurvey()
        # self.printMissing()
        # self.constructPlotInput()



    def dataFromFile(self, filenames):
        
        
        matrix_contact = np.load(filenames[0])
        matrix_40cm = np.load(filenames[1])
        

        

        
        self.xesContact = matrix_contact[0:,0]
        self.yesContact = matrix_contact[0:,1]
        
        self.xes40cm = matrix_40cm[0:,0]
        self.yes40cm = matrix_40cm[0:,1]
        



    def export(self):
        
        xes_contact = self.xes
        yes_contact = self.yesContact
        
        assert len(xes_contact) == len(yes_contact)
        
        M = np.zeros([len(xes_contact), 2])
        
        M[0:,0] = xes_contact
        M[0:,1] = yes_contact
        
        np.save('Contact_{}.npy'.format(self.filename[:-4]), M)    # .npy extension is added if not given

        




    def correctDB(self, position_corrections):
        
        print("Correcting database")
        
        for item in list(position_corrections.keys()):
            print(item)
            for pos in list(position_corrections[item].keys()):
                print("Before ", self.elementDict[item][pos])
                print(item,pos, position_corrections[item][pos])
                self.elementDict[item][pos] = position_corrections[item][pos]

        

    def readSurvey(self):
        f = open(self.filename, 'r').readlines()
        fileformat = "normal"
        if f[0].split()[0] == "DCUM":
            fileformat = "alternative"
            
        if fileformat == "normal":  
            f = f[7:-8]
            idx = [0,1,2]
        elif fileformat == "alternative":
            f = f[7:]
            idx = [1,2,3]
        
        for item  in f:
            name = item.split()[idx[0]]
            doserateContact = float(item.split()[idx[1]])
            try:
                doserate1meter = float(item.split()[idx[2]])
            except:
                doserate1meter = None        
                                
            if name not in self.surveyElements:
                if name != "Chambre.":
                    self.surveyElements.append(name)
                    self.surveyElementsCount[name] = 1
                    self.doseRateContact[name] = [doserateContact]
                    self.doseRate1meter[name] = [doserate1meter]

            else:
                self.surveyElementsCount[name] += 1
                self.doseRateContact[name].append(doserateContact)
                self.doseRate1meter[name].append(doserate1meter)    

    def constructPlotInput(self):
        for item in self.surveyElements:
            

            info = self.elementDict[item]

            
            if float(info[mid]) - self.origo < 260: #Fluka geo restriction
                if self.surveyElementsCount[item] == 1:
                    self.xes.append(float(info[mid]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][0])
                    self.yes1meter.append(self.doseRate1meter[item][0])
                elif self.surveyElementsCount[item] == 2:
                    self.xes.append(float(info[start]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][0])
                    self.yes1meter.append(self.doseRate1meter[item][0])
            
                    self.xes.append(float(info[end]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][1])
                    self.yes1meter.append(self.doseRate1meter[item][1])        
                    
                elif self.surveyElementsCount[item] == 3:

                        

                    self.xes.append(float(info[start]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][0])
                    self.yes1meter.append(self.doseRate1meter[item][0])
            
                    self.xes.append(float(info[mid]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][1])
                    self.yes1meter.append(self.doseRate1meter[item][1])
                    
                    self.xes.append(float(info[end]) - self.origo)
                    self.yesContact.append(self.doseRateContact[item][2])
                    self.yes1meter.append(self.doseRate1meter[item][2])        



                else:
                    print("ERROR", item)
        
    def printElement(self, element):
        print(element,  self.elementDict[element][start] ,  self.elementDict[element][mid],  self.elementDict[element][end])


    def printMissing(self):
        missingElements = []
        for i, item in enumerate(self.surveyElements):
            name = item.split()[0]
            if name not in self.elementDict:
                missingElements.append(name)   
        if len(missingElements) > 0:
            print("Missing:")
            print(missingElements)

    
    def readElements(self):
        os.chdir(self.path)
        for filenameCSV in glob.glob("*.csv"):
        #filenameCSV = "all.csv"
            df = pd.read_csv(filenameCSV, encoding = "ISO-8859-1", index_col ="Name")
            #df.rename(columns={"Dcum Start S": "start", "Dcum Mid S": "mid", "Dcum End S": "end"})
            for name, row in df.iterrows():
                try:    
                        
                        if not row["Dcum Start S"] == row["Dcum Mid S"] == row["Dcum End S"] == "---":
                    
                            self.elementDict[name] = row         
                            
                            
                            if name[-2:] == 'B1' or name[-2:] == 'B2':
                                if name[-3:] not in self.elementDict:
                                    self.elementDict[name[:-3]] = row
                      
                                
                                
                            if name[:2] == "VA":
                                if name[6] == "A":
                                    self.elementDict[name[:6] + name[7:]] = row
                                    
                                if  name[5] == "A" and name[7] == "A":
                                    self.elementDict[name[:5] + "." + name[8:]] = row                    
                except:
                    pass





