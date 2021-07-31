#step 1 Compress log information by time

#import necesary libraries
import glob
import pandas as pd

# get data file names
path = r'\\192.168.0.7\ftpdata\logs'

# get data from afc
#path = r'\\192.168.0.200\logs'

#path = r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\fsf\trial_badan_shell_2021\raw'

#stday = '26'
#filenames = glob.glob(path + '\Log'+stday+'*.csv')

filenames = glob.glob(path + '\Log*.csv')

print(filenames)
number = 0
dfs = []
for filename in filenames:
    number = number + 1
    try:
        data1 = pd.read_csv(filename)
        #filetering columns
        ds_Q = data1[['Time', 'Pressure[Bar]', 'DP[Bar]', 'Temperature[C]',
               'Velocity[m/s]', 'Quality',
               'WaterCut[%]', 'Xl', 'WWC[%]', 'ch1[nA]', 'ch2[nA]', 'ch3[nA]',
               'ch4[nA]', 'ch5[nA]','TotWLR[%]', 'TotGOR', 'GVF[%]', 'XLM',
               'Frg_dp_out', 'GasDen[kg/m3]', 'GasVisc[cP]', 'Kappa',
               'LiqDen[kg/m3]', 'LiqVisc[cP]','Qg[m3/s]', 'Ql[m3/s]', 'Qo[m3/s]',
               'Qw[m3/s]', 'QgStd[m3/s]', 'QlStd[m3/s]', 'QoStd[m3/s]', 'QwStd[m3/s]',
               'TotWLR[%]', 'TotGOR', 'GVF[%]'
               ]]

        #adding columns with 24hs rates

        ds_Q.loc[:,"Qg[m3/d]"] = ds_Q.loc[:,"Qg[m3/s]"] * 86400
        ds_Q.loc[:,"Ql[m3/d]"] = ds_Q.loc[:,"Ql[m3/s]"] * 86400
        ds_Q.loc[:,"Qo[m3/d]"] = ds_Q.loc[:,"Qo[m3/s]"] * 86400
        ds_Q.loc[:,"Qw[m3/d]"] = ds_Q.loc[:,"Qw[m3/s]"] * 86400
        ds_Q.loc[:,"QgStd[m3/d]"] = ds_Q.loc[:,"QgStd[m3/s]"] * 86400
        ds_Q.loc[:,"QlStd[m3/d]"] = ds_Q.loc[:,"QlStd[m3/s]"] * 86400
        ds_Q.loc[:,"QoStd[m3/d]"] = ds_Q.loc[:,"QoStd[m3/s]"] * 86400
        ds_Q.loc[:,"QwStd[m3/d]"] = ds_Q.loc[:,"QwStd[m3/s]"] * 86400

        #cleaning columns

        to_drop = ['Qg[m3/s]', 'Ql[m3/s]', 'Qo[m3/s]',
               'Qw[m3/s]', 'QgStd[m3/s]', 'QlStd[m3/s]', 'QoStd[m3/s]', 'QwStd[m3/s]',
               'TotGOR', 'GVF[%]']

        ds_Qf= ds_Q.drop(to_drop, axis=1)

        ds = ds_Qf.copy()

        ds = ds.set_index('Time')

        ds.index = pd.to_datetime(ds.index)

        ds2 = ds.groupby(pd.Grouper(freq='1min')).mean() 
        ds2.head()


        #export in a way to compare 
        ds2.to_csv(path+'\compressed\log'+str(number)+'.csv')

        print('Transformation '+number+' OK, the output file is ready to use')
    except:
            print("Skipped file: ",filename)

# get data file names
path = r'\\192.168.0.7\ftpdata\logs\compressed'

filenames = glob.glob(path + "\*.csv")
print(filenames)

dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename,low_memory=False).assign(filename = filename))

# Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=False,sort=False)

big_frame.to_csv(r"D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\fsf\trial_badan_shell_2021\cleaned\fsf_raw_full.csv", index=False, encoding='utf-8-sig')

print("Final Transformation OK, the output file is ready to use")