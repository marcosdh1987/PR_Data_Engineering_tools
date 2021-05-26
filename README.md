# PR_Data_Engineering_tools


Scope of work:

this repository collects the Engineering tools tested for the development proposal in the field operations

Architecture:

![image](https://user-images.githubusercontent.com/31476977/119668857-e9b90080-be0d-11eb-889f-773e306c353f.png)


Tools:\
•	Ubuntu 20.04 OS\
•	Apache Airflow\
•	PostgreSQL + pgAdmin\


Installation commands:

PostgreSQL:
#to connect\
$ sudo -u postgres psql\
ALTER USER marcosdb WITH Superuser;\
#to show list of roles\
\du

Aiflow:\

We’ll change settings in pg_hb.conf file for required configuration as per Airflow.\ 
You can run command SHOW hba_file to find location of pg_hba.conf file.\
Most likely located at pg_hb.conf located at /etc/postgresql/*/main/pg_hba.conf\

sudo nano /etc/postgresql/*/main/pg_hba.conf\

open this file with vim and change ipv4 address to 0.0.0.0/0 and listen_addresses to listen_addresses = ‘*’.\

We will restart PostgreSQL to load changes.\

airflow webserver --port 8081\

airflow init db\

airflow scheduler\


Filesnames for learning purposes:\
•	-\

Filesname deployed:\
•	pydag.py\
•	Modbus_DDS.xlsx\
•	BD_Arch.vsdx\


