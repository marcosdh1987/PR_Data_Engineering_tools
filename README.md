# PR_Data_Engineering_tools


Scope of work:

this repository collects the Engineering tools tested for the development proposal in the field operations

Architecture:

![image](https://user-images.githubusercontent.com/31476977/119668857-e9b90080-be0d-11eb-889f-773e306c353f.png)


##Tools:\
•	Ubuntu 20.04 OS\
•	Apache Airflow\
•	PostgreSQL + pgAdmin
• WinSCP

### Option 1 using docker:

To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.

using WSL ubuntu:

mkdir airflow-docker
cd airflow-docker

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.0/docker-compose.yaml'

mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

You need to run database migrations and create the first user account. To do it, run.

docker-compose up airflow-init

Now you can start all services:

docker-compose up

next the airflow user and pass are same.

note:
to install pandas in powershell (py -m pip install pandas)

###Option 2 Installation commands:

#### pip update
sudo pip install --upgrade pip

#### PostgreSQL:

to install
sudo apt-get install postgresql postgresql-contrib

sudo -u postgres psql

Create a new user and provide privileges to it

CREATE ROLE ubuntu;
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES on database airflow to ubuntu;
ALTER ROLE ubuntu SUPERUSER;
ALTER ROLE ubuntu CREATEDB;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ubuntu;

connect to airflow database and get connection information

postgres-# \c airflow
airflow=# \conninfo

#to connect with postgresql\
$ sudo -u postgres psql\
ALTER USER marcosdb WITH Superuser;\
#to show list of roles\
\du


We’ll change settings in pg_hb.conf file for required configuration as per Airflow.\
You can run command SHOW hba_file to find location of pg_hba.conf file.
Most likely located at pg_hb.conf located at /etc/postgresql/*/main/pg_hba.conf

sudo nano /etc/postgresql/*/main/pg_hba.conf

open this file with vim and change ipv4 address to 0.0.0.0/0 and listen_addresses to listen_addresses = ‘*’.

We will restart PostgreSQL to load changes.

sudo service postgresql restart

Aiflow:

airflow webserver --port 8081

airflow init db

airflow scheduler

winSCP:
use script [winscp](winscp.bat)



Filesnames for learning purposes:\
•	[Modbus_AFC_V001](Modbus_AFC_V001.ipynb)\
• [some_querys](some_querys)\

Filesname deployed:\
•	[pydag](pydag.py)\
•	[Modbus_DDS](Modbus_DDS.xlsx)\
•	[BD_Arch](BD_Arch.vsdx)\


Full Dig Data architecture (with azure):\

![image](https://user-images.githubusercontent.com/31476977/119707587-b12b1e00-be31-11eb-8c68-edc43bc1b538.png)




