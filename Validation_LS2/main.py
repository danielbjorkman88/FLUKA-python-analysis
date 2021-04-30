# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:06:16 2021

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
from PointAnalysis import pointAnalysis
from multi_fluka import multi_fluka
from SupportInfo import *
from scipy.interpolate import interp1d
import math as math
import matplotlib.gridspec as gridspec
import datetime 


#LS2 = datetime.datetime(2018,10,23,13,22,00)
measurementDate1 = datetime.datetime(2018, 12, 3)
measurementDate2 = datetime.datetime(2019, 1, 8)
days_first = (measurementDate1 - LS2).total_seconds()/(60*60*24)
days_second = (measurementDate2 - LS2).total_seconds()/(60*60*24)











origo_ip1 = 0 # Machine longitudian z or S coordinate

# Survey 3/12/2018
filenameSurvey = "Survey_UJ16_ir1_03122018.txt"
comparison1 = multi_fluka(["USRBIN_3122018_2017cont", "USRBIN_3122018_2018cont"], path)
comparison1.set_survey(filenameSurvey, path, origo_ip1)
comparison1.set_sampling_path(sampling_path)
comparison1.survey.dataFromFile(["Contact_Survey_UJ16_ir1_03122018.npy", "40cm_Survey_UJ16_ir1_03122018.npy"])
comparison1.valuesofpath()
comparison1.set_AD6_errors(0.3)
comparison1.result.loadGeometryFile( "horizontal.dat",path_drawings)
comparison1.highlight_path()
comparison1.title = "LSS1 Fluka to measurement comparison after {} days cool down after Run 2 p-p".format(round(days_first))
comparison1.fig_name = "SurveyValidation03122018_IR1.pdf"
comparison1.plot_full()
comparison1.plot_triplet()
comparison1.print_mean_by_limit(element_limits)



#Survey 8/01/2019
filenameSurvey = "Survey_UJ16_ir1_08012019.txt"
comparison2 = multi_fluka(["USRBIN_08012019_2017cont", "USRBIN_08012019_2018cont"], path)
comparison2.set_survey(filenameSurvey, path, origo_ip1)
comparison2.set_sampling_path(sampling_path)
comparison2.survey.dataFromFile(["Contact_Survey_UJ16_ir1_08012019.npy", "40cm_Survey_UJ16_ir1_08012019.npy"])
comparison2.valuesofpath()
comparison2.set_AD6_errors(0.3)
comparison2.result.loadGeometryFile( "horizontal.dat",path_drawings)
#comparison2.highlight_path()
comparison2.title = "LSS1 Fluka to measurement comparison after {} days cool down after Run 2 p-p".format(round(days_second))
comparison2.fig_name = "SurveyValidation08012019_IR1.pdf"
comparison2.plot_full()
comparison2.plot_triplet()
comparison2.print_mean_by_limit(element_limits)



# # # # # #-----Point 5 ----------------------------------------------------------------------------------------------------


# survey = "Survey 3/12/2018"
filenameSurvey = "Survey_ir5_03122018.txt"
comparison3 = multi_fluka(["ir5_3122018_2017cont", "ir5_3122018_2018cont"], path)
comparison3.set_survey(filenameSurvey, path, origo_ip5)
comparison3.set_sampling_path(sampling_path)
comparison3.survey.dataFromFile(["Contact_Survey_ir5_03122018.npy", "40cm_Survey_ir5_03122018.npy"])
comparison3.valuesofpath()
comparison3.set_AD6_errors(0.3)
comparison3.result.loadGeometryFile( "horizontal.dat",path_drawings)
#comparison3.highlight_path()
comparison3.title = "LSS5 Fluka to measurement comparison after {} days cool down after Run 2 p-p".format(round(days_first))
comparison3.fig_name = "SurveyValidation03122018_IR5.pdf"
comparison3.plot_full()
comparison3.plot_triplet()
comparison3.print_mean_by_limit(element_limits)




# survey = "Survey 8/01/2019"
filenameSurvey = "Survey_ir5_08122019.txt"
comparison4 = multi_fluka(["ir5_08012019_2017cont", "ir5_08012019_2018cont"], path)
comparison4.set_survey(filenameSurvey, path, origo_ip5)
comparison4.set_sampling_path(sampling_path)
comparison4.survey.dataFromFile(["Contact_Survey_ir5_08012019.npy", "40cm_Survey_ir5_08012019.npy"])
comparison4.setup()
comparison4.valuesofpath()
comparison4.set_AD6_errors(0.3)
comparison4.result.loadGeometryFile( "horizontal.dat",path_drawings)
#comparison4.highlight_path()
comparison4.title = "LSS5 Fluka to measurement comparison after {} days cool down after Run 2 p-p".format(round(days_second))
comparison4.fig_name = "SurveyValidation08012019_IR5.pdf"
comparison4.plot_full()
comparison4.plot_triplet()
comparison4.print_mean_by_limit(element_limits)








# comparisons = [comparison1, comparison2, comparison3, comparison4]
# #comparisons = [comparison1]

# n_datapoints = 0
# for comparison in comparisons:

    
#     n_datapoints += len(comparison.survey.doseRateContact) + len(comparison.survey.doseRate1meter)
    


#     comparison.print_mean_by_limit(comparison, element_limits)
    

#     comparison.plot_full()


#     print(" ")



# print(n_datapoints, "n data points")

