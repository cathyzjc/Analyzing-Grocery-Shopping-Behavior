# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:26:48 2019

@author: Catherine Chen
"""
# In[] Setup
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

large = 22; med = 16; small = 12
params = {'axes.titlesize'  : large,
          'legend.fontsize' : med,
          'figure.figsize'  : (16, 10),
          'axes.labelsize'  : med,
          'axes.titlesize'  : med,
          'xtick.labelsize' : med,
          'ytick.labelsize' : med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")
#%matplotlib inline

# In[] a.4.i
a_4_i_1 = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\a4.i.1.csv")

a_4_i_2 = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\a4.i.2.csv")



# In[] a.4.ii
a_4_ii = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\a4.ii.csv")
fig,ax = plt.subplots()

name_list=[]
for a in a_4_ii['department_at_prod_id']:
    name_list.append(a)

num_list_1=[]
for a in a_4_ii['count(distinct prod_id)']:
    num_list_1.append(a)
     
num_list_2=[]
for a in a_4_ii['count(distinct module_at_prod_id)']:
    num_list_2.append(a)



rects=plt.bar(range(len(num_list_1)), num_list_1)

index=list(range(12))
index=[float(c) for c in index]

plt.ylim(ymax=1400000, ymin=0)
plt.title('Distribution of products per department',verticalalignment='bottom',fontsize=20)
plt.xticks(index, name_list,rotation=90,fontsize=15)
plt.ylabel("products") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=15)
plt.show()

# In[] b2.iii
#One retailer
b_2_iii_1 = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b2.iii.1.csv",index_col=0).sort_index()

fig,ax=plt.subplots()
ax.bar(b_2_iii_1.index,b_2_iii_1['count(hh_id)'],label='One retailer')
ax.set_xticklabels(b_2_iii_1.index,rotation=90)
ax.set_ylabel("Number of loyalist households per state")
plt.title('Distribution by state (One retailer)',verticalalignment='bottom',fontsize=30)
	
plt.show()

#Two retailers
b_2_iii_2 = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b2.iii.2.csv",index_col=0).sort_index()

fig,ax=plt.subplots()
ax.bar(b_2_iii_2.index,b_2_iii_2['count(hh_id)'],label='Two retailers',color='green')
ax.set_xticklabels(b_2_iii_2.index,rotation=90)
ax.set_ylabel("Number of loyalist households per state")
plt.title('Distribution by state (Two retailers)',verticalalignment='bottom',fontsize=30)
plt.show()

# In[] b3.i/ii
b_3_i = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b3.i.csv",index_col=0).sort_index()
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.style.use("seaborn-colorblind")
ax.plot(b_3_i.index,b_3_i['average_purchase_items']) 
ax.set_xlabel('Time',fontsize=25)
ax.set_ylabel('Average number of items purchased',fontsize=25)
ax.tick_params('y')

b_3_ii = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b3.ii.csv",index_col=0).sort_index()
#import matplotlib.pyplot as plt
#fig, ax = plt.subplots()
ax2=ax.twinx()
ax2.plot(b_3_ii.index,b_3_ii['average_shopping_trips']) 
ax2.set_ylabel('Average number of shopping trips',fontsize=25)
ax2.tick_params('y')


lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)
plt.title('Average number of items/shopping trips per month',verticalalignment='bottom',fontsize=30)

plt.show()
'''
ax.plot(b_3_ii.index,b_3_ii['average_shopping_trips']) 
ax.set_xlabel('Time')
ax.set_ylabel('Average number of items purchased')
plt.show()
'''
# In[] b3.i/ii drop the first date
b_3_i = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b3.i.csv",index_col=0).sort_index()
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.style.use("seaborn-colorblind")
b_3_i_order=b_3_i.drop("2003-12") 
ax.plot(b_3_i_order.index,b_3_i_order['average_purchase_items']) 
ax.set_xlabel('Time',fontsize=25)
ax.set_ylabel('Average number of items purchased',fontsize=25)
ax.tick_params('y')

b_3_ii = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b3.ii.csv",index_col=0).sort_index()
b_3_ii_order=b_3_ii.drop("2003-12") 

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots()
ax2=ax.twinx()
ax2.plot(b_3_ii_order.index,b_3_ii_order['average_shopping_trips']) 
ax2.set_ylabel('Average number of shopping trips',fontsize=25)
ax2.tick_params('y')


lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)
plt.title('Average number of items/shopping trips per month',verticalalignment='bottom',fontsize=30)

plt.show()

# In[] b.3.iii
b_3_iii = pd.read_csv("C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\BUS 211F Analyzing Big Data I\\final project\\final results\\bigdatafinalfinalfinal\\b3.iii.csv",index_col=0).sort_index()
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.style.use("seaborn-colorblind")
avg_list=[]
for a in b_3_iii['avg(TIME_WINDOW_SIZE)']:
    avg_list.append(a)

ax.boxplot(avg_list) 
ax.set_ylabel('AVG(TIME_WINDOW_SIZE)')
plt.title('Average number of days between 2 consecutive shopping trips',verticalalignment='bottom',fontsize=30)

plt.show()

# In[] c.1
# Import dataset 
corr1 = pd.read_csv("/Users/liuxinyi/Downloads/c.1.csv")
corr1_1 = corr1.drop([0])
# Each line in its own column
sns.set_style("white")
gridobj = sns.lmplot(x       = "average_shopping_trips",
                     y       = "average_purchase_items", 
                     data    = corr1, 
                     height  = 7, 
                     robust  = True, 
                     palette ='Set1',
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))

# Decorations
gridobj.set(xlim=(2, 18), ylim=(20, 130))
plt.show()

# Each line in its own column
sns.set_style("white")
gridobj = sns.lmplot(x       = "average_shopping_trips",
                     y       = "average_purchase_items", 
                     data    = corr1_1, 
                     height  = 7, 
                     robust  = True, 
                     palette ='Set1',
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))

# Decorations
gridobj.set(xlim=(14, 18), ylim=(100, 130))
plt.show()

# In[] c.2
# Import dataset 
corr2 = pd.read_csv("/Users/liuxinyi/Downloads/fwdbigdatafinalfinalfinal/c2.csv")

# Each line in its own column
sns.set_style("white")
gridobj = sns.lmplot(x       = "number_items_purchased",
                     y       = "item_average_price", 
                     data    = corr2, 
                     height  = 7, 
                     robust  = True, 
                     palette ='Set1',
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))

# Decorations
gridobj.set(xlim=(0, 38), ylim=(0, 110))
plt.show()

# In[] c.3.i
a_3_i = pd.read_csv(r"C:\Users\yiche\Desktop\c3.i.csv")
fig,ax = plt.subplots()

name_list=[]
for a in a_3_i['department_at_prod_id']:
    name_list.append(a)

num_list_1=[]
for a in a_3_i['private_label_percent']:
    a = round(a,4)
    num_list_1.append(a)
     

rects=plt.bar(range(len(num_list_1)), num_list_1)

index=list(range(10))
index=[float(c) for c in index]

plt.ylim(ymax=0.5, ymin=0)
plt.title('product categories that have proven to be more “Private labelled” ',verticalalignment='bottom',fontsize=15)
plt.xticks(index, name_list,rotation=90,fontsize=10)
plt.ylabel("private_label_percent") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=8)
plt.show()

# In[] c.3.ii
a_3_ii = pd.read_csv(r"C:\Users\yiche\Desktop\c3.ii.csv")
fig,ax = plt.subplots()

name_list=[]
for a in a_3_ii['department_at_prod_id']:
    name_list.append(a)

num_list_1=[]
for a in a_3_ii['private_label_percent']:
    a = round(a,4)
    num_list_1.append(a)
     

rects=plt.bar(range(len(num_list_1)), num_list_1)

index=list(range(10))
index=[float(c) for c in index]

plt.ylim(ymax=0.4, ymin=0)
plt.title('Expenditure Share in Private Labeled products for each department',verticalalignment='bottom',fontsize=15)
plt.xticks(index, name_list,rotation=90,fontsize=10)
plt.ylabel("Expenditure Share in  ‘CTL BR’  ") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=8)
plt.show()

# In[] c.3.iii-1
a_3_iii_1 = pd.read_csv(r"C:\Users\yiche\Desktop\c3.iii.1.csv")
fig,ax = plt.subplots()

name_list=[]
for a in a_3_iii_1['income_group']:
    if a ==1:
        b = 'Low'
    elif a==2:
        b = 'Medium'
    else:
        b = 'High'    
    name_list.append(b)

num_list_1=[]
for a in a_3_iii_1['group_avg']:
    num_list_1.append(a)
     

rects=plt.bar(range(len(num_list_1)), num_list_1)

index=list(range(3))
index=[float(c) for c in index]

plt.ylim(ymax=13500000, ymin=0)
plt.title('Average Monthly Expenditure on Grocery',verticalalignment='bottom',fontsize=20)
plt.xticks(index, name_list,rotation=0,fontsize=15)
plt.ylabel("Avg monthly expenditure") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=10)
plt.show()

# In[] c.3.iii-2
a_3_iii_2 = pd.read_csv(r"C:\Users\yiche\Desktop\c3.iii.2.csv")
fig,ax = plt.subplots()

name_list=[]
for a in a_3_iii_1['income_group']:
    if a ==1:
        b = 'Low'
    elif a==2:
        b = 'Medium'
    else:
        b = 'High'    
    name_list.append(b)

num_list_1=[]
for a in a_3_iii_2['percentage']:
    a= round(a,4)
    num_list_1.append(a)
     

rects=plt.bar(range(len(num_list_1)), num_list_1)

index=list(range(3))
index=[float(c) for c in index]

plt.ylim(ymax=0.5, ymin=0)
plt.title('% of private label share in monthly  expenditures of income group',verticalalignment='bottom',fontsize=20)
plt.xticks(index, name_list,rotation=0,fontsize=15)
plt.ylabel("% of private label share") 
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom',fontsize=10)
plt.show()

    
