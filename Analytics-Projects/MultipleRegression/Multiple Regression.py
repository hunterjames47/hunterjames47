#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as mpp
import seaborn as sb
import os as os
import statsmodels.api as ssm
import numpy as np
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing

os.chdir("documents")


# In[2]:


#import csv
rawdata = pd.read_csv('churn_clean.csv')


# In[3]:


#check non-nulls and length, make sure there are no null values
rawdata.info()
len(rawdata)


# In[4]:


duplicate_check = rawdata['Customer_id'].duplicated()
duplicate_check.value_counts()


# In[5]:


rawdata.head()


# In[6]:


rawdata = rawdata.drop(['Customer_id','Lat','Lng','County','Zip','Interaction','CaseOrder','Job','UID','City','Area', 'State','TimeZone','Churn'], axis = 1)


# In[7]:


rawdata.describe()


# In[8]:


rawdata['Gender'].value_counts()


# In[9]:


rawdata['Male'] = rawdata['Gender'].replace({"Male":1, "Female":0, "Nonbinary":0})
rawdata['Male'].value_counts()


# In[10]:


rawdata['Marital'].value_counts()
rawdata['Married'] = rawdata['Marital'].replace({"Never Married":0, "Married":1, "Widowed":0, "Separated":0, "Divorced":0})


# In[11]:


rawdata['Children'].value_counts()


# In[12]:


rawdata['Phone'].value_counts()


# In[13]:


rawdata['InternetService'].value_counts()


# In[14]:


rawdata['Internet'] = rawdata['InternetService']
rawdata['Internet']=rawdata['Internet'].replace({"Fiber Optic":1,"DSL":2,"None":0})
rawdata['Internet'].value_counts()


# In[15]:


rawdata['OnlineSecurity'].value_counts()


# In[16]:


rawdata['OnlineSecurity'] = rawdata['OnlineSecurity'].replace({"Yes":1, "No":0})
rawdata['OnlineSecurity'].value_counts()


# In[17]:


rawdata['OnlineBackup'].value_counts()


# In[18]:


rawdata['OnlineBackup'] = rawdata['OnlineBackup'].replace({"Yes":1, "No":0})
rawdata['OnlineBackup'].value_counts()


# In[19]:


rawdata['DeviceProtection'].value_counts()


# In[20]:


rawdata['DeviceProtection'] = rawdata['DeviceProtection'].replace({"Yes":1, "No":0})
rawdata['DeviceProtection'].value_counts()


# In[21]:


rawdata['TechSupport'].value_counts()


# In[22]:


rawdata['TechSupport'] = rawdata['TechSupport'].replace({"Yes":1, "No":0})
rawdata['TechSupport'].value_counts()


# In[23]:


rawdata['StreamingTV'].value_counts()


# In[24]:


rawdata['StreamingTV'] = rawdata['StreamingTV'].replace({"Yes":1, "No":0})
rawdata['StreamingTV'].value_counts()


# In[25]:


rawdata['StreamingMovies'].value_counts()


# In[26]:


rawdata['Multiple'].value_counts()


# In[27]:


rawdata['Multiple'] = rawdata['Multiple'].replace({"Yes":1, "No":0})
rawdata['Multiple'].value_counts()


# In[28]:


rawdata['StreamingMovies'] = rawdata['StreamingMovies'].replace({"Yes":1, "No":0})
rawdata['StreamingMovies'].value_counts()


# In[29]:


rawdata['Techie'] = rawdata['Techie'].replace({"Yes":1, "No":0})
rawdata['Port_modem'] = rawdata['Port_modem'].replace({"Yes":1, "No":0})
rawdata['Tablet'] = rawdata['Tablet'].replace({"Yes":1, "No":0})
rawdata['Techie'] = rawdata['Techie'].replace({"Yes":1, "No":0})


# In[30]:


rawdata['Contract'].value_counts()


# In[31]:


rawdata['Contract'] = rawdata['Contract'].replace({"One year":1,"Two Year":1, "Month-to-month":0})


# In[32]:


rawdata['PaperlessBilling'].value_counts()


# In[33]:


rawdata['PaymentMethod'].value_counts()


# In[34]:


rawdata['Automatic Payment'] = rawdata['PaymentMethod'].replace({"Electronic Check":0,"Bank Transfer(automatic)":1,"Credit Card (automatic)":1, "Mailed Check":0})


# In[35]:


rawdata['Phone'] = rawdata['Phone'].replace({"Yes":1, "No":0})
rawdata['PaperlessBilling'] = rawdata['PaperlessBilling'].replace({"Yes":1, "No":0})


# In[36]:


rawdata['Timely Response'] = rawdata['Item1']
rawdata['Timely Fixes'] = rawdata['Item2']
rawdata['Timely Replacements'] = rawdata['Item3']
rawdata['Reliability'] = rawdata['Item4']
rawdata['Options'] = rawdata['Item5']
rawdata['Respectful Response'] = rawdata['Item6']
rawdata['Courteous Exchange'] = rawdata['Item7']
rawdata['Active Listening'] = rawdata['Item8']


# In[37]:


rawdata=rawdata.drop(['InternetService','Item1','Item2','Item3','Item4','Item5','Item6','Item7','Item8','Marital','PaymentMethod','Gender'], axis = 1)


# In[38]:


rawdata.head()


# In[39]:


rawdata.info()


# In[40]:


rawdata.describe


# In[41]:


#Income and Population have outliers, as would be expected. Opting to keep them in the analysis as they could
# both have a noticeable impact on tenure and it is not unusual for income nor population to be drastically varied

sb.boxplot(data=rawdata, x='Bandwidth_GB_Year',)
mpp.show()

sb.boxplot(data=rawdata, x='Tenure')
mpp.show()

sb.boxplot(data=rawdata, x='MonthlyCharge')
mpp.show()

sb.boxplot(data=rawdata, x='Income')
mpp.show()

sb.boxplot(data=rawdata, x='Population')
mpp.show()


# In[42]:


rawdata.to_excel ('cleaned_churn_data.xlsx', index = False, header=True)


# In[43]:


#univariate continuous variables
rawdata[['Outage_sec_perweek','Children','Age','Email','Contacts','Yearly_equip_failure','Tenure','MonthlyCharge','Bandwidth_GB_Year','Population','Income']].hist()
mpp.savefig('histogram_churn.jpg')
mpp.tight_layout(pad=.1, w_pad=.1, h_pad=.1)


# In[44]:


rawdataSum = rawdata[['Techie','Port_modem','Tablet','Phone','Multiple','OnlineSecurity','OnlineBackup','DeviceProtection',
                     'TechSupport','StreamingTV','StreamingMovies','PaperlessBilling','Married','Automatic Payment','Contract','Male']]


# In[45]:


rawdataSum = rawdataSum.apply(pd.Series.value_counts)
rawdataSum.head()


# In[46]:


rawdataSum2 = rawdata[['Internet']]
rawdataSum2 = rawdataSum2.apply(pd.Series.value_counts)
rawdataSum2.head()


# In[47]:


rawdataSurvSum = rawdata[['Timely Response','Timely Fixes','Timely Replacements','Reliability',
                      'Options','Respectful Response','Courteous Exchange', 
                      'Active Listening']]
rawdataSurvSum = rawdataSurvSum.apply(pd.Series.value_counts)
rawdataSurvSum.head()


# In[48]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Techie', title = 'Techie?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[49]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Port_modem', title = 'Port_modem')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[50]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Tablet', title = 'Tablet')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[51]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Phone', title = 'Phone')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[52]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Multiple', title = 'Multiple Lines?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[53]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='OnlineSecurity', title = 'Online Security')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[54]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='OnlineBackup', title = 'Customer Opted in for Online Backup?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[55]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='DeviceProtection', title = 'Customer Opted in for Device Protection?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[56]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='PaperlessBilling', title = 'Customer Opted in for Paperless Billing?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[57]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='TechSupport', title = 'Tech Support?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[58]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='StreamingTV', title = 'Streaming TV?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[59]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='StreamingMovies', title = 'Streaming Movies?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[60]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Married', title = 'Married?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[61]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Contract', title = 'Contract?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[62]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Automatic Payment', title = 'Automatic Payment?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[63]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Male', title = 'Male?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[64]:


ax = rawdataSum2.plot.bar(ylabel="Quantity",y='Internet', title = 'Internet?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[65]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Timely Response', title = 'Timely Response Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[66]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Reliability', title = 'Reliability Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[67]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Timely Replacements', title = 'Timely Replacements Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[68]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Timely Fixes', title = 'Timely Fixes Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[69]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Options', title = 'Options Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[70]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Respectful Response', title = 'Respectful Response Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[71]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Courteous Exchange', title = 'Courteous Exchange Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[72]:


ax = rawdataSurvSum.plot.bar(ylabel="Quantity",y='Active Listening', title = 'Active Listening Importance (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[73]:


ax = sb.scatterplot(x='MonthlyCharge', y='Bandwidth_GB_Year', data=rawdata)


# In[74]:


ax = sb.scatterplot(x='Outage_sec_perweek', y='Bandwidth_GB_Year', data=rawdata)


# In[75]:


ax = sb.scatterplot(x='Children', y='Bandwidth_GB_Year', data=rawdata)


# In[76]:


ax = sb.scatterplot(x='Age', y='Bandwidth_GB_Year', data=rawdata)


# In[77]:


ax = sb.scatterplot(x='Email', y='Bandwidth_GB_Year', data=rawdata)


# In[78]:


ax = sb.scatterplot(x='Contacts', y='Bandwidth_GB_Year', data=rawdata)


# In[79]:


ax = sb.scatterplot(x='Yearly_equip_failure', y='Bandwidth_GB_Year', data=rawdata)


# In[80]:


ax = sb.scatterplot(x='MonthlyCharge', y='Bandwidth_GB_Year', data=rawdata)


# In[81]:


ax = sb.scatterplot(x='Tenure', y='Bandwidth_GB_Year', data=rawdata)


# In[82]:


ax = sb.scatterplot(x='Population', y='Bandwidth_GB_Year', data=rawdata)


# In[83]:


ax = sb.scatterplot(x='Income', y='Bandwidth_GB_Year', data=rawdata)


# In[84]:


x = rawdata.drop(['Bandwidth_GB_Year'], axis=1)
y = rawdata['Bandwidth_GB_Year']


# In[85]:


x2=ssm.add_constant(x)
model= ssm.OLS(y,x2).fit()
print_summary= model.summary()
print(print_summary)


# In[86]:


X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=101)
model = LinearRegression()
model.fit(X_train,y_train)
predictions = model.predict(X_test)
print(
  'mean_absolute_error : ', mean_absolute_error(y_test, predictions))
residuals=y_test-predictions
mpp.scatter(residuals,predictions)
mpp.show()


# In[87]:


#keep predictors with a P-value greater than .05
NewPredictor=rawdata[['Bandwidth_GB_Year','Children','Age','Contract','Multiple','OnlineSecurity','OnlineBackup',
                      'DeviceProtection','TechSupport','StreamingTV', 'StreamingMovies', 'Tenure', 'MonthlyCharge','Male',
                      'Internet','Timely Response','Timely Fixes']]
x = NewPredictor.drop(['Bandwidth_GB_Year'], axis=1)
y = NewPredictor['Bandwidth_GB_Year']


# In[88]:


xs = x     # independent variables
corr = np.corrcoef(xs, rowvar=0)  # correlation matrix
w, v = np.linalg.eig(corr)        # eigen values & eigen vectors
w


# In[89]:


x = x.drop(['Multiple','MonthlyCharge','Timely Fixes','Timely Response'], axis=1)
y = NewPredictor['Bandwidth_GB_Year']


# In[90]:


x2=ssm.add_constant(x)
model= ssm.OLS(y,x2).fit()
print_summary= model.summary()
print(print_summary)


# In[91]:


X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=101)
model = LinearRegression()
model.fit(X_train,y_train)
predictions = model.predict(X_test)
mse=mean_squared_error(y_test, predictions)
print(
  'mean_absolute_error : ', mean_absolute_error(y_test, predictions))
residuals=y_test-predictions
mpp.scatter(residuals,predictions)
mpp.show()


# In[ ]:




