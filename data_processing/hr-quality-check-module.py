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
import plotly.graph_objects as go


############################################################
#  HELPER FUNCTIONS.   #
############################################################

def custom_function(timestamp_string):
    #print("custom_function timestamp_string: ",timestamp_string.split(" ")[1],"\n")
    return timestamp_string.split(" ")[1]

#"04:42:43.358"
def format_ts_seconds(timestamp_str):
    #print("format_ts_seconds ():/  timestamp_str: ",timestamp_str,timestamp_str.split(".")[0])
    return timestamp_str.split(".")[0]



def extract_and_convert(x):
    try:
        return int(x.split("_")[1]) #int(x[1])
    except (IndexError, ValueError):
        return None  # or any default value you prefer.

############################################################
#  HELPER FUNCTIONS.   #
############################################################

# to check the correctness of the data.
def percentage_zeros_hr(df_hr):
    # Count the total number of zeros
    total_zeros = (df_hr == 0).sum().sum()
    # Count the total number of elements
    total_elements = df_hr.size
    # Calculate the percentage of zeros
    percentage_zeros = (total_zeros / total_elements) * 100
    return percentage_zeros

def snr_hr(df_hr):
    return df_hr["bpm"].mean()/df_hr["bpm"].std()

def percentage_missing_hr(df):
    # Create DataFrame
    df = pd.DataFrame(df)
    # Convert watch_timestamp to datetime
    df['watch_timestamp'] = pd.to_datetime(df['watch_timestamp'])
    # Generate a complete time index.
    start_time = df.iloc[0]["watch_timestamp"] #df['watch_timestamp'].min()
    end_time = df.iloc[-1]["watch_timestamp"] #df['watch_timestamp'].max()
    print("start_time,end_time: ",start_time,end_time)
    full_time_index = pd.date_range(start=start_time, end=end_time, freq='1S')
    print("df: ",df.shape[0],"len(full_time_index): ",len(full_time_index))
    expected_number_of_samples = len(full_time_index)
    recieved_number_of_samples = df.shape[0]
    percentage_missing=  ((expected_number_of_samples-recieved_number_of_samples)/expected_number_of_samples)*100
    print("Percentage of missing data: ", percentage_missing)
    return percentage_missing