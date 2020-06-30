# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:50:15 2019

@author: Cathy Chen
"""

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        port = '3306',
        passwd='zjchen1358',
)


mycursor = mydb.cursor()
mycursor.execute('use db_consumer_panel;')
mycursor.execute('select department_at_prod_id,count(distinct prod_id),count(distinct module_at_prod_id) from dta_at_prod_id group by department_at_prod_id;')
myresult = mycursor.fetchall()

s=[]
for x in myresult:   
    print(x)
    s.append(x)

mycursor.close()

# In[]

###product
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率

name_list=[]
for a in s:
    name_list.append(a[0])

num_list=[]
for a in s:
    num_list.append(a[1])


rects=plt.bar(range(len(num_list)), num_list)

index=list(range(12))
index=[float(c) for c in index]


plt.ylim(ymax=1400000, ymin=0)
plt.title('Distribution of products per department',verticalalignment='bottom')
plt.xticks(index, name_list,rotation=90,fontsize=7)
plt.ylabel("products") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=7)
plt.show()


# In[]

###module
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率

name_list_2=[]
for a in s:
    name_list_2.append(a[0])

num_list_2=[]
for a in s:
    num_list_2.append(a[2])


rects=plt.bar(range(len(num_list_2)), num_list_2)

index=list(range(12))
index=[float(c) for c in index]


plt.ylim(ymax=500, ymin=0)
plt.title('Distribution of modules per department',verticalalignment='bottom')
plt.xticks(index, name_list,rotation=90,fontsize=7)
plt.ylabel("Modules") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=7)
plt.show()


