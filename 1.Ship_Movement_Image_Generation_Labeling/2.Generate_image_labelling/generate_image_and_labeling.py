#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 1/22/2019 11:50 AM
# @Author : Xiang Chen (Richard)
# @File : CNN_structure.py
# @Software: PyCharm
import os
import pandas as pd
import glob
import math
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') #In local debugging, it should comment it and uploading to remote server, should use this.
from shutil import copyfile

working_directory = '/home/ucesxc0/Scratch/output/process_ais_data_Danish/ais_danish_201809_2'
file_names = glob.glob(working_directory + '/*.csv')

def delete_small_size_file(size):
    files = os.listdir(os.getcwd())
    for file in files:
        if file.endswith('.csv'):
            if os.path.getsize(file) < size * 1024:
                os.remove(file)
                print(file + " was deleted.")
    return

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


def CropImage2File(filepath, destpath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join(filepath, allDir)
        dest = os.path.join(destpath, allDir)
        if os.path.isfile(child):
            image = cv2.imread(child)
            #define the clipping area
            a = 60
            b = 420
            c = 80
            d = 570
            cropImg = image[a:b, c:d]
            #resize the image
            after_clip_size = cropImg.shape
            dstHeight = int(after_clip_size[0] * 0.7)
            dstWidth = int(after_clip_size[1] * 0.7)
            dst = cv2.resize(cropImg, (dstWidth, dstHeight))
            cv2.imwrite(dest, dst)

for file_name in file_names:
    directory_name = os.path.splitext(file_name)[0]
    os.mkdir(directory_name)
    ais_file1 = pd.read_csv(file_name)
    delete_base_station = ais_file1[~ ais_file1['Type of mobile'].str.contains('Base Station')]
    delete_AtoN = delete_base_station[~ delete_base_station['Type of mobile'].str.contains('AtoN')]
    delete_SR = delete_AtoN[~ delete_AtoN['Type of mobile'].str.contains('Search and Rescue Transponder')]

    finish_drop = delete_SR.drop(
        columns=['Navigational status', 'ROT', 'IMO', 'Callsign', 'Name', 'Width',
                 'Length', 'Type of position fixing device', 'Draught', 'Destination',
                 'ETA', 'Data source type', 'A', 'B', 'C', 'D', 'Ship type', 'Cargo type', 'Type of mobile', 'COG'])
    finish_drop.rename(columns={finish_drop.columns[0]: "Record_Datetime"}, inplace=True)
    finish_drop.rename(columns={finish_drop.columns[4]: "Speed"}, inplace=True)

    # delete the speed and sog is null
    finish_drop_null = finish_drop.dropna()
    finish_drop_null.reset_index(drop=True, inplace=True)

    # groupby the data by MMSI
    group_by_mmsi = finish_drop_null.groupby(['MMSI'])
    for group in group_by_mmsi:
        group[1].to_csv(directory_name +'/%s.csv' % (str(group[0])), index=False)

    # delete the small size data
    os.chdir(directory_name)
    delete_small_size_file(30)

    #print(os.getcwd())
    # groupby MMSI per day
    address = os.getcwd()
    path = os.path.join(address, 'groupby_mmsi_per_day')
    os.mkdir(path)
    file_names_1 = glob.glob('*.csv')
    #print(file_names_1)
    for f in file_names_1:
        read_file = pd.read_csv(f)
        read_file['Record_Datetime'] = pd.to_datetime(read_file['Record_Datetime'], format='%d/%m/%Y %H:%M:%S')
        read_file['Day'] = pd.to_datetime(read_file['Record_Datetime']).dt.day
        read_file['Hour'] = (pd.to_datetime(read_file['Record_Datetime']).dt.hour).apply(lambda x: x * 3600)
        read_file['Minute'] = (pd.to_datetime(read_file['Record_Datetime']).dt.minute).apply(lambda x: x * 60)
        read_file['Seconds'] = pd.to_datetime(read_file['Record_Datetime']).dt.second
        read_file['time_to_seconds'] = read_file['Hour'] + read_file['Minute'] + read_file['Seconds']
        after_process_read_file = read_file.drop(columns=['Record_Datetime', 'Hour', 'Minute', 'Seconds'])
        group_by_day = after_process_read_file.groupby(after_process_read_file['Day'])
        name = int(after_process_read_file.iloc[0]['MMSI'])
        for group in group_by_day:
            group[1].to_csv('groupby_mmsi_per_day/%s-%s.csv' % (
            str(name), str(group[0])), index=False)

    # calculate the dela time, speed and headings
    os.chdir(path)
    delete_small_size_file(20)
    #print(os.getcwd())
    address1 = os.getcwd()
    path1 = os.path.join(address1, 'delta_time_delta_speed')
    os.mkdir(path1)
    file_names_2 = glob.glob('*.csv')
    #print(file_names_2)
    threshold_heading_max_value = 20
    for file_1 in file_names_2:
        file_load = pd.read_csv(file_1)
        MMSI_list = list(file_load['MMSI'])
        Longitude_list = ['{:.3f}'.format(i) for i in list(file_load['Longitude'])]
        Latitude_list = ['{:.3f}'.format(i) for i in list(file_load['Latitude'])]
        Speed_list = list(file_load['Speed'])
        Heading_list = list(file_load['Heading'])
        Day_list = list(file_load['Day'])
        time_to_seconds_list = list(file_load['time_to_seconds'])
        # calculate the delta time and delta speed
        delta_time = compute_time_difference(time_to_seconds_list)
        delta_speed = compute_speed_difference(Speed_list)
        delta_heading = compute_heading_difference(Heading_list)
        # save the files
        save_dict = {'MMSI': MMSI_list,
                     'Longitude': Longitude_list,
                     'Latitude': Latitude_list,
                     'Speed': Speed_list,
                     'Heading': Heading_list,
                     'Day': Day_list,
                     'time_to_seconds': time_to_seconds_list,
                     'delta_time': delta_time,
                     'delta_speed': delta_speed,
                     'delta_heading': delta_heading}
        data = pd.DataFrame(save_dict)
        # output the file
        name_mmsi = int(data.iloc[0]['MMSI'])
        name_day = int(data.iloc[0]['Day'])
        data.to_csv('delta_time_delta_speed/%d-%d.csv' % (name_mmsi, name_day), index=False)

    # split the abnormal data per day
    os.chdir(path1)
    address2 = os.getcwd()
    path2 = os.path.join(address2, 'split_abnormal_data')
    os.mkdir(path2)
    file_names_3 = glob.glob('*.csv')
    for file_3 in file_names_3:
        file_load = pd.read_csv(file_3)
        delta_heading = list(file_load['delta_heading'])
        # find the abnormal trajectory points in the whole trajectory file.
        index_split = file_load[file_load.delta_heading >= threshold_heading_max_value].index.tolist()
        if len(index_split) >= 1:
            # after that, add the starting point and ending point into the split list.
            index_split.insert(0, 0)
            index_split.append(len(delta_heading))
            for i in range(0, len(index_split) - 1):
                new_file = file_load.iloc[index_split[i]:index_split[i + 1]]
                current_position = i
                name_mmsi = int(new_file.iloc[0]['MMSI'])
                name_day = int(new_file.iloc[0]['Day'])
                new_file.to_csv('split_abnormal_data/%d-%d-%d.csv' % (name_mmsi, name_day, current_position), index=False)
        else:
            # output the file that cannot process
            name_mmsi = int(file_load.iloc[0]['MMSI'])
            name_day = int(file_load.iloc[0]['Day'])
            file_load.to_csv('split_abnormal_data/%d-%d.csv' % (name_mmsi, name_day), index=False)

    #generate the trajectory images
    os.chdir(path2)
    address3 = os.getcwd()
    path3 = os.path.join(address3, 'trajectory_images')
    os.mkdir(path3)
    file_names_4 = glob.glob('*.csv')
    for file_4 in file_names_4:
        file_load = pd.read_csv(file_4)
        file_name = os.path.split(file_4)[-1]
        file_name_1 = os.path.splitext(file_name)[0]
        # get a trajectory list and transfer to array
        name_mmsi = int(file_load.iloc[0]['MMSI'])
        longitude_list = list(file_load['Longitude'])
        latitude_list = list(file_load['Latitude'])
        speed_list = list(file_load['Speed'])
        heading_list = list(file_load['Heading'])
        name_day = int(file_load.iloc[0]['Day'])
        delta_time_list = list(file_load['delta_time'])
        delta_speed_list = list(file_load['delta_speed'])
        delta_heading_list = list(file_load['delta_heading'])
        # the data for plot
        trajectory_lat_long_speed_heading_delta_time_speed_heading_dict = {
            'latitude': latitude_list,
            'longitude': longitude_list,
            'speed': speed_list,
            'heading': heading_list,
            'delta_time': delta_time_list,
            'delta_speed': delta_speed_list,
            'delta_heading': delta_heading_list}
        plot_trajectory_dataframe = pd.DataFrame(trajectory_lat_long_speed_heading_delta_time_speed_heading_dict)
        speed_threshold = 2.0
        delta_heading_threshold = 8
        # get the deviation
        speed_deviation = plot_trajectory_dataframe['speed'].std()
        delta_heading_max = plot_trajectory_dataframe['delta_heading'].max()
        # loop for the file
        for i in range(1, len(plot_trajectory_dataframe)):
            if plot_trajectory_dataframe.iloc[i]['speed'] <= speed_threshold:
                plt.plot(plot_trajectory_dataframe.iloc[i]['latitude'],
                         plot_trajectory_dataframe.iloc[i]['longitude'],
                         color='red', marker='s', markersize=15)  # berthing or anchorage
            else:
                if plot_trajectory_dataframe.iloc[i]['delta_heading'] <= delta_heading_threshold:
                    plt.plot(plot_trajectory_dataframe.iloc[i]['latitude'],
                             plot_trajectory_dataframe.iloc[i]['longitude'],
                             color='green', marker='s', markersize=15)  # normal navigation
                else:
                    plt.plot(plot_trajectory_dataframe.iloc[i]['latitude'],
                             plot_trajectory_dataframe.iloc[i]['longitude'],
                             color='blue', marker='s', markersize=15)  # maneuvring operation
        # label for the trajectory image
        if speed_deviation < 2.0:
            name_label_static = 0
            plt.savefig('trajectory_images/%s-%d.jpg' % (
                file_name_1, name_label_static))
            plt.close('all')
            f = open('trajectory_images/label.txt', 'a')
            f.write(file_name_1 + '-' + str(name_label_static) + '.jpg' + ',' + '1' + ',' + '-1' + ',' + '-1' + '\r\n')
            f.close()
        elif delta_heading_max <= delta_heading_threshold:
            name_label_normal_navigation = '0-1'
            plt.savefig('trajectory_images/%s-%s.jpg' % (
                file_name_1, name_label_normal_navigation))
            plt.close('all')
            f = open('trajectory_images/label.txt', 'a')
            f.write(
                file_name_1 + '-' + name_label_normal_navigation + '.jpg' + ',' + '1' + ',' + '1' + ',' + '-1' + '\r\n')
            f.close()
        else:
            name_label_maneuvring = '0-1-2'
            plt.savefig('trajectory_images/%s-%s.jpg' % (
                file_name_1, name_label_maneuvring))
            plt.close('all')
            f = open('trajectory_images/label.txt', 'a')
            f.write(file_name_1 + '-' + name_label_maneuvring + '.jpg' + ',' + '1' + ',' + '1' + ',' + '1' + '\r\n')
            f.close()

    # clip the images and get the final results
    os.chdir(path3)
    address4 = os.getcwd()
    path4 = os.path.join(address4, 'croped_images')
    os.mkdir(path4)
    CropImage2File(path3, path4)
    #copy the label files into the cropped images directory
    copyfile('label.txt', path4)

