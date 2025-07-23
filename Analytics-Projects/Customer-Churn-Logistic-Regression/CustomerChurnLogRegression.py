#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import prince as pr
import matplotlib.pyplot as mpp
import numpy as np
import seaborn as sb
import os as os
import sklearn as sk
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

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


rawdata.describe()


# In[7]:


rawdata = rawdata.drop(['Customer_id','Lat','Lng','County','Zip','Interaction','CaseOrder','Job','UID','City','Area', 'State','TimeZone','Income','Population','Tenure'], axis = 1)


# In[8]:


rawdata.describe()


# In[9]:


rawdata['Gender'].value_counts()


# In[10]:


rawdata['MonthlyCharge'].describe()


# In[11]:


rawdata.loc[rawdata['MonthlyCharge'] >=172.62, 'HighCharge?'] = True
rawdata.loc[rawdata['MonthlyCharge'] < 172.62, 'HighCharge?'] = False
rawdata['HighCharge?'].value_counts()


# In[12]:


rawdata['Male?'] = rawdata['Gender'].replace({"Male":True, "Female":False,"Nonbinary":False})
rawdata['Male?'].value_counts()


# In[13]:


rawdata['Age'].describe()


# In[14]:


rawdata.loc[rawdata['Age'] >=  53.09, 'Older?'] = True
rawdata.loc[rawdata['Age'] < 53.07, 'Older?'] = False
rawdata['Older?'].value_counts()


# In[15]:


rawdata['Marital'].value_counts()
rawdata['Married'] = rawdata['Marital'].replace({"Never Married":0, "Married":1, "Widowed":0, "Separated":0, "Divorced":0})


# In[16]:


rawdata['Children'].value_counts()
rawdata.loc[rawdata['Children'] > 0, 'Children?'] = True
rawdata.loc[rawdata['Children'] == 0, 'Children?'] = False
rawdata['Children?'].value_counts()


# In[17]:


rawdata['Phone'].value_counts()


# In[18]:


rawdata['Multiple'].value_counts()


# In[19]:


rawdata['MultipleLines'] = rawdata['Multiple'].replace({"Yes":True, "No":False})
rawdata['MultipleLines'].value_counts()


# In[20]:


rawdata['InternetService'].value_counts()


# In[21]:


rawdata['FiberOptic'] = rawdata['InternetService']
rawdata['FiberOptic']=rawdata['FiberOptic'].replace({"Fiber Optic":True,"DSL":False,"None":False})
rawdata['FiberOptic'].value_counts()


# In[22]:


rawdata['DSL'] = rawdata['InternetService']
rawdata['DSL']=rawdata['DSL'].replace({"Fiber Optic":False,"DSL":True,"None":False})
rawdata['DSL'].value_counts()


# In[23]:


rawdata['OnlineSecurity'].value_counts()


# In[24]:


rawdata['OnlineSecurity'] = rawdata['OnlineSecurity'].replace({"Yes":True, "No":False})
rawdata['OnlineSecurity'].value_counts()


# In[25]:


rawdata['OnlineBackup'].value_counts()


# In[26]:


rawdata['OnlineBackup'] = rawdata['OnlineBackup'].replace({"Yes":True, "No":False})
rawdata['OnlineBackup'].value_counts()


# In[27]:


rawdata['DeviceProtection'].value_counts()


# In[28]:


rawdata['DeviceProtection'] = rawdata['DeviceProtection'].replace({"Yes":True, "No":False})
rawdata['DeviceProtection'].value_counts()


# In[29]:


rawdata['TechSupport'].value_counts()


# In[30]:


rawdata['TechSupport'] = rawdata['TechSupport'].replace({"Yes":True, "No":False})
rawdata['TechSupport'].value_counts()


# In[31]:


rawdata['StreamingTV'].value_counts()


# In[32]:


rawdata['StreamingTV'] = rawdata['StreamingTV'].replace({"Yes":True, "No":False})
rawdata['StreamingTV'].value_counts()


# In[33]:


rawdata['StreamingMovies'].value_counts()


# In[34]:


rawdata['StreamingMovies'] = rawdata['StreamingMovies'].replace({"Yes":True, "No":False})
rawdata['StreamingMovies'].value_counts()


# In[35]:


rawdata['Contract'].value_counts()
rawdata['Contract'] = rawdata['Contract'].replace({"One Year":True,"Two Year":True, "Month-to-month":False})


# In[36]:


rawdata['Outage_sec_perweek'].describe()


# In[37]:


rawdata.loc[rawdata['Outage_sec_perweek'] >= 10.001848, 'High Outage_Sec_Week'] = True
rawdata.loc[rawdata['Outage_sec_perweek'] < 10.001848, 'High Outage_Sec_Week'] = False
rawdata['High Outage_Sec_Week'].value_counts()


# In[38]:


rawdata['Email'].describe()


# In[39]:


rawdata.loc[rawdata['Email'] >= 12.016, 'High Email'] = True
rawdata.loc[rawdata['Email'] < 12.016, 'High Email'] = False
rawdata['High Email'].value_counts()


# In[40]:


rawdata['Contacts'].value_counts()


# In[41]:


rawdata.loc[rawdata['Contacts'] > 0, 'Contacts?'] = True
rawdata.loc[rawdata['Contacts'] == 0, 'Contacts?'] = False
rawdata['Contacts?'].value_counts()


# In[42]:


rawdata['Yearly_equip_failure'].value_counts()


# In[43]:


rawdata.loc[rawdata['Yearly_equip_failure'] > 0, 'Equip Failure?'] = True
rawdata.loc[rawdata['Yearly_equip_failure'] == 0, 'Equip Failure?'] = False
rawdata['Equip Failure?'].value_counts()


# In[44]:


rawdata['PaperlessBilling'].value_counts()


# In[45]:


rawdata['PaymentMethod'].value_counts()
rawdata['Online Payment?'] = rawdata['PaymentMethod'].replace({"Electronic Check":True,"Bank Transfer(automatic)":True,"Credit Card (automatic)":True, "Mailed Check":False})


# In[46]:


rawdata['Bandwidth_GB_Year'].describe()


# In[47]:


rawdata.loc[rawdata['Bandwidth_GB_Year'] >= 3392.341550, 'High Bandwidth_GB_Year'] = True
rawdata.loc[rawdata['Bandwidth_GB_Year'] < 3392.341550, 'High Bandwidth_GB_Year'] = False
rawdata['High Bandwidth_GB_Year'].value_counts()


# In[48]:


rawdata.loc[rawdata['Item1'] <=4, 'Timely Response Important'] = True
rawdata.loc[rawdata['Item1'] >4, 'Timely Response Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item2'] <=4, 'Timely Fixes Important'] = True
rawdata.loc[rawdata['Item2'] >4, 'Timely Fixes Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item3'] <=4, 'Timely Replacements Important'] = True
rawdata.loc[rawdata['Item3'] >4, 'Timely Replacements Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item4'] <=4, 'Reliability Important'] = True
rawdata.loc[rawdata['Item4'] >4, 'Reliability Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item5'] <=4, 'Options Important'] = True
rawdata.loc[rawdata['Item5'] >4, 'Options Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item6'] <=4, 'Respectful Response Important'] = True
rawdata.loc[rawdata['Item6'] >4, 'Respectful Response Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item7'] <=4, 'Courteous Exchange Important'] = True
rawdata.loc[rawdata['Item7'] >4, 'Courteous Exchange Important'] = False
rawdata['Timely Response Important'].value_counts()
rawdata.loc[rawdata['Item7'] <=4, 'Active Listening Important'] = True
rawdata.loc[rawdata['Item8'] >4, 'Active Listening Important'] = False
rawdata['Timely Response Important'].value_counts()


# In[49]:


rawdata['Phone'] = rawdata['Phone'].replace({"Yes":True, "No":False})
rawdata['PaperlessBilling'] = rawdata['PaperlessBilling'].replace({"Yes":True, "No":False})
rawdata['Churn'] = rawdata['Churn'].replace({"Yes":True, "No":False})
rawdata['Techie'] = rawdata['Techie'].replace({"Yes":True, "No":False})
rawdata['Port_modem'] = rawdata['Port_modem'].replace({"Yes":True, "No":False})
rawdata['Tablet'] = rawdata['Tablet'].replace({"Yes":True, "No":False})
rawdata['Techie'] = rawdata['Techie'].replace({"Yes":True, "No":False})


# In[50]:


rawdata['Married'] = rawdata['Married'].astype('bool')
rawdata['Children?'] = rawdata['Children?'].astype('bool')
rawdata['Phone'] = rawdata['Phone'].astype('bool')
rawdata['PaperlessBilling'] = rawdata['PaperlessBilling'].astype('bool')
rawdata['Older?'] = rawdata['Older?'].astype('bool')
rawdata['Churn'] = rawdata['Churn'].astype('bool')
rawdata['HighCharge?'] = rawdata['HighCharge?'].astype('bool')
rawdata['FiberOptic']=rawdata['FiberOptic'].astype('bool')
rawdata['DSL']=rawdata['DSL'].astype('bool')
rawdata['Contract']=rawdata['Contract'].astype('bool')
rawdata['High Outage_Sec_Week'] = rawdata['High Outage_Sec_Week'].astype('bool')
rawdata['High Email']=rawdata['High Email'].astype('bool')
rawdata['Contacts?']=rawdata['Contacts?'].astype('bool')
rawdata['Equip Failure?']=rawdata['Equip Failure?'].astype('bool')
rawdata['Timely Response Important']=rawdata['Timely Response Important'].astype('bool')
rawdata['Timely Fixes Important']=rawdata['Timely Fixes Important'].astype('bool')
rawdata['Timely Replacements Important']=rawdata['Timely Replacements Important'].astype('bool')
rawdata['Reliability Important']=rawdata['Reliability Important'].astype('bool')
rawdata['Options Important']=rawdata['Options Important'].astype('bool')
rawdata['Respectful Response Important']=rawdata['Respectful Response Important'].astype('bool')
rawdata['Courteous Exchange Important']=rawdata['Courteous Exchange Important'].astype('bool')
rawdata['Active Listening Important']=rawdata['Active Listening Important'].astype('bool')
rawdata['High Bandwidth_GB_Year']=rawdata['High Bandwidth_GB_Year'].astype('bool')


# In[51]:


rawdata=rawdata.drop(['Gender','PaymentMethod','MonthlyCharge','InternetService','Marital','Multiple','Children','Item1','Item2','Item3','Item4','Item5','Item6','Item7','Item8','Age','Contacts','Email','Outage_sec_perweek','Yearly_equip_failure','Bandwidth_GB_Year'], axis = 1)


# In[52]:


rawdata.head()


# In[53]:


rawdata.info()


# In[54]:


rawdataSum = rawdata.apply(pd.Series.value_counts)
rawdataSum.head()


# In[55]:


rawdata.describe


# In[56]:


rawdata.to_excel ('cleaned_data.xlsx', index = False, header=True)


# In[57]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Churn', title = 'Churned?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[58]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Older?', title = 'Older Customer?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[59]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Married', title = 'Customer is Married?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[60]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Phone', title = 'Customer has Phone Service?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[61]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='MultipleLines', title = 'Customer has Multiple Lines?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[62]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='FiberOptic', title = 'Customer has Fiber Optic?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[63]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='DSL', title = 'Customer has DSL?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[64]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='OnlineSecurity', title = 'Customer Opted in for Online Security?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[65]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='OnlineBackup', title = 'Customer Opted in for Online Backup?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[66]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='DeviceProtection', title = 'Customer Opted in for Device Protection?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[67]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='TechSupport', title = 'Tech Support?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[68]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='StreamingTV', title = 'Streaming TV?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[69]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='StreamingMovies', title = 'Streaming Movies?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[70]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Contract', title = 'In Contract?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[71]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='HighCharge?', title = 'High Charge?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[72]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='PaperlessBilling', title = 'Utilizes Paperless Billing?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[73]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Male?', title = 'Customer is a Male?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[74]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Online Payment?', title = 'Utilizes Online Payment?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[75]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Techie', title = 'Techie?')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[76]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Port_modem', title = 'Port_modem')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[77]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Tablet', title = 'Tablet')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[78]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Timely Response Important', title = 'Timely Response Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[79]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Reliability Important', title = 'Reliability Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[80]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Timely Replacements Important', title = 'Timely Replacements Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[81]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Timely Fixes Important', title = 'Timely Fixes Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[82]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Options Important', title = 'Options Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[83]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Respectful Response Important', title = 'Respectful Response Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[84]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Courteous Exchange Important', title = 'Courteous Exchange Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[85]:


ax = rawdataSum.plot.bar(ylabel="Quantity",y='Active Listening Important', title = 'Active Listening Important (Survey)')
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[86]:


ax = sb.countplot(x='Older?', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[87]:


ax = sb.countplot(x='Married', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[88]:


ax = sb.countplot(x='Children?', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[89]:


ax = sb.countplot(x='Phone', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[90]:


ax = sb.countplot(x='MultipleLines', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[91]:


ax = sb.countplot(x='FiberOptic', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[92]:


ax = sb.countplot(x='DSL', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[93]:


ax = sb.countplot(x='OnlineSecurity', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[94]:


ax = sb.countplot(x='OnlineBackup', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[95]:


ax = sb.countplot(x='DeviceProtection', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[96]:


ax = sb.countplot(x='TechSupport', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[97]:


ax = sb.countplot(x='StreamingTV', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[98]:


ax = sb.countplot(x='StreamingMovies', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[99]:


ax = sb.countplot(x='Contract', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[100]:


ax = sb.countplot(x='HighCharge?', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[101]:


ax = sb.countplot(x='PaperlessBilling', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[102]:


ax = sb.countplot(x='Male?', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[103]:


ax = sb.countplot(x='Online Payment?', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[104]:


ax = sb.countplot(x='Techie', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[105]:


ax = sb.countplot(x='Port_modem', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[106]:


ax = sb.countplot(x='Tablet', hue='Churn', data=rawdata)
for container in ax.containers:
    ax.bar_label(container, padding = -15, color = 'white')


# In[107]:


sb.heatmap(rawdata.corr(), xticklabels=rawdata.columns, yticklabels=rawdata.columns)


# In[108]:


rawdata.corr()


# In[109]:


Corr_df=rawdata.corr()
Corr_df = Corr_df.sort_values('Churn', ascending=False)
Corr_df = Corr_df['Churn']
print(Corr_df)


# In[110]:


abs_corr=abs(Corr_df)
abs_corr = abs_corr.sort_values(ascending=False)
print(abs_corr)


# In[111]:


independent = rawdata.drop(['Churn'], axis=1)
y = rawdata['Churn']


# In[112]:


logisticRegr = LogisticRegression()
x_train, x_test, y_train, y_test = sk.model_selection.train_test_split(independent,
y, test_size = .2, random_state=3)
log1=logisticRegr.fit(x_train, y_train)
predictions = logisticRegr.predict(x_test)
score = logisticRegr.score(x_test, y_test)
print(score)


# In[113]:


logit_model=sm.Logit(y,independent)
result=logit_model.fit()
print(result.summary())


# In[114]:


cnf_matrix=metrics.confusion_matrix(y_test,predictions)


# In[115]:


class_names=[0,1]
fig, ax = mpp.subplots()
tick_marks = np.arange(len(class_names))
mpp.xticks(tick_marks, class_names)
mpp.yticks(tick_marks, class_names)
# create heatmap
sb.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
mpp.tight_layout()
mpp.title('Confusion matrix (All Variables)', y=1.1)
mpp.ylabel('Actual label')
mpp.xlabel('Predicted label')


# In[116]:


from sklearn.metrics import classification_report
target_names = ['Not Churned', 'Churned']
print(classification_report(y_test, predictions, target_names=target_names))


# In[117]:


ca = pr.CA(
    n_components = 35,
    n_iter = 2,
    copy = True
)
ca = ca.fit(rawdata)


# In[118]:


ca_eigenvalues = ca.eigenvalues_
ca_eigenvalues


# In[119]:


mpp.plot(np.arange(35), ca_eigenvalues, 'ro-')
mpp.title("Scree Plot")
mpp.xlabel("Principal Component")
mpp.ylabel("Eigenvalue")
mpp.show()


# In[120]:


kb = SelectKBest(chi2, k='all')
kb_fit = kb.fit(independent, y)
# print feature scores
for i in range(len(kb_fit.scores_)):
    print(' %s: %f' % (independent.columns[i], kb_fit.scores_[i]))


# In[121]:


Kdata = pd.DataFrame()
Kdata['feature'] = independent.columns[ range(len(kb_fit.scores_))]
Kdata['scores'] = kb_fit.scores_
Kdata = Kdata.sort_values(by='scores', ascending=True)
print(Kdata)


# In[122]:


df=rawdata[['High Bandwidth_GB_Year','HighCharge?','StreamingMovies','Contract','StreamingTV','MultipleLines','DSL','Techie','FiberOptic']]
df.info()


# In[123]:


logisticRegr = LogisticRegression()
x_train, x_test, y_train, y_test = sk.model_selection.train_test_split(df,
rawdata.Churn, test_size = .2, random_state=3)
logisticRegr.fit(x_train, y_train)
predictions2 = logisticRegr.predict(x_test)
score = logisticRegr.score(x_test, y_test)
print(score)


# In[124]:


logit_model=sm.Logit(rawdata.Churn,df)
result=logit_model.fit()
print(result.summary())


# In[125]:


df_matrix=metrics.confusion_matrix(y_test,predictions2)


# In[126]:


class_names=[0,1]
fig, ax = mpp.subplots()
tick_marks = np.arange(len(class_names))
mpp.xticks(tick_marks, class_names)
mpp.yticks(tick_marks, class_names)
sb.heatmap(pd.DataFrame(df_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
mpp.tight_layout()
mpp.title('Confusion matrix (Top 6 Variables)', y=1.1)
mpp.ylabel('Actual label')
mpp.xlabel('Predicted label')


# In[127]:


target_names = ['Not Churned', 'Churned']
print(classification_report(y_test, predictions2, target_names=target_names))


# In[ ]:




