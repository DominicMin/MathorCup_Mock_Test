import numpy as np
import pandas as pd

'''
This is a Python file for processing historical logistics cargo data. 
The program divides the raw data into 2021 and 2022, storing them in two tensors named tensor_2021 and tensor_2022. 
Each tensor contains 365 matrices, corresponding to the 365 days of the year. 
The usage of the tensor is as follows: 
    the tensor has three indices: day_idx, i, and j. 
    "day_idx" represents the day of the year, ranging from 0 to 364. 
    "i" represents the starting station, and "j" represents the destination station, with station indices ranging from 0 to 80, corresponding to DC1 - DC81. 
    You can access the data for the day_idx-th day of 2021 from station i to station j using tensor_2021[day_idx, i, j].
'''

#raw data
raw = pd.read_excel("data.xlsx")

#max stations (DC1 - DC81)
N = 81

#set of valid routes, length = 1049
valid_routes = set(zip(raw["场地1"], raw["场地2"])) 

#raw data preparation
new = raw.copy()
new["日期"] = new["日期"].dt.year * 1000 + new["日期"].dt.dayofyear
new.columns = ['site_from', 'site_to', 'date_code', 'shipment_volume']

#tensor of 2021 and 2022 (NaN -> no connection)
tensor_2021 = np.full((365, N, N), np.nan)
tensor_2022 = np.full((365, N, N), np.nan)

#generate tensors
for _, row in new.iterrows():
    year = row["date_code"] // 1000
    day_idx = row["date_code"] % 1000 - 1
    i = int(row["site_from"][2:]) - 1
    j = int(row["site_to"][2:]) - 1
    vol = row["shipment_volume"]

    if year == 2021:
        if np.isnan(tensor_2021[day_idx, i, j]):
            tensor_2021[day_idx, i, j] = 0
        tensor_2021[day_idx, i, j] += vol
    elif year == 2022:
        if np.isnan(tensor_2022[day_idx, i, j]):
            tensor_2022[day_idx, i, j] = 0
        tensor_2022[day_idx, i, j] += vol


