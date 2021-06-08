### importing the required libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import pandas as pd
#data = pd.read_excel(r'D:\Weatherford\Flow Measurements\Research\Modbus_Reg_AFC.xlsx')
data = pd.read_excel(r'~/airflow/dags/Modbus_DDS.xlsx')

x = data[data['leer']==1][['read','Description','Unit / Remark']]

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

from datetime import datetime

def read_time():
    # datetime object containing current date and time
    now = datetime.now()
    # mm/dd/YY H:M:S
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

#database connection
#database connection
import pyodbc
server = 'daqsamsrv01.database.windows.net'
database = 'daqdb01'
username = 'marcos'
password = 'Asdf*123'   
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
print("Database opened successfully")


def validator(instance):
    if not instance.isError():
        '''.isError() implemented in pymodbus 1.4.0 and above.'''
        decoder = BinaryPayloadDecoder.fromRegisters(
            instance.registers,
            byteorder=Endian.Big, wordorder=Endian.Little
        )
        return float('{0:.2f}'.format(decoder.decode_32bit_float()))

    else:
        # Error handling.
        print("There isn't the registers, Try again.")
        return None


client = ModbusTcpClient('192.168.0.200', port=502)  # Specify the port.

connection = client.connect()

# These args will get passed on to the python operator
default_args = {
    'owner': 'lakshay',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
}

# define the python function
def my_function():
    var5 = read_time()

    if connection:

        for i in x['read']:
            j = x[x['read']==i]

            var1 = int(j['read'])-2
            request = client.read_input_registers(var1, 2, unit=1)  # Specify the unit.
            data = validator(request)

            var2 = str(j.iloc[0]['Description'])
            var3 = data
            var4 = str(j.iloc[0]['Unit / Remark'])
            
            cursor = cnxn.cursor()
            cursor.execute("INSERT INTO modbus_data(register, description, value, unit, created_on) VALUES (?, ?, ?, ?,?)",(var1,var2,var3,var4,var5));
            cnxn.commit()
            print(var2,"= ", data , var4, var5)

            client.close()

    else:
            print('Connection lost, Try again')



    print("Record inserted successfully")
    cnxn.close()




# define the DAG
dag = DAG(
    'python_operator_azure',
    default_args=default_args,
    description='How to use the Python Operator?',
    schedule_interval=timedelta(minutes=1),
)

# define the first task
t1 = PythonOperator(
    task_id='myfunction',
    python_callable= my_function,
    dag=dag,
)

t1
