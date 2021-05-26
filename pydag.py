### importing the required libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import pandas as pd
#data = pd.read_excel(r'D:\Weatherford\Flow Measurements\Research\Modbus_Reg_AFC.xlsx')
data = pd.read_excel(r'~/airflow/dags/Modbus_Reg_AFC.xlsx')

x = data[data['leer']==1][['read','Description','Unit / Remark']]

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

from datetime import datetime

def read_time():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

#database connection
import psycopg2

con = psycopg2.connect(database="mydb", user="marcosdb", password="32922161", host="192.168.0.7", port="5432")

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
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
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

            var2 = j.iloc[0]['Description']
            #var2 = 'pressure'
            var3 = data
            var4 = j.iloc[0]['Unit / Remark']
            #var4 = 'bara'
            cur = con.cursor()
            cur.execute("INSERT INTO modbus_data(register, description, value, unit, created_on) VALUES (%s, %s, %s, %s, %s)",(var1,var2,var3,var4,var5));
            con.commit()
            print(var2,"= ", data , var4, var5)

            client.close()

    else:
            print('Connection lost, Try again')



    print("Record inserted successfully")
    con.close()




# define the DAG
dag = DAG(
    'python_operator',
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
