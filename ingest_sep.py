#step 2 data ingest from separator data

import pandas as pd
print('imported library')
# get data file names
path = r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\separator\trial_badan_shell_2021\raw'

ds = pd.read_excel(path+'\Reporte Flow PAD-11.xlsx', sheet_name='DATA-SEPARATORS', engine="openpyxl")

print('Data loaded ok')


ds = ds.rename(columns = {'DATE & TIME':'DateTime','Well Head Press':'WHP','Well Head Temp':'WHT',' Choke':'choke','Gas Rate Standard':'GasFlowRate','GOR (Gas/Oil Ratio) Test':'GOR'
                           ,'Sep. Static Press':'sp','Sep. diff. Press':'dp','Sep. Gas Temp':'gasT','Oil Flow Corrected':'OilFlowRate','Water Flow Rate':'WaterFlowRate'
                            ,'Flow Water Cut ':'WCFlow','Oil Temp':'OilTemp'
                           })


ds.to_csv(r"D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\By_Equipment\separator\trial_badan_shell_2021\cleaned\sep_raw_full.csv", index=False, encoding='utf-8-sig')


print('file ready to use')
