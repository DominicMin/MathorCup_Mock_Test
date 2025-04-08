import numpy as np
import pandas as pd
import data_proc
from datetime import datetime

tensors = {"2021": data_proc.tensor_2021, 
           "2022": data_proc.tensor_2022,}

def main():
    print("[PROMPT]Please enter the date in format like \'20210101_DC3_DC5\'.")
    while True:
        raw_input = input("[INPUT]>> ")
        cons = raw_input.split('_')

        if len(cons) == 3:
            #date process
            date = cons[0]
            year, month, day = date[:4], date[4:6], date[6:]
            date = year + '-' + month + '-' + day
            day_idx = datetime.strptime(date, "%Y-%m-%d").timetuple().tm_yday - 1

            #site process
            i = int(cons[1][2:]) - 1
            j = int(cons[2][2:]) - 1
            
            print(f"[INFO]The shipment volume of {cons[1]} to {cons[2]} at {date}: {tensors[year][day_idx, i, j]}")
        else:
            print("[ERROR]Invalid input!")

if __name__ == "__main__":
    main()
        
    