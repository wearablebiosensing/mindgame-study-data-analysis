import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import re
import seaborn as sns
from datetime import datetime
from shutil import move
import plotly.express as px
import pytz
import shutil

####################################################################################################
# HELPER FUNCTIONS TO ORGANIZE TIMESTAMPS.
####################################################################################################

# Function to split file name and get the character
def get_participant_id(file_name):
    print("Participnt ID: ",file_name.split('_')[1])
    return file_name.split('_')[1]
def get_level_id(file_name):
    print("Level ID: ",file_name.split('_')[2])
    return file_name.split('_')[2]
    
def get_session_id(file_name):
    print("Session ID: ",file_name.split('_')[3])
    return file_name.split('_')[3]

def get_timestamp_id(current_timestamp):
    print("current_timestamp(): ",current_timestamp)
    int_time_stamp = int(current_timestamp.split("_")[-2].split(".")[0])
    readable_date_time = datetime.fromtimestamp(int_time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    return readable_date_time

def get_time_id(current_timestamp):
    print("current_timestamp(): ",current_timestamp)
    time_only = current_timestamp.split(" ")[1]
#     readable_date_time = datetime.fromtimestamp(time_only).strftime('%Y-%m-%d %H:%M:%S')
    return time_only
def get_am_pm(timestamp):
    timestamp_new = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    print("get_am_pm(): / ",timestamp_new,timestamp_new.hour)
    # Determine if it's AM or PM
    if timestamp_new.hour < 12:
        period = 'AM'
    else:
        period = 'PM'
    return period
    
def get_dates_id(file_name):
    return file_name.split(" ")[0]

# Function to get filename DF with formatted timestamps, filename information, AM/PM information.
# INPUT: List of files in a folder. 
# For example: csv_files (For levels infor folder format is in .JSON) = ['info_P4_L1_S1_1717642604.json',
#  'info_P1999_L1_S1_1724944552.json',
#  'info_N4_L2_S1_1718247323.json',
#  'info_P3_L5_S2_1718373870.json',
#  'info_N5_L4_S2_1717001443.json',
#  'info_P5_L3_S2_1721660138.json',
#  'info_P5_L6_S3_1721506524.json',
#  'info_N16_L3_S1_1720890704.json',
#  'info_P4_L6_S2_1717704686.json',
#  'info_N12_L3_S2_1719937747.json',
#  'info_P6_L7_S3_1726281344.json',
#  'info_N8_L5_S2_1717084645.json',
#  'info_N20_L4_S2_1722489365.json',
#  'info_N5_L5_S1_1718116251.json',
#  'info_P3_L8_S1_1718578648.json',
#  'info_N6_L3_S2_1718066963.json']
# OUTPUT: A pandas df with formatted timestamps.
# 1718066963 to 2024-06-05 22:56:44
# The pandas df consists of the following 8 column names:
#'Filenames_level_info': info_P4_L1_S1_1717642604.json 
#'participant_id': P4
#'level_id', : L1
#'session_id: S1
#'timestamp_human': 2024-06-05 22:56:44
#'time_only': 22:56:44
#'am_pm', PM or AM
#'dates: 2024-06-05

def get_filename_df_formated_ts(csv_files):
    # Clean the master dataframe.
    df_filename_level_info = pd.DataFrame(csv_files, columns=['Filenames_level_info'])
    # Apply the function to each row and create a new column
    df_filename_level_info['participant_id'] = df_filename_level_info['Filenames_level_info'].apply(get_participant_id)
    df_filename_level_info['level_id'] = df_filename_level_info['Filenames_level_info'].apply(get_level_id)
    df_filename_level_info['session_id'] = df_filename_level_info['Filenames_level_info'].apply(get_session_id)
    df_filename_level_info['timestamp_human'] = df_filename_level_info['Filenames_level_info'].apply(get_timestamp_id)
    df_filename_level_info['time_only'] = df_filename_level_info['timestamp_human'].apply(get_time_id)
    df_filename_level_info['am_pm'] = df_filename_level_info['timestamp_human'].apply(get_am_pm)
    df_filename_level_info['dates'] = df_filename_level_info['timestamp_human'].apply(get_dates_id)
    return df_filename_level_info


# This function assigns session number based on timedifference between two files for each participant. 
# If 10 mins are elapsed then that is counted as one session.
def sort_df_by_date_time(df_filename_level_info):
    # Sorting by the numeric part of participant_id
    df_sorted = df_filename_level_info.sort_values(by=['participant_id', 'timestamp_human'])
    # convert string timestamp to pd.to_datetime timestamp.
    df_sorted['timestamp_human'] = pd.to_datetime(df_sorted['timestamp_human'])
    # Calculate difference in time.
    df_sorted['time_diff'] = df_sorted.groupby('participant_id')['timestamp_human'].diff().dt.total_seconds()
    threshold = 400
    # Identifying new days based on time difference peaks
    df_sorted['new_session'] = df_sorted['time_diff'] > threshold

    # Assigning day numbers
    df_sorted['session_number'] = df_sorted.groupby('participant_id')['new_session'].cumsum() + 1
    return df_sorted

# /data folder. i.e folder with the actual data.
mouse_data_path = "mouse_data"
watch_acc_data_path = "watch_data/accelerometer_data" 
watch_hr_data_path = "watch_data/heartrate_data"
watch_gry_data_path = "watch_data/gyroscope_data"
source_base_dir = '/Volumes/CW_2024/data_dump_mindgame_11-20-2024_Copy/data/watch_data/gyroscope_data'

# /Organized_By_Sessions folder.
target_base_dir = '/Users/shehjarsadhu/Desktop/UniversityOfRhodeIsland/Graduate/WBL/Project_MindGame/MindGame-at-home-study-data/Session_Organized_2/gyroscope_data'  



def reorganise_and_put_in_folders(df_sorted,source_base_dir,target_base_dir):
    # Creating folders for each participant and each day, and moving the files.
    for participant_id in df_sorted['participant_id'].unique():
        participant_dir = os.path.join(target_base_dir, participant_id)
        os.makedirs(participant_dir, exist_ok=True)
        participant_data = df_sorted[df_sorted['participant_id'] == participant_id]
        ## for index, (item1, item2) in enumerate(zip(list1, list2)):
#         print("participant_data DATES: ",participant_data["dates"].unique())
        for session_number in participant_data['session_number'].unique():
            day_data = participant_data[participant_data['session_number'] == session_number]
            print("day_data: ",day_data["am_pm"].unique()[0])
            day_dir = os.path.join(participant_dir, f'Session_{session_number}_{day_data["dates"].unique()[0]}_{day_data["am_pm"].unique()[0]}')
            os.makedirs(day_dir, exist_ok=True)
            print("day_data: ",day_data)
            for filename in day_data['Filenames_level_info']:
                print("filename: ",filename)
                source_path = os.path.join(source_base_dir, filename)
                destination_path = os.path.join(day_dir, filename)
                if os.path.exists(source_path):
                    shutil.copy(source_path, destination_path)
                else:
                    print(f"File not found: {source_path}")

#########################################  RUN MAIN   #############################################

csv_files = [f for f in os.listdir(source_base_dir) if f.endswith('.csv')]
# json_files_level_info = [f for f in os.listdir(dir_root_levels_info) if f.endswith('.json')]


df_filename_level_info = get_filename_df_formated_ts(csv_files)

df_sorted = sort_df_by_date_time(df_filename_level_info)



reorganise_and_put_in_folders(df_sorted, source_base_dir,target_base_dir)


