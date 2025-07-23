#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import seaborn as sns
import os as os


os.chdir("documents")


# In[2]:


#import csv
DF = pd.read_csv('churn_clean.csv')


# In[3]:


DF=DF.select_dtypes(include='number')
DF.columns


# In[4]:


DF=DF.drop(['CaseOrder', 'Zip', 'Lat', 'Lng',  'Item1', 'Item2',
            'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8'], axis=1)


# In[5]:


DF.info()


# In[6]:


scaler = StandardScaler()
DF_std = scaler.fit_transform(DF)
DF_std


# In[7]:


Clean_Data= pd.DataFrame(data=DF_std, columns= DF.columns)
Clean_Data.to_excel("Cleaned_PCA_Data.xlsx", index=False)


# In[8]:


pca = PCA()
pca.fit(Clean_Data)


# In[9]:


Covariance=Clean_Data.cov()
sns.heatmap(Covariance, annot=True,linewidths=2, annot_kws={'size': 6})


# In[10]:


#https://campus.datacamp.com/courses/dimensionality-reduction-in-python/feature-extraction?ex=15
# Pipeline a scaler and pca selecting 11 components
pipe = Pipeline([('scaler', StandardScaler()),
                 ('reducer', PCA(n_components=11))])

# Fit the pipe to the data
pipe.fit(Clean_Data)

# Plot the explained variance ratio
plt.plot(pipe['reducer'].explained_variance_ratio_)

plt.xlabel('Principal component index')
plt.ylabel('Explained variance ratio')
plt.show()


# In[11]:


print(pca.explained_variance_ratio_)
#https://campus.datacamp.com/courses/dimensionality-reduction-in-python/feature-extraction?ex=8


# In[12]:


print(pca.explained_variance_ratio_.cumsum())

