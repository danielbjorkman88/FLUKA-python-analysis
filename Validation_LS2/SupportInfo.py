# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:01:33 2020

@author: dbjorkma
"""


sampling_path = []
# (start, binnumber, end)
sampling_path.append((0,104, 5490))
sampling_path.append((5490,145,5940))
sampling_path.append((5940,109,8460))
sampling_path.append((8460,138,14024))
sampling_path.append((14024,94,14450 ))
sampling_path.append((14450,136,15255 ))
sampling_path.append((15255,104, 17230))
sampling_path.append((17230,135, 18600))
sampling_path.append((18600,96, 19090))
sampling_path.append((19090,135, 19260))
sampling_path.append((19260,104, 20000))
sampling_path.append((20000,135, 22455))
sampling_path.append((22455,104, 23180))
sampling_path.append((23180,135, 25880))
sampling_path.append((25880,104, 100000))




start = 'Dcum Start S'
mid = 'Dcum Mid S'
end = 'Dcum End S' 


position_corrections_ir1 = {}
item = "LQXAA.1R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][end] = 3005 / 100
item = "LQXBA.2R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][start] = 3193 / 100
position_corrections_ir1[item][end] = 4417 / 100

item = "LQXAG.3R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][start] = 4683 / 100

item = "QQQI.2R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][mid] = 3101 / 100


item = "QQQI.3R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][mid] = 4530 / 100


item = "QQDI.3R1"
position_corrections_ir1[item] = {}
position_corrections_ir1[item][mid] = 5580 / 100



origo_ip5 = 13349.5066 - 20.012
position_corrections_ir5 = {}
item = "LQXAA.1R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][end] = 3005 / 100 + origo_ip5
item = "LQXBA.2R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][start] = 3193 / 100 + origo_ip5
position_corrections_ir5[item][end] = 4417 / 100 + origo_ip5

item = "LQXAG.3R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][start] = 4683 / 100 + origo_ip5

item = "QQQI.2R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][mid] = 3101 / 100 + origo_ip5


item = "QQQI.3R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][mid] = 4530 / 100 + origo_ip5


item = "QQDI.3R5"
position_corrections_ir5[item] = {}
position_corrections_ir5[item][mid] = 5580 / 100 + origo_ip5



