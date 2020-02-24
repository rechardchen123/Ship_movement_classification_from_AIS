#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 1/22/2019 11:50 AM
# @Author : Xiang Chen (Richard)
# @File : CNN_structure.py
# @Software: PyCharm
import os
import numpy as np
import pandas as pd
import datetime
import glob

ais_file1 = pd.read_csv(r'C:\Users\LPT-ucesxc0\AIS-Data\Danish_AIS_data_process\test.csv')
delete_base_station = ais_file1[~ ais_file1['Type of mobile'].str.contains('Base Station')]
delete_AtoN = delete_base_station[~ delete_base_station['Type of mobile'].str.contains('AtoN')]
delete_SR = delete_AtoN[~ delete_AtoN['Type of mobile'].str.contains('Search and Rescue Transponder')]

finish_drop = delete_SR.drop(
    columns=['Navigational status', 'ROT', 'IMO','Callsign','Name','Width',
             'Length','Type of position fixing device','Draught','Destination',
             'ETA','Data source type','A','B','C','D','Ship type','Cargo type','Type of mobile','COG'])
finish_drop.rename(columns={finish_drop.columns[0]:"Record_Datetime"},inplace=True)
finish_drop.rename(columns={finish_drop.columns[4]:"Speed"},inplace=True)
#delete the speed and sog is null
finish_drop_null = finish_drop.dropna()
finish_drop_null.reset_index(drop=True,inplace=True)

# groupby the data by MMSI
group_by_mmsi = finish_drop_null.groupby(['MMSI'])
for group in group_by_mmsi:
    group[1].to_csv(str(group[0]) + '.csv', index=False)


