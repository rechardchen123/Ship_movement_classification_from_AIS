#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 12/18/2018 4:12 PM 
# @Author : Xiang Chen (Richard)
# @File : split_abnormal_ais_per_day.py 
# @Software: PyCharm
import glob
import pandas as pd
"""
The split_abnorma_ais_per_day is used to split the AIS data per day. Due to the AIS devices uneven sampling
Phenomena, using this function can split the abnormal trajectory. Before doing this, I calculate the
delta_heading. If the delta_heading is abnormal, it should be split from the same day AIS trajectory file.
Here, the threshold value of delta_heading is 20. It refers to the navigational maneuvring knowledge.
"""
def save_data_into_file(new_file, current_position):
    """
    This function is used to save the split files.
    """
    name_mmsi = int(new_file.iloc[0]['MMSI'])
    name_day = int(new_file.iloc[0]['Day'])
    new_file.to_csv('/home/ucesxc0/Scratch/output/split_abnormal_ais_trajectory_per_day/result/%d-%d-%d.csv'%(name_mmsi,name_day,current_position),index=False)

# read the files
file_address = glob.glob('/home/ucesxc0/Scratch/output/split_abnormal_ais_trajectory_per_day/AIS_trajectory_include_delta_time_speed_heading/*.csv')
threshold_heading_max_value = 20
for file in file_address:
    file_load = pd.read_csv(file)
    delta_heading = list(file_load['delta_heading'])
    # find the abnormal trajectory points in the whole trajectory file.
    index_split = file_load[file_load.delta_heading >= threshold_heading_max_value].index.tolist()
    if len(index_split) >= 1:
        #after that, add the starting point and ending point into the split list.
        index_split.insert(0, 0)
        index_split.append(len(delta_heading))
        for i in range(0, len(index_split) - 1):
            new_file = file_load.iloc[index_split[i]:index_split[i + 1]]
            current_position = i
            save_data_into_file(new_file, current_position)
    else:
        # output the file that cannot process
        name_mmsi = int(file_load.iloc[0]['MMSI'])
        name_day = int(file_load.iloc[0]['Day'])
        file_load.to_csv('/home/ucesxc0/Scratch/output/split_abnormal_ais_trajectory_per_day/result/%d-%d.csv'%(name_mmsi,name_day),index=False)
