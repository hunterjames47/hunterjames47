#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.vq import kmeans, vq
import seaborn as sns
import os as os
from sklearn.metrics import silhouette_score


os.chdir("documents")


# In[2]:


#import csv
DF = pd.read_csv('churn_clean.csv')


# In[3]:


DF= DF[['MonthlyCharge', 'Income']]


# In[4]:


DF.info()
len(DF)


# In[5]:


print("Missing Values ", (DF.isna().sum() + DF.isnull().sum()).sum())


# In[6]:


DF.describe()


# In[7]:


Array=DF.to_numpy()
Scaler = StandardScaler()
Standard = Scaler.fit_transform(Array)
print(Standard)


# In[8]:


Clean_Data= pd.DataFrame(data=Standard, columns= ['MonthlyCharge', 'Income'])
Clean_Data.to_excel("Cleaned_DF_Data.xlsx", index=False)


# In[9]:


Std_DF = pd.DataFrame(Standard, columns= ['MonthlyCharge', 'Income'])
distortions = []
num_clusters = range(1, 10)

# Create a list of distortions from the kmeans function
for i in num_clusters:
    cluster_centers, distortion = kmeans(Std_DF[['MonthlyCharge', 'Income']],i)
    distortions.append(distortion)

# Create a DataFrame with two lists - num_clusters, distortions
elbow_plot = pd.DataFrame({'num_clusters': num_clusters, 'distortions': distortions})

# Creat a line plot of num_clusters and distortions
sns.lineplot(x='num_clusters', y='distortions', data = elbow_plot)


# In[10]:


centroids,_= kmeans(Std_DF, 3)
Std_DF['cluster_labels'], _ = vq(Std_DF, centroids)
sns.scatterplot(x='MonthlyCharge', y='Income', hue='cluster_labels', data=Std_DF)
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]
print(centroids)
sns.scatterplot(x=centroids_x,y=centroids_y,color="red", marker = "s")


# In[11]:


cluster_labels=Std_DF['cluster_labels']
SilhouetteScore= silhouette_score(Std_DF, cluster_labels)
print(SilhouetteScore)

