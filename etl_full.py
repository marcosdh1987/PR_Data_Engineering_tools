#import necesary libraries
import pandas as pd
import io
import numpy as np
import seaborn as sns
#import earthpy as et

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Use white grid plot background from seaborn
sns.set(font_scale=1.5, style="whitegrid")
import matplotlib.pyplot as plt


#
#data1 = pd.read_csv(r"\\192.168.0.7\3tdata\data_lake\shell_pad11\fsf_raw_full.csv",low_memory=False)
#data2 = pd.read_csv(r"\\192.168.0.7\3tdata\data_lake\shell_pad11\sep_raw_full.csv",low_memory=False)

data1 = pd.read_csv(r"D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\fsf\trial_badan_shell_2021\cleaned\fsf_raw_full.csv",low_memory=False)
data2 = pd.read_csv(r"D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\separator\trial_badan_shell_2021\cleaned\sep_raw_full.csv",low_memory=False)


print("Data Loaded OK")

dsA = data1.copy()
dsB = data2.copy()

dsA['Time'] = pd.to_datetime(dsA['Time'])
dsA['Time_hs'] = dsA['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
dsA = dsA.sort_values('Time')
dsB['Time'] = pd.to_datetime(dsB['DateTime'])
dsB['Time_hs'] = dsB['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
dsB = dsB.sort_values('Time_hs')

print(dsA['Time_hs'].head())
print(dsB['Time_hs'].head())

ds = pd.merge(dsA, dsB, on='Time_hs')
ds.sort_values(by='Time_hs')
ds.drop_duplicates(subset ='Time_hs',keep='first',inplace=True) 

ds['Time_hs'].head(10)

#to define the trial duration
mask = (ds['Time_hs'] > '2021-07-1 06:00:00') & (ds['Time_hs'] <= '2021-12-12 18:00:00')

ds1 = ds.loc[mask]
ds1.head()

#for local record update
ds1.to_csv(r"D:\Dev\dashboards\static\ds\compared_data_full.csv", index=False, encoding='utf-8-sig')

#for test record in onedrive
ds1.to_csv(r"D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\fsf\trial_badan_shell_2021\bi\compared_data_full.csv", index=False, encoding='utf-8-sig')
print('data compared loaded ok, the data is ready to publish')
