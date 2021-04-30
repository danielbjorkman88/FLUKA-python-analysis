# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:28:33 2021

@author: dbjorkma
"""
import datetime 


LS2 = datetime.datetime(2018,10,23,13,22,00)


# Approximate LHC element limits

element_limits = {}
element_limits["IT"] = [0,5651] #cm
element_limits["D1"] = [5803, 8787]
element_limits["TAN"] = [13464, 14722 ]
element_limits["TCL4"] = [14900 , 15090]
element_limits["D2 Q4"] = [15190, 17900]
element_limits["TCL5"] = [17900, 18848 ]
element_limits["TCL6"] = [21199, 22500 ]

element_limits["Q5"] = [18900, 20500]
element_limits["Q6"] = [22500, 24000]

element_limits["All"] = [0, 26000 ]




# Useful positions of LHC element labels

xpos = -65

machine_labels = {}
machine_labels["Q1"] = [2670 - 300, xpos]
machine_labels["Q2"] = [3800 - 300, xpos]
machine_labels["Q3"] = [5030 - 300, xpos]

#machine_labels["TAS"] = [2000- 300, xpos]

machine_labels["D1"] = [7000 - 100, xpos]
machine_labels["TAN"] = [14300 - 300, xpos]

machine_labels["D2, Q4"] = [16250  - 700, xpos]
machine_labels["Q5"] = [19600 - 300 , xpos]
machine_labels["Q6"] = [22800 - 300 , xpos]
machine_labels["Q7"] = [26150 - 300 , xpos]

machine_labels["TCL4"] = [15000 - 500 , 15]
machine_labels["TCL5"] = [18440 - 500 , 15]
machine_labels["TCL6"] = [21900 - 500 , 15]




y_beamaxis = 15 # bin number y axis
x_1meter = 20 # bin number x axis corresponding 1 meter from beam axis

