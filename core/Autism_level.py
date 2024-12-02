#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
import time as time
import os
from IPython.display import display # Allows the use of display() for DataFrame

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder




#pretty display for notebooks
get_ipython().run_line_magic('matplotlib', 'inline')

data = pd.read_csv("ADS.csv")
display(data.head(7))


# In[2]:


asd_data = pd.read_csv('ADS.csv', na_values=['?'])
asd_data.head()


# In[3]:


def assign_severity(row):
    if row["Class"] == "NO":
        return "no_Autism"
    elif row["result"] < 6:
        return "Mild"
    elif 6 <= row["result"] < 8:
        return "Medium"
    else:
        return "Severe"

# Apply the function to create a new column
asd_data["Severity"] = asd_data.apply(assign_severity, axis=1)
label_encoder = LabelEncoder()
asd_data['Severity_encoded'] = label_encoder.fit_transform(asd_data['Severity'])


# In[4]:


asd_data


# In[5]:


asd_classes = asd_data['Severity_encoded']
asd_data = asd_data.drop(columns=['Class','Severity', 'Severity_encoded'])


# In[6]:


features_raw = asd_data[['Age', 'Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 'result',
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']]
columns_names = ['Age', 'Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 'result',
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']


# In[7]:


numerical = ['Age', 'result']
categorical = ['Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']


# In[ ]:





# In[8]:


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

features_minmax_transform = pd.DataFrame(data = features_raw)
features_minmax_transform[numerical] = scaler.fit_transform(features_raw[numerical])
features_minmax_transform

display(features_minmax_transform.head(n = 5))


# In[9]:


features_final = pd.get_dummies(features_minmax_transform)
display(features_final.head(5))

encoded = list(features_final.columns)
print("{} total features after one-hot encoding. ".format(len(encoded)))

# Uncomment the following line to see the encoded feature names
print(encoded)


# In[10]:


from sklearn.model_selection import train_test_split

np.random.seed(1234)

X_train, X_test, y_train, y_test = train_test_split(features_final, asd_classes, train_size=0.80, random_state=1)


# Show the results of the split
print("Training set has {} samples.".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))
X_train


# In[11]:


y_test[y_test==np.inf]=np.nan
y_test.fillna(y_test.mean(), inplace=True)

X_train[X_train==np.inf]=np.nan
X_train.fillna(X_train.mean(), inplace=True)


# In[12]:


def encode_user_input(user_input):
    encoded_input = {}
    
    # Map direct values
    encoded_input['Age'] = user_input['Age']
    encoded_input['result'] = user_input['Result']
    for i in range(1, 11):
        encoded_input[f"A{i}_Score"] = user_input[f"A{i}_Score"]
    
    # Encode gender
    encoded_input['Gender_f'] = 1 if user_input['Gender'] == 'Female' else 0
    encoded_input['Gender_m'] = 1 if user_input['Gender'] == 'Male' else 0
    
    # Encode ethnicity
    ethnicity_list = [
        "Middle Eastern", "South Asian", "Asian", "Black", "Hispanic", 
        "Latino", "Others", "Pasifika", "Turkish", "White-European"
    ]
    for eth in ethnicity_list:
        encoded_input[f"Ethnicity_{eth.replace(' ', '_')}"] = 1 if user_input['Ethnicity'] == eth else 0
    
    # Encode jaundice
    encoded_input['Jaundice_born_no'] = 1 if user_input['Jaundice_Born'] == 'No' else 0
    encoded_input['Jaundice_born_yes'] = 1 if user_input['Jaundice_Born'] == 'Yes' else 0
    
    # Encode autism
    encoded_input['Autism_no'] = 1 if user_input['Autism'] == 'No' else 0
    encoded_input['Autism_yes'] = 1 if user_input['Autism'] == 'Yes' else 0
    
    # Encode country
    countries = [
        'Costa Rica', 'Isle of Man', 'New Zealand', 'Saudi Arabia', 
        'South Africa', 'South Korea', 'U.S. Outlying Islands', 'United Arab Emirates', 
        'United Kingdom', 'United States', 'Afghanistan', 'Argentina', 'Armenia', 
        'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brazil', 
        'Bulgaria', 'Canada', 'China', 'Egypt', 'Europe', 'Georgia', 'Germany', 
        'Ghana', 'India', 'Iraq', 'Ireland', 'Italy', 'Japan', 'Jordan', 'Kuwait', 
        'Latvia', 'Lebanon', 'Libya', 'Malaysia', 'Malta', 'Mexico', 'Nepal', 
        'Netherlands', 'Nigeria', 'Oman', 'Pakistan', 'Philippines', 'Qatar', 
        'Romania', 'Russia', 'Sweden', 'Syria', 'Turkey'
    ]
    for country in countries:
        encoded_input[f"Country_{country.replace(' ', '_')}"] = 1 if user_input['Country'] == country else 0
    
    # Encode app usage
    encoded_input['Used_app_before_no'] = 1 if user_input['Used_App_Before'] == 'No' else 0
    encoded_input['Used_app_before_yes'] = 1 if user_input['Used_App_Before'] == 'Yes' else 0
    
    # Encode relation
    relations = ["Health care professional", "Parent", "Relative", "Self"]
    for rel in relations:
        encoded_input[f"Relation_{rel.replace(' ', '_')}"] = 1 if user_input['Relation'] == rel else 0
    
    # Ensure 87 features: Added feature for the relation "Self" twice
    encoded_input['Relation_self'] = 1 if user_input['Relation'] == 'Self' else 0

    # Return the list of keys instead of dictionary
    return list(encoded_input.values())

# Example user input
user_input = {
    'Age': 25,
    'Result': 6,
    'A1_Score': 1,
    'A2_Score': 0,
    'A3_Score': 1,
    'A4_Score': 0,
    'A5_Score': 1,
    'A6_Score': 1,
    'A7_Score': 0,
    'A8_Score': 1,
    'A9_Score': 0,
    'A10_Score': 1,
    'Gender': 'Male',
    'Ethnicity': 'Middle Eastern',
    'Jaundice_Born': 'Yes',
    'Autism': 'No',
    'Country': 'Egypt',
    'Used_App_Before': 'No',
    'Relation': 'Parent'
}

# Encode the input and print the keys
encoded_input_keys = encode_user_input(user_input)
print(encoded_input_keys)
print(f"Number of features: {len(encoded_input_keys)}")


# In[13]:


from sklearn.ensemble import RandomForestClassifier

ranfor = RandomForestClassifier(n_estimators=5, random_state=1)
ranfor.fit(X_train,y_train)
cv_scores = cross_val_score(ranfor, features_final, asd_classes, cv=10)
cv_scores.mean()


# In[14]:


from sklearn.metrics import fbeta_score
predictions_test = ranfor.predict(X_test)
fbeta_score(y_test, predictions_test, average='macro', beta=0.5)


# In[15]:

import random
def AI(user_input):
    user_input['Age'] = 7
    user_input['Country'] = "Egypt"
    user_input['Used_App_Before'] = "No"
    user_input['Relation'] = "Parent"
    user_input['Ethnicity'] = "Middle Eastern"
    user_input['Jaundice_Born'] = "No"
    user_input['Gender'] = random.choice(["Male", "Female"])
    user_input['Autism'] = random.choice(["Yes", "No"])
    user_input['result'] = sum(data[key] for key in data if key.startswith('A') and key[-1].isdigit())
    data_encoded =[encode_user_input(user_input)]
    f_prediction = ranfor.predict(data_encoded)

    return f_prediction[0]


AI(user_input = {
    'Age': 25,
    'Result': 6,
    'A1_Score': 1,
    'A2_Score': 0,
    'A3_Score': 1,
    'A4_Score': 0,
    'A5_Score': 1,
    'A6_Score': 1,
    'A7_Score': 0,
    'A8_Score': 1,
    'A9_Score': 0,
    'A10_Score': 1,
    'Gender': 'Male',
    'Ethnicity': 'Middle Eastern',
    'Jaundice_Born': 'Yes',
    'Autism': 'No',
    'Country': 'Egypt',
    'Used_App_Before': 'No',
    'Relation': 'Parent'
})


# In[16]:


X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(features_raw, asd_classes, train_size=0.80, random_state=1)


# In[17]:


X_train_1


# In[18]:


numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # Handle NaN and inf
    ('scaler', MinMaxScaler())                    # Normalize the data
])


# In[19]:


categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing categorical values
    ('onehot', OneHotEncoder(handle_unknown='ignore'))     # One-hot encode
])


# In[20]:


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical),
        ('cat', categorical_transformer, categorical)
    ]
)


# In[21]:


pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', ranfor)
])


# In[22]:


pipe_predict = pipeline.fit(X_train_1,y_train_1)
input_data = pd.DataFrame(
    [[25, 'Male', 'Middle Eastern', 'Yes', 'No', 'Egypt', 'No', 'Parent',9, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]],
    columns= ['Age','Gender','Ethnicity','Jaundice_born','Autism','Country','Used_app_before','Relation','result','A1_Score','A2_Score'	,'A3_Score','A4_Score',	'A5_Score','A6_Score','A7_Score','A8_Score','A9_Score',	'A10_Score']
)
check = pipe_predict.predict(input_data)


# In[23]:


if check[0] == 0 :
    print("No Autism")
elif check[0] == 1 :
    print("mild")
elif check[0] == 2 :
    print("moderate")
else :
    print("severe")


# In[24]:


import modelbit
mb = modelbit.login()


# In[25]:


def prediction1(Age,Gender,Ethinicity,jaudice,Autism,Country,used_app,Relation,Result,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10):
    data = pd.DataFrame([[Age,Gender,Ethinicity,jaudice,Autism,Country,used_app,Relation,Result,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10]],
                       columns= ['Age','Gender','Ethnicity','Jaundice_born','Autism','Country','Used_app_before','Relation','result','A1_Score','A2_Score'	,'A3_Score','A4_Score',	'A5_Score','A6_Score','A7_Score','A8_Score','A9_Score',	'A10_Score'])
    predict = pipe_predict.predict(data)
    if check[0] == 0 :
        final_predict = "No_Autism"
    elif check[0] == 1 :
         final_predict = "mild"
    elif check[0] == 2 :
         final_predict = "moderate"
    else :
        final_predict = "severe"

    return {
        "prediction is":final_predict
    }
mb.deploy(prediction1)


# In[26]:


import requests
import json

# Define the input data correctly
input_data = {
    "data":  [25, 'Male', 'Middle Eastern', 'Yes', 'No', 'Egypt', 'No', 'Parent',6, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
}

# Define the URL (replace <your-workspace-url> with the correct URL)
url = "https://ahmedmostafa.us-east-2.aws.modelbit.com/v1/prediction1/latest"

# Make the POST request
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    json = input_data
)
response_json = response.json()

# Check response
print(json.dumps(response_json, indent=4))


# In[ ]:




