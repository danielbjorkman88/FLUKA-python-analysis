# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:57:08 2020

@author: dbjorkma
"""

# -*- coding: utf-8 -*-
"""
Imperative programming solution for reading, writing, plotting and other 
operations related to FLUKA irradiation profiles of the LHC and its 
corresponding experiments.
By Daniel Björkman 2018 - 2021
daniel.bjorkman@cern.ch
"""


from irrprofi_functionlibrary import *
import pickle


origo = LS3
experiment_name = 'ATLAS'
title = "LHC LSS1 and ATLAS irradiation profile up to Run 3 p-p"
ATLAS_profile = readProfile('ATLAS_profile.inp')
lumi = pickle.load(open("lumi_ATLAS",'rb'))





config = {}
config["origo"] = origo
config["experiment_name"] = experiment_name
config["title"] = title
config["lumi"] = lumi
config["output_filename"] = 'AtlasIrradiationProfileLS3.inp'


plot(ATLAS_profile, config) 
writeProfile(ATLAS_profile, config["output_filename"] )



