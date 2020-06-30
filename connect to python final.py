# -*- coding: utf-8 -*-
"""
Created on Thu Oct  31 21:20:13 2019

@author: Catherine Chen
"""

#Connect to python
import pymysql
import pandas as pd
from sqlalchemy import create_engine
db = pymysql.connect(host='localhost',
user='root',
password='64122200',
db='db_consumer_panel',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)
engine = create_engine('mysql+pymysql://root:64122200@localhost/db_consumer_panel')

# load table dta_at_hh
database_1 = pd.read_csv("/Users/hanzhexiao/Desktop/dta_at_hh.csv", sep=',')
pd.io.sql.to_sql(database_1, 'dta_at_hh', con=engine, index=False, if_exists='replace')

# load table dta_at_prod_id
database_2 = pd.read_csv("/Users/hanzhexiao/Desktop/dta_at_prod_id.csv", sep=',')
pd.io.sql.to_sql(database_2, 'dta_at_prod_id', con=engine, index=False, if_exists='replace')

# load table dta_at_TC
database_3= pd.read_csv("/Users/hanzhexiao/Desktop/dta_at_TC.csv", sep=',')
pd.io.sql.to_sql(database_3,'dta_at_TC', con=engine, index=False, if_exists='replace')

# load table dta_at_TC_upc
database_4= pd.read_csv("/Users/hanzhexiao/Desktop/dta_at_TC_upc.csv", sep=',')
pd.io.sql.to_sql(database_4,'dta_at_TC_upc', con=engine, index=False, if_exists='replace')