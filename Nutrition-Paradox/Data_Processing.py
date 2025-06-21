#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import requests


# In[7]:


adult_obesity_json = requests.get("https://ghoapi.azureedge.net/api/NCD_BMI_30C").json()
child_obesity_json = requests.get("https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C").json()
adult_underweight_json = requests.get("https://ghoapi.azureedge.net/api/NCD_BMI_18C").json()
child_thinness_json = requests.get("https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C").json()


# In[9]:


adult_obesity = pd.json_normalize(adult_obesity_json['value'])
child_obesity = pd.json_normalize(child_obesity_json['value'])
adult_underweight = pd.json_normalize(adult_underweight_json['value'])
child_thinness = pd.json_normalize(child_thinness_json['value'])


# In[11]:


adult_obesity['age_group'] = 'Adult'
child_obesity['age_group'] = 'Child/Adolescent'
adult_underweight['age_group'] = 'Adult'
child_thinness['age_group'] = 'Child/Adolescent'


# In[13]:


df_obesity = pd.concat([adult_obesity, child_obesity], ignore_index=True)
df_malnutrition = pd.concat([adult_underweight, child_thinness], ignore_index=True)


# In[15]:


df_obesity['TimeDim'] = pd.to_numeric(df_obesity['TimeDim'] , errors = 'coerce')
df_malnutrition['TimeDim'] = pd.to_numeric(df_malnutrition['TimeDim'] , errors = 'coerce')


# In[17]:


df_obesity = df_obesity[(df_obesity['TimeDim'] >= 2012) &  (df_obesity['TimeDim'] <= 2022)]
df_malnutrition = df_malnutrition[(df_malnutrition['TimeDim'] >= 2012) &  (df_malnutrition['TimeDim'] <= 2022)]


# In[19]:


columns_needed = [
    'ParentLocation', 
    'Dim1', 
    'TimeDim',
    'Low', 
    'High', 
    'NumericValue', 
    'SpatialDim',
    'age_group'
]

df_obesity = df_obesity[columns_needed].copy()
df_malnutrition = df_malnutrition[columns_needed].copy()


# In[21]:


rename_columns_map = {
    'TimeDim' : 'Year',
    'Dim1' : 'Sex',
    'NumericValue' : 'Mean_Estimate',
    'Low' : 'LowerBound',
    'High' : 'UpperBound',
    'ParentLocation' : 'Region',
    'SpatialDim' : 'Country',
    'age_group' : 'Age_Group'
}

df_obesity.rename(columns=rename_columns_map, inplace=True)
df_malnutrition.rename(columns=rename_columns_map, inplace=True)


# In[23]:


df_obesity['Sex'].unique()


# In[25]:


df_malnutrition['Sex'].unique()


# In[27]:


gender_map = {
    'SEX_MLE' : 'Male',
    'SEX_FMLE' : 'Female',
    'SEX_BTSX' : 'Both'
}

df_obesity['Sex'] = df_obesity['Sex'].map(gender_map).fillna('Other')
df_malnutrition['Sex'] = df_malnutrition['Sex'].map(gender_map).fillna('Other')


# In[29]:


get_ipython().system('pip install pycountry')
import pycountry


# In[31]:


special_cases = {
    'GLOBAL' : 'Global',
    'WB_LMI' : 'Low & Middle Income',
    'WB_HI' : 'High Income',
    'WB_LI' : 'Low Income',
    'EMR' : 'Eastern Mediterranean Region',
    'EUR' : 'Europe',
    'AFR' : 'Africa',
    'SEAR' : 'South-East Asia Region',
    'WPR' : 'Western Pacific Region',
    'AMR' : 'Americas Region',
    'WB_UMI' : 'Upper Middle Income'
}

def convert_code_to_name(code):
    try:
        country = pycountry.countries.get(alpha_3=code)
        if country:
            return country.name
        elif code in special_cases:
            return special_cases[code]
        else:
            return 'Unknown'
    except:
        return 'Unknown'

df_obesity['Country'] = df_obesity['Country'].apply(convert_code_to_name)
df_malnutrition['Country'] = df_malnutrition['Country'].apply(convert_code_to_name)


# In[33]:


df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']
df_malnutrition['CI_Width'] = df_malnutrition['UpperBound'] - df_malnutrition['LowerBound']


# In[35]:


def get_obesity_level(numeric_value):
    if numeric_value >= 30:
        return 'High'
    elif 25 <= numeric_value <= 29.9:
        return 'Moderate'
    elif numeric_value < 25:
        return 'Low'
    else:
        return 'Unknown'

df_obesity['obesity_level'] = df_obesity['Mean_Estimate'].apply(get_obesity_level)

def get_malnutrition_level(numeric_value):
    if numeric_value >= 20:
        return 'High'
    elif 10 <= numeric_value <= 19.9:
        return 'Moderate'
    elif numeric_value < 10:
        return 'Low'
    else:
        return 'Unknown'

df_malnutrition['malnutrition_level'] = df_malnutrition['Mean_Estimate'].apply(get_malnutrition_level)


# In[37]:


df_obesity.head()


# In[39]:


df_malnutrition.head()


# In[ ]:




