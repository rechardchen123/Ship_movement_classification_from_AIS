#!/usr/bin/env python3
# _*_coding:utf-8 _*_
# @Time    :Created on Dec 04 4:39 PM 2018
# @Author  :xiang chen

import os,sys
import numpy as np
import pandas as pd
import glob
import math

def compute_time_difference(time_to_seconds_list):
    '''calculate the delta time
    Input: time_to_seconds_list.
    Output: new list for store delta time.'''
    save_time_difference = []
    for i in range(0, len(time_to_seconds_list) - 1):
        save_time_difference.append(abs(time_to_seconds_list[i + 1] - time_to_seconds_list[i]))
    save_time_difference.insert(0, 0)
    return save_time_difference

def compute_speed_difference(Speed_list):
    '''Calculate the delta speed.
    Input: Speed_list
    Output: new list for store delta speed.'''
    save_speed_difference = []
    for i in range(0, len(Speed_list) - 1):
        difference = math.fabs(Speed_list[i + 1] - Speed_list[i])
        save_speed_difference.append(difference)
    save_speed_difference.insert(0, 0.0)
    save_speed_difference1 = [round(j, 2) for j in save_speed_difference]
    return save_speed_difference1

def compute_heading_difference(Heading_list):
    '''Calculate the delta speed.
        Input: Heading_list
        Output: new list for store delta heading.'''
    save_heading_difference = []
    for i in range(0,len(Heading_list)-1):
        difference = math.fabs(Heading_list[i+1]-Heading_list[i])
        save_heading_difference.append(difference)
    save_heading_difference.insert(0,0)
    return save_heading_difference

def save_data_into_file(MMSI_list,
                        Longitude_list,
                        Latitude_list,
                        Speed_list,
                        Heading_list,
                        Day_list,
                        time_to_seconds_list,
                        delta_time,
                        delta_speed,
                        delta_heading):
    '''This function is for storing the data and outputing the data into a file.'''
    # dictionary for storing the list and transfer it to dataframe
    save_dict = {'MMSI':MMSI_list,
                 'Longitude':Longitude_list,
                 'Latitude':Latitude_list,
                 'Speed':Speed_list,
                 'Heading':Heading_list,
                 'Day':Day_list,
                 'time_to_seconds':time_to_seconds_list,
                 'delta_time':delta_time,
                 'delta_speed':delta_speed,
                 'delta_heading':delta_heading}
    data = pd.DataFrame(save_dict)
    # output the file
    name_mmsi = int(data.iloc[0]['MMSI'])
    name_day = int(data.iloc[0]['Day'])
    data.to_csv(r'C:\Users\LPT-ucesxc0\AIS-Data\Danish_AIS_data_process\aisdk_20180901\%d-%d.csv' % (name_mmsi, name_day),
                index=False)

file_names = glob.glob(r"C:\Users\LPT-ucesxc0\AIS-Data\Danish_AIS_data_process\aisdk_20180901\test\*.csv")
threshold_heading_max_value = 20
for file in file_names:
    file_load = pd.read_csv(file)
    file_load['Timestamp']=pd.to_datetime(file_load['Timestamp'], format='%d/%m/%Y %H:%M:%S')
    file_load['Day'] = pd.to_datetime(file_load['Timestamp']).dt.day
    file_load['Hour'] = (pd.to_datetime(file_load['Timestamp']).dt.hour).apply(lambda x:x*3600)
    file_load['Minute'] = (pd.to_datetime(file_load['Timestamp']).dt.minute).apply(lambda x:x*60)
    file_load['Seconds'] = pd.to_datetime(file_load['Timestamp']).dt.second
    file_load['time_to_seconds'] = file_load['Hour'] + file_load['Minute'] + file_load['Seconds']
    after_process_read_file = file_load.drop(columns=['Timestamp','Hour','Minute','Seconds'])

    MMSI_list = list(after_process_read_file['MMSI'])
    Longitude_list = ['{:.3f}'.format(i) for i in list(after_process_read_file['Longitude'])]
    Latitude_list = ['{:.3f}'.format(i) for i in list(after_process_read_file['Latitude'])]
    Speed_list = list(after_process_read_file['Speed'])
    Heading_list = list(after_process_read_file['Heading'])
    Day_list = list(after_process_read_file['Day'])
    time_to_seconds_list = list(after_process_read_file['time_to_seconds'])
    # calculate the delta time and delta speed
    delta_time = compute_time_difference(time_to_seconds_list)
    delta_speed = compute_speed_difference(Speed_list)
    delta_heading = compute_heading_difference(Heading_list)
    save_data_into_file(MMSI_list,Longitude_list,Latitude_list,Speed_list,Heading_list,Day_list,
                        time_to_seconds_list,delta_time,delta_speed,delta_heading)


