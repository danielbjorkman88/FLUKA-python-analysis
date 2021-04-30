# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:01:33 2020

@author: dbjorkma
"""

import os, sys
from matplotlib.colors import LogNorm
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
path = os.getcwd()
sys.path.insert(0, os.path.split(os.getcwd())[0] + "\\USRBIN")
path_data = os.path.split(os.getcwd())[0] + "\\Data"
sys.path.insert(0, path_data)
path_drawings = os.path.split(os.getcwd())[0] + "\\Data\\Drawings"
sys.path.insert(0, path_drawings)
from USRBIN import USRBIN
from LHC_constants import *
from Survey import Survey
from SupportInfo import *
import pandas as pd
import matplotlib.pyplot as plt
from USRBIN import USRBIN
from scipy.interpolate import interp1d
import matplotlib.patches as patches
import numpy as np
import math
from statistics import mean, stdev




class pointAnalysis:
    def __init__(self, fluka_name_1, fluka_name_2, mypath, filenameSurvey, path, origo, position_corrections):
        self.fluka1 = USRBIN(fluka_name_1, path, 0.0036)
        self.fluka2 = USRBIN(fluka_name_2, path, 0.0036)
        self.survey = Survey(filenameSurvey, path, origo , position_corrections)
        self.mypath = mypath
        self.merged = []
        # self.yesContact = []
        # self.yesContactError = []
        # self.yes40cm = []
        # self.yes40cmError = []       
        # self.xesContact = []

        


        # self.setup()
        # self.valuesofpath()
        # comparison1.calcErrors()
        # self.calc()

    def export(self):
        
        
        
        xes_40cm = self.survey.xes40cm
        yes_40cm = self.survey.yes40cm
        
        assert len(xes_40cm) == len(yes_40cm)
        
        M = np.zeros([len(xes_40cm), 2])
        
        M[0:,0] = xes_40cm
        M[0:,1] = yes_40cm
        
        np.save('40cm_{}.npy'.format(self.survey.filename[:-4]), M)    # .npy extension is added if not given

        
        
        
    def setup(self):
        

        self.fluka1.readError()
        self.fluka2.readError()
        
        self.merged = self.fluka1
        self.merged.cube = self.fluka1.cube + self.fluka2.cube
        
        for i in range(self.fluka1.cube.shape[0]):
           for j in range(self.fluka1.cube.shape[1]):
               for k in range(self.fluka1.cube.shape[2]):
                   self.merged.cubeErrors[i,j,k] = math.sqrt(self.fluka1.cubeErrors[i,j,k]**2 + self.fluka2.cubeErrors[i,j,k]**2)
                
        # self.xes40cm = []
        # self.survey.yes40cm = []
        # for i in range(len(self.survey.xesContact)):
        #     if self.survey.yes1meter[i] != None:
        #         self.xes40cm.append(self.survey.xesContact[i])
        #         self.survey.yes40cm.append(self.survey.yes1meter[i])



    def valuesofpath(self):
        
        self.yesContact = np.zeros(self.fluka1.cube.shape[2])
        self.yesContactError = np.zeros(self.fluka1.cube.shape[2])
        self.yes40cm = np.zeros(self.fluka1.cube.shape[2])
        self.yes40cmError = np.zeros(self.fluka1.cube.shape[2])  
        mypath = self.mypath
        
        
        
        zStart = 2090
        idx = 0
        for z in range(self.fluka1.cube.shape[2]):

            self.yesContact[z] = self.merged.cube[mypath[idx][1],0,z]
            self.yesContactError[z] = self.merged.cubeErrors[mypath[idx][1],0,z]
            self.yes40cm[z] = self.merged.cube[mypath[idx][1] - 40 ,0,z]
            self.yes40cmError[z] = self.merged.cubeErrors[mypath[idx][1] - 40 ,0,z]
        

            if z*10 + zStart > mypath[idx][2]:
                idx += 1
                
                
                
    def high_light_path(self):
        

        mypath = self.mypath
        pathValue = 400000
        zStart = 2090 #1291
        idx = 0
        self.cubePath = self.merged.cube.copy()
        for z in range(self.fluka1.cube.shape[2]):
            self.cubePath[mypath[idx][1],0,z] = pathValue
            if z*10 + zStart > mypath[idx][2]:
                idx += 1
                
    def calcErrors(self):
        

        self.AD6_abs_error_contact = np.array(self.survey.yesContact)*0.3

    
    
        function_of_relevant_errors = interp1d(self.merged.xcoordinates/100, self.yesContactError/100 ) #second vector in fraction instead of percent 
        

        self.rel_errors_for_ratio = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_contact/self.survey.yesContact, function_of_relevant_errors(self.survey.xesContact)))



        self.AD6_abs_error_40cm = np.array(self.survey.yes40cm)*0.3

    def calc(self):
        self.xesContact = self.merged.xcoordinates/100

        
        fluka_interpolated_contact_function = interp1d(self.xesContact, self.yesContact)
             

        self.ratiosContactmerged = fluka_interpolated_contact_function(self.survey.xesContact)/self.survey.yesContact
        
        self.w_mean, self.sd = self.weightedMean(self.ratiosContactmerged , self.rel_errors_for_ratio)
        
        


    def ratios_in_range(self, ax, xmin, xmax):
        
        sub_xes_contact = []
        sub_xes_40cm = []
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yesContactError/100 )
        rel_ratioerrors_contact = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_contact /self.survey.yesContact, ferrors(self.survey.xes)))
        sub_rel_ratioerrors_contact = []
        for i, z in enumerate(self.survey.xes):
            if z > xmin and z < xmax:               
                sub_rel_ratioerrors_contact.append(rel_ratioerrors_contact[i])    
                sub_xes_contact.append(z)
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors_40cm = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        sub_rel_ratioerrors_40cm = []
        for i, z in enumerate(self.survey.xes40cm):
            if z > xmin and z < xmax:               
                sub_rel_ratioerrors_40cm.append(rel_ratioerrors_40cm[i])    
                sub_xes_40cm.append(z)
        
        sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm = self.mean_by_range([xmin*100, xmax*100])

    
    
        # print(len(comparison.survey.xes) , len(sub_ratiosContact))
        #ax.errorbar(sub_xes_contact, sub_ratiosContact, yerr = sub_ratiosContact *sub_rel_ratioerrors_contact , label = "Contact Fluka/Measurements" , marker=".", linestyle= 'None', markersize = 12)
        #ax.axhline(y=sub_weightedMean_contact, color='C0', linestyle='-', linewidth = 2, label =  "Contact weighted mean of ratio = {} \u00B1 {}".format( round(sub_weightedMean_contact,4), round(sub_sd_contact,4) ) )
        ax.plot([xmin, xmax], [sub_weightedMean_contact, sub_weightedMean_contact], color='C0', linestyle='-', linewidth = 2)
        
        rect = plt.Rectangle((xmin, sub_weightedMean_contact - 1*sub_sd_contact),
              (xmax - xmin),
              2*sub_sd_contact, color = 'C0', alpha = 0.05 ,  edgecolor = None)
        ax.add_patch(rect)
        
    
        #ax.errorbar(sub_xes_40cm, sub_ratios40cm , yerr = sub_ratios40cm *sub_rel_ratioerrors_40cm , label =  "40 cm Fluka/Measurements", marker=".", linestyle= 'None', markersize = 12)
        #ax.axhline(y=sub_weightedMean_40cm, color='C1', linestyle='-', linewidth = 2, label =  "40 cm weighted mean of ratio = {} \u00B1 {}".format( round(sub_weightedMean_40cm,4), round(sub_sd_40cm,4) ) )
        ax.plot([xmin, xmax], [sub_weightedMean_40cm, sub_weightedMean_40cm], color='C1', linestyle='-', linewidth = 2)
        rect = plt.Rectangle((xmin, sub_weightedMean_40cm - 1*sub_sd_40cm),
              (xmax - xmin),
              2*sub_sd_40cm, color = 'C1', alpha = 0.05 ,  edgecolor = None)
        ax.add_patch(rect)
    
        return ax
    
    
        
    def weightedMean(self, ratios, relative_prop_errors):
        """
        Parameters
        ----------
        ratios : list
            vector of ratios.
        relative_prop_errors : list
            vector of relative propagating errors. Matching ratios by index.

        Returns
        -------
        weightedMean : float
            weighted mean of ratios.
        sd : float
            weighted standard deviation of ratios.

        """

        
        if ratios.size == 0:
            return 0 , 0

        # removes zero entries
        nonZeroRatios = []
        nonZero_relative_prop_errors = []
        for i in range(len(ratios)):
            if ratios[i] != 0:
                nonZeroRatios.append(ratios[i])
                nonZero_relative_prop_errors.append(relative_prop_errors[i])
        ratios = nonZeroRatios
        relative_prop_errors = nonZero_relative_prop_errors
        
        if len(ratios) == 1:
            return ratios[0], relative_prop_errors[0]

        numerator = 0
        denominator= 0
        for i in range(len(ratios)):
            weight = (1/relative_prop_errors[i])**2
            numerator += ratios[i]* weight
            denominator += weight
        weightedMean = numerator / denominator
        
        
        for i in range(len(ratios)):
            weight = (1/relative_prop_errors[i])**2
            numerator += weight* (ratios[i] - weightedMean)**2
            denominator += weight

        n = len(ratios)
        variance = numerator / denominator * n / (n - 1)
        sd = math.sqrt(variance/n)
   
        
        return weightedMean, sd
    
    def mean_by_range(self, element_limit):
        
        lim_low_z = element_limit[0]/100 #cm to m
        lim_high_z = element_limit[1]/100
        
        
        xes = self.merged.xcoordinates/100
           
        g = interp1d(xes, self.yesContact)
        f = interp1d(xes, self.yes40cm)
    
        ferrors = interp1d(self.merged.xcoordinates/100, self.yesContactError/100 )
        rel_ratioerrors_contact = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_contact /self.survey.yesContact, ferrors(self.survey.xesContact)))
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors_40cm = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        
        ratiosContact = g(self.survey.xesContact)/self.survey.yesContact
        ratios40cm = f(self.survey.xes40cm)/self.survey.yes40cm
        
        sub_ratiosContact = []
        for i, z in enumerate(self.survey.xesContact):
            if z > lim_low_z and z < lim_high_z:
                sub_ratiosContact.append(ratiosContact[i])
    
        sub_ratios40cm = []
        for i, z in enumerate(self.survey.xes40cm):
            if z > lim_low_z and z < lim_high_z:               
                sub_ratios40cm.append(ratios40cm[i])
        
        sub_ratiosContact = np.array(sub_ratiosContact)
        sub_ratios40cm = np.array(sub_ratios40cm)
        
        sub_weightedMean_contact, sub_sd_contact = self.weightedMean(sub_ratiosContact , rel_ratioerrors_contact)
        sub_weightedMean_40cm, sub_sd_40cm = self.weightedMean(sub_ratios40cm , rel_ratioerrors_40cm)    
        

        
        return sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm
    

    def plot3(self):
        xmin = 20.90
        xmax = 232
        xCut = 89 #155
        matching_start = 139
        ymin = 1E-1
        ymin2 = 2
        
        ymax = 4E3
        
        yratioMin = 0.03
        yratioMin2 = 0.17
        yratioMax = 4
        
        gs = gridspec.GridSpec(200, 1)
        
        stops = [60, 92 , 112,  167]

        
        fig = plt.figure()
        #plt.subplot(311)
        #-----1111111111111111111-------------------------
        ax = plt.subplot(gs[0:stops[0], 0])
        
        

        
        
        xes = self.merged.xcoordinates/100
        
        
        g = interp1d(xes, self.yesContact)
        plt.plot(xes,g(xes) , label = "Fluka contact", color = "C0", linewidth = 2)
        
        # print(type(self.survey.xesContact))
        plt.errorbar(self.survey.xesContact, self.survey.yesContact, yerr = self.AD6_abs_error_contact, label = "Survey contact", marker=".", linestyle= 'None', color = "C0", markersize = 12)
        

        f = interp1d(xes, self.yes40cm)
        plt.plot(xes, f(xes), label = "Fluka 40cm", color = "C1", linewidth = 2)
        plt.errorbar(self.survey.xes40cm, self.survey.yes40cm, yerr = self.AD6_abs_error_40cm , label = "Survey 40 cm", marker=".", linestyle= 'None', color = "C1", markersize = 12)
        
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.20),
          fancybox=True, shadow=True, ncol=5, prop={'size': 12})
        plt.yscale("log")
        plt.ylim(ymin2,ymax)
        plt.xlim(xmin,xCut)
        plt.grid(linewidth= 0.3)
        plt.ylabel("[uSv/h]", fontsize = 12)
        plt.title("Inner Triplet and D1 section" , fontsize = 14)
        
        

        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yesContactError/100 )
        rel_ratioerrors_contact = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_contact /self.survey.yesContact, ferrors(self.survey.xesContact)))
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors_40cm = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        
        
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        #ax.axes.xaxis.set_visible(False)
        
        
        ax2 = ax.twinx()
        ax2 = self.merged.drawGeo_inside_of(ax2 , 0.50, xmax , 100, 0.3, 0.3)
        ax2.set_ylim(-3.50, 0.45)
        ax2.set_xlim(xmin, xCut)
        ax2.axes.yaxis.set_visible(False)

        for key in machine_labels.keys():
            zpos = machine_labels[key][0]/100
            if xmin < zpos < xCut:
                ax2.text(zpos, machine_labels[key][1]/100 , key,
                        color='k', fontsize=12)




        #-----222222222222222222222222222-------------------------
        ax = plt.subplot(gs[stops[0]+1:stops[1], 0])
        
        ratiosContactmerged = g(self.survey.xesContact)/self.survey.yesContact
        ratios1meterMerged = f(self.survey.xes40cm)/self.survey.yes40cm
        
        for element_limit in element_limits.keys():
            if element_limit != "All":
                ax = self.ratios_in_range( ax, element_limits[element_limit][0]/100, element_limits[element_limit][1]/100)
        
        
        
        # weightedMean_contact, sd_contact = self.weightedMean(ratiosContactmerged , rel_ratioerrors_contact)
        # weightedMean_40cm, sd_40cm = self.weightedMean(ratios1meterMerged , rel_ratioerrors_40cm)
        # #print(weightedMean_contact, weightedMean_40cm)
        # # self.mean_by_range([20.90*100, 232*100])
        sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm = self.mean_by_range([0, xmax*1000])

        plt.errorbar(self.survey.xesContact, sub_ratiosContact, yerr = sub_ratiosContact *rel_ratioerrors_contact , label = "Contact Fluka/Measurements" , marker=".", linestyle= 'None', markersize = 12)
        # plt.axhline(y=sub_weightedMean_contact, color='C0', linestyle='-', linewidth = 2, label =  "Contact weighted mean of ratio = {} \u00B1 {}".format( round(sub_weightedMean_contact,4), round(sub_sd_contact,4) ) )
        # rect = plt.Rectangle((-1000, sub_weightedMean_contact - 1*sub_sd_contact),
        #       2000,
        #       2*sub_sd_contact, color = 'C0', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation")
        # plt.gca().add_patch(rect)
        

        plt.errorbar(self.survey.xes40cm, sub_ratios40cm , yerr = sub_ratios40cm *rel_ratioerrors_40cm , label =  "40 cm Fluka/Measurements", marker=".", linestyle= 'None', markersize = 12)
        # plt.axhline(y=sub_weightedMean_40cm, color='C1', linestyle='-', linewidth = 2, label =  "40 cm weighted mean of ratio = {} \u00B1 {}".format( round(sub_weightedMean_40cm,4), round(sub_sd_40cm,4) ) )
        # rect = plt.Rectangle((-1000, sub_weightedMean_40cm - 1*sub_sd_40cm),
        #       2000,
        #       2*sub_sd_40cm, color = 'C1', alpha = 0.1 ,  edgecolor = None)
        # plt.gca().add_patch(rect)
        
        #fake
        # plt.plot([0], [0], label = "Contact Weighted mean =  0.78", color = "C0")
        # plt.plot([0], [0], label = "40 cm Weighted mean = 0.62 ", color = "C1")
        
        plt.plot([0], [0], label = r"Contact Weighted mean$\pm1\sigma$", color = "C0", linewidth = 4)
        plt.plot([0], [0], label = r"40 cm Weighted mean$\pm1\sigma$", color = "C1", linewidth = 4)

       
        
        # rect = plt.Rectangle((0, 0),
        #   0,
        #   0, color = 'C0', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation -  Contact")
        # ax.add_patch(rect)
        
        # rect = plt.Rectangle((0, 0),
        #   0,
        #   0, color = 'C1', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation - 40 cm")
        # ax.add_patch(rect)
        
       
        plt.ylabel("Ratio", fontsize = 12)
        plt.grid(linewidth= 0.3)
        ax.legend(loc='upper center', bbox_to_anchor=(0.25, 0.55),
              fancybox=True, shadow=True, ncol=2, prop={'size': 9})
        
        plt.axhline(y=1, color='k', linestyle='-')
        plt.yscale("log")
        plt.xlabel("z [m from IP]", fontsize = 12)
        plt.xlim(xmin,xCut)
        plt.ylim(yratioMin, yratioMax)
        
        
        
        
        
        xes = self.merged.xcoordinates/100
        g = interp1d(xes, self.yes40cm)

        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors= list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        
        # plt.tick_params(
        #     axis='x',          # changes apply to the x-axis
        #     which='both',      # both major and minor ticks are affected
        #     bottom=False,      # ticks along the bottom edge are off
        #     top=False,         # ticks along the top edge are off
        #     labelbottom=False) # labels along the bottom edge are off
        


        
        
        #-----33333333333333333333333333333333333------------------------
        ax = plt.subplot(gs[stops[2]:stops[3], 0])
        
        # ax.text(3, 8, 'boxed italics text in data coords', style='italic',
        #         bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        
        
        
        xes = self.merged.xcoordinates/100
        
        
        g = interp1d(xes, self.yesContact)
        plt.plot(xes,g(xes) , label = "Fluka contact", color = "C0", linewidth = 2)
        plt.errorbar(self.survey.xesContact, self.survey.yesContact, yerr = self.AD6_abs_error_contact, label = "Survey contact", marker=".", linestyle= 'None', color = "C0", markersize = 12)
        
        # xes = self.merged.xcoordinates/100
        f = interp1d(xes, self.yes40cm)
        plt.plot(xes, f(xes), label = "Fluka 40cm", color = "C1", linewidth = 2)
        plt.errorbar(self.survey.xes40cm, self.survey.yes40cm, yerr = self.AD6_abs_error_40cm , label = "Survey 40 cm", marker=".", linestyle= 'None', color = "C1", markersize = 12)
        
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.32, 0.65),
              fancybox=True, shadow=True, ncol=2, prop={'size': 9})
        
        plt.yscale("log")
        plt.ylim(ymin,ymax)
        plt.xlim(matching_start, xmax)
        plt.grid(linewidth= 0.3)
        plt.ylabel("[uSv/h]", fontsize = 12)
        plt.title("TAN, TCLs, D2 and Matching section" , fontsize = 12)
        
        
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        
        ax2 = ax.twinx()
        ax2 = self.merged.drawGeo_inside_of(ax2 , 0.50, xmax , 100, 0.3, 0.3)
        ax2.set_ylim(-3.50, 0.45)
        ax2.set_xlim(matching_start, xmax)
        ax2.axes.yaxis.set_visible(False)
        
        
        for key in machine_labels.keys():
            zpos = machine_labels[key][0]/100
            if matching_start < zpos < xmax:
                ax2.text(zpos, machine_labels[key][1]/100 , key,
                        color='k', fontsize=12)

        
        #-----444444444444444444444444444444------------------------
        ax = plt.subplot(gs[stops[3]+1:, 0])
        
        ratios1meterMerged = f(self.survey.xes40cm)/self.survey.yes40cm
        
        weightedMean, sd = self.weightedMean(ratios1meterMerged , rel_ratioerrors)
        #sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm = self.mean_by_range([xmin*100, xmax*100])
        
        plt.errorbar(self.survey.xesContact, ratiosContactmerged, yerr = ratiosContactmerged *rel_ratioerrors_contact , label = "Contact Fluka/Measurements" , marker=".", linestyle= 'None', markersize = 12)
        # plt.axhline(y=weightedMean_contact, color='C0', linestyle='-', linewidth = 2, label =  "Contact weighted mean of ratio = {} \u00B1 {}".format( round(weightedMean_contact,4), round(sd_contact,4) ) )
        # rect = plt.Rectangle((-1000, weightedMean_contact - 1*sd_contact),
        #       2000,
        #       2*sd_contact, color = 'C0', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation")
        # plt.gca().add_patch(rect)
        

        plt.errorbar(self.survey.xes40cm, ratios1meterMerged , yerr = ratios1meterMerged *rel_ratioerrors_40cm , label =  "40 cm Fluka/Measurements", marker=".", linestyle= 'None', markersize = 12)
        # plt.axhline(y=weightedMean_40cm, color='C1', linestyle='-', linewidth = 2, label =  "40 cm weighted mean of ratio = {} \u00B1 {}".format( round(weightedMean_40cm,4), round(sd_40cm,4) ) )
        # rect = plt.Rectangle((-1000, weightedMean_40cm - 1*sd_40cm),
        #       2000,
        #       2*sd_40cm, color = 'C1', alpha = 0.1 ,  edgecolor = None)
        # plt.gca().add_patch(rect)

        for element_limit in element_limits.keys():
            if element_limit != "All":
                ax = self.ratios_in_range( ax, element_limits[element_limit][0]/100, element_limits[element_limit][1]/100)
        
        
        plt.plot([0], [0], label = r"Contact Weighted mean$\pm1\sigma$", color = "C0", linewidth = 4)
        plt.plot([0], [0], label = r"40 cm Weighted mean$\pm1\sigma$", color = "C1", linewidth = 4)

        # rect = plt.Rectangle((0, 0),
        #   0,
        #   0, color = 'C0', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation - Contact")
        # ax.add_patch(rect)
        
        # rect = plt.Rectangle((0, 0),
        #   0,
        #   0, color = 'C1', alpha = 0.1 ,  edgecolor = None, label = "1 standard deviation - 40 cm")
        # ax.add_patch(rect)
        
        plt.ylabel("Ratio", fontsize = 12)
        plt.grid(linewidth= 0.3)
        ax.legend(loc='upper center', bbox_to_anchor=(0.65, 1),
              fancybox=True, shadow=True, ncol=2, prop={'size': 8})
        
        plt.axhline(y=1, color='k', linestyle='-')
        plt.yscale("log")
        
        plt.xlim(xmin,xmax)
        plt.xlabel("z [m from IP]", fontsize = 16)
        plt.ylim(yratioMin, yratioMax)
        plt.xlim(matching_start, xmax)
        
        
        
        plt.suptitle(self.title, fontsize = 18)
        xlength = 15
        fig.set_size_inches(xlength, xlength/1.618)
        plt.show()
        try:
            os.chdir(self.path)
            plt.savefig(self.fig_name,  bbox_inches = 'tight', pad_inches = 0.1)
        except:
            pass;

    def print_mean_by_limit(self, element_limits):
        
        for item in list(element_limits.keys()):
            xmin, xmax = element_limits[item]
            sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm = self.mean_by_range( (xmin, xmax))
            print(item , round(sub_weightedMean_contact,2), round(sub_weightedMean_40cm, 2))

    def plot_triplet(self):
        xmin = 20.90
        xmax = 154
        xCut = 56 

    
        ymin = 8
        ymax = 700
        
        yratioMin = 0.08
        yratioMax = 1.35
        
        gs = gridspec.GridSpec(100, 1)
        

        stops = [65, 66, 95]
        
        fig = plt.figure()
        #plt.subplot(311)
        #-----1111111111111111111-------------------------
        ax = plt.subplot(gs[0:stops[0], 0])
        
        
    
        
        
        xes = self.merged.xcoordinates/100
        
        
        g = interp1d(xes, self.yesContact)
        plt.plot(xes,g(xes) , label = "Fluka contact", color = "C0", linewidth = 2)
        plt.errorbar(self.survey.xesContact, self.survey.yesContact, yerr = self.AD6_abs_error_contact, label = "Survey contact", marker=".", linestyle= 'None', color = "C0", markersize = 16)
        
        # xes = self.merged.xcoordinates/100
        f = interp1d(xes, self.yes40cm)
        plt.plot(xes, f(xes), label = "Fluka 40cm", color = "C1", linewidth = 2)
        plt.errorbar(self.survey.xes40cm, self.survey.yes40cm, yerr = self.AD6_abs_error_40cm , label = "Survey 40 cm", marker=".", linestyle= 'None', color = "C1", markersize = 16)
        
        
    
        plt.yscale("log")
        plt.ylim(ymin,ymax)
        plt.xlim(xmin,xCut)
        plt.grid(linewidth= 0.3)
        plt.ylabel(r"Residual $H^{*}(10)$ rates [uSv/h]", fontsize = 20)
        plt.title("Comparison LSS1 IT between FLUKA and measurement", fontsize = 24)

    
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yesContactError/100 )
        rel_ratioerrors_contact = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_contact /self.survey.yesContact, ferrors(self.survey.xesContact)))
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors_40cm = list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        
        
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        
        ax2 = ax.twinx()
        ax2 = self.merged.drawGeo_inside_of(ax2 , 0.43, xmax , 100, 0.05, 0.4)
                                            #(self, ax , yCut, zCut , factor = 1 ,linewidth = 0.5, alpha = 1)
        ax2.set_ylim(-3.50, 0.45)
        ax2.set_xlim(xmin, xCut)
        ax2.axes.yaxis.set_visible(False)
    
        for key in machine_labels.keys():
            zpos = machine_labels[key][0]/100
            if xmin < zpos < xCut:
                ax2.text(zpos, machine_labels[key][1]/100 , key,
                        color='k', fontsize=20)
    
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.12),
              fancybox=True, shadow=True, ncol=5, prop={'size': 15})

        
    
        #-----222222222222222222222222222-------------------------
        ax = plt.subplot(gs[stops[1]:stops[2], 0])
        
        ratiosContactmerged = g(self.survey.xesContact)/self.survey.yesContact
        ratios1meterMerged = f(self.survey.xes40cm)/self.survey.yes40cm
        
        for element_limit in element_limits.keys():
            if element_limit != "All":
                ax = self.ratios_in_range( ax, element_limits[element_limit][0]/100, element_limits[element_limit][1]/100)
        
        
    
        sub_ratiosContact, sub_weightedMean_contact, sub_sd_contact, sub_ratios40cm, sub_weightedMean_40cm, sub_sd_40cm = self.mean_by_range([0, xmax*1000])
    
        plt.errorbar(self.survey.xesContact, sub_ratiosContact, yerr = sub_ratiosContact *rel_ratioerrors_contact  , marker=".", linestyle= 'None', markersize = 16, label = "Contact Fluka/Measurements") #, label = "Fluka/Measurements - Contact"

        
    
        plt.errorbar(self.survey.xes40cm, sub_ratios40cm , yerr = sub_ratios40cm *rel_ratioerrors_40cm , marker=".", linestyle= 'None', markersize = 16, label =  "40 cm Fluka/Measurements") #, label =  "Fluka/Measurements - 40 cm"

        
        plt.plot([0], [0], label = r"Contact Weighted mean =  0.78 $\pm1\sigma$", color = "C0", linewidth = 4)
        plt.plot([0], [0], label = r"40 cm Weighted mean = 0.62 $\pm1\sigma$", color = "C1", linewidth = 4)
    
       
        plt.ylabel("Ratio", fontsize = 22)
        plt.grid(linewidth= 0.3)
    
        plt.axhline(y=1, color='k', linestyle='-')
        plt.yscale("log")
        plt.xlabel("z [m from IP]", fontsize = 24)
        plt.xlim(xmin,xCut)
        plt.ylim(yratioMin, yratioMax)
        
        
        
        xes = self.merged.xcoordinates/100
        g = interp1d(xes, self.yes40cm)
    
        
        ferrors = interp1d(self.merged.xcoordinates/100, self.yes40cmError/100 )
        rel_ratioerrors= list(map(lambda x,y: math.sqrt(x*x + y*y ), self.AD6_abs_error_40cm/self.survey.yes40cm, ferrors(self.survey.xes40cm)))
        
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        
    
        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.55),
              fancybox=True, shadow=True, ncol=2, prop={'size': 15})
        
        
        xlength = 12
        fig.set_size_inches(xlength, xlength/1.61803398875)
        plt.show()
        try:
            plt.savefig("LSS1_triplet.pdf",  bbox_inches = 'tight', pad_inches = 0.2)
        except:
            pass;
    
