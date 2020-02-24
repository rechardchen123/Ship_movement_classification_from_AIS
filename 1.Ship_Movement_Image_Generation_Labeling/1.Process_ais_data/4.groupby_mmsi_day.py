#!/usr/bin/env python3 
# -*- coding: utf-8 -*
import os, sys
import glob
import pandas as pd
import matplotlib
import time
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

#pd.set_option('display.max_columns', None)  # 读取的数据显示全部的列，不缺省显示
#pd.set_option('display.max_rows', None)

#read files in the directory
file_names = glob.glob(r"C:\Users\LPT-ucesxc0\AIS-Data\Danish_AIS_data_process\aisdk_20180901\test\*.csv")

# loop for the files
for f in file_names:
    read_file = pd.read_csv(f)
    read_file['Timestamp']=pd.to_datetime(read_file['Timestamp'], format='%d/%m/%Y %H:%M:%S')
    print(read_file)
    read_file['Day'] = pd.to_datetime(read_file['Timestamp']).dt.day
    read_file['Hour'] = (pd.to_datetime(read_file['Timestamp']).dt.hour).apply(lambda x:x*3600)
    read_file['Minute'] = (pd.to_datetime(read_file['Timestamp']).dt.minute).apply(lambda x:x*60)
    read_file['Seconds'] = pd.to_datetime(read_file['Timestamp']).dt.second
    read_file['time_to_seconds'] = read_file['Hour'] + read_file['Minute'] + read_file['Seconds']
    #删除以上的时分秒数据:
    after_process_read_file = read_file.drop(columns=['Timestamp','Hour','Minute','Seconds'])
    # 根据天数将同一个MMSI文件按照天数分开，按照MMSI-Day的格式生成文件
    group_by_day = after_process_read_file.groupby(after_process_read_file['Day'])
    name = int(after_process_read_file.iloc[0]['MMSI'])
    for group in group_by_day:
        group[1].to_csv(str(name)+'-'+str(group[0])+'.csv', index=False)








