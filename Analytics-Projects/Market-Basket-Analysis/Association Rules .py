#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import os as os


os.chdir("documents")


# In[2]:


#import csv
DF = pd.read_csv('teleco_market_basket.csv')
DF.head(10)


# In[3]:


DF=DF.dropna(how='all')


# In[4]:


DF.head()


# In[5]:


print(DF.dtypes)
DF.shape


# In[6]:


trans = []
for i in range (0,7501):
    trans.append([str(DF.values[i,j]) for j in range (0,20)])


# In[7]:


TE= TransactionEncoder()
array=TE.fit_transform(trans)


# In[8]:


Clean_Data= pd.DataFrame(data=array, columns= TE.columns_)
Clean_Data


# In[9]:


for col in Clean_Data.columns:
    print(col)


# In[10]:


Clean_Data = Clean_Data.drop(['nan'], axis =1)


# In[11]:


Clean_Data.shape


# In[12]:


Clean_Data.to_excel("Cleaned_MBA_Data.xlsx", index=False)


# In[13]:


itemsets = apriori(Clean_Data, min_support = 0.05, use_colnames= True)
itemsets.head()


# In[14]:


rules= association_rules(itemsets, metric='lift', min_threshold=1)
rules.head()


# In[15]:


rules[ (rules['lift'] > 1.2) & (rules['confidence'] > 0.25)]

