#import libraries 
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




data = pd.read_csv("ADS.csv")
display(data.head(7))

data.shape 
#Number of Instances (records in your data set): 292
#Number of Attributes (fields within each record): 21

# Number of records where individual's with ASD
n_asd_yes = len(data[data['Class'] == 'YES'])

#Number of records where individual's with no ASD
n_asd_no = len(data[data['Class'] == 'NO'])

# Total number of records
n_records = len(data.index)

#Percentage of individuals whose are with ASD
yes_percent = float(n_asd_yes) / n_records *100

# print("Individuals diagonised with ASD: ",n_asd_yes)
# print("Individuals not diagonised with ASD: ",n_asd_no)
# print("Percentage of individuals diagonised with ASD: ", yes_percent)

asd_data = pd.read_csv('ADS.csv', na_values=['?'])
asd_data.head()

asd_data.describe()

data.info()
#we have 10 categorical features

asd_data.info()
# Now we can see that missing values are randomly spread over the data set



#since the missing data seems randomly distributed, I go ahead and drop rows with missing data.
#If we could have fill with median values for 'NaN' instead of dropping them, but in this situation that is little complicated as I have lot of categorical colums with 'NaN'.

asd_data.loc[(asd_data['Age'].isnull()) |(asd_data['Gender'].isnull()) |(asd_data['Ethnicity'].isnull()) 
            |(asd_data['Jaundice_born'].isnull())|(asd_data['Autism'].isnull()) |(asd_data['Country'].isnull())
            |(asd_data['Used_app_before'].isnull())|(asd_data['result'].isnull())|(asd_data['Age_desc'].isnull())
            |(asd_data['Relation'].isnull())]


asd_raw = asd_data['Class']
features_raw = asd_data[['Age', 'Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 'result',
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']]

columns_names = ['Age', 'Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 'result',
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
numerical = ['Age', 'result']
categorical = ['Gender', 'Ethnicity', 'Jaundice_born', 'Autism', 'Country', 
                      'Used_app_before','Relation','A1_Score','A2_Score','A3_Score','A4_Score','A5_Score','A6_Score','A7_Score','A8_Score',
                      'A9_Score','A10_Score']

features_minmax_transform = pd.DataFrame(data = features_raw)
features_minmax_transform[numerical] = scaler.fit_transform(features_raw[numerical])
features_minmax_transform

display(features_minmax_transform.head(n = 5))


#One-hot encode the 'features_minmax_transform' data using pandas.get_dummies()
features_final = pd.get_dummies(features_minmax_transform)
display(features_final.head(5))


# Encode the 'all_classes_raw' data to numerical values
asd_classes = asd_raw.apply(lambda x: 1 if x == 'YES' else 0)



# Print the number of features after one-hot encoding
encoded = list(features_final.columns)
print("{} total features after one-hot encoding. ".format(len(encoded)))

# Uncomment the following line to see the encoded feature names
print(encoded)


from sklearn.model_selection import train_test_split

np.random.seed(1234)

X_train, X_test, y_train, y_test = train_test_split(features_final, asd_classes, train_size=0.80, random_state=1)


# Show the results of the split
print("Training set has {} samples.".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))
#asd_data

y_test[y_test==np.inf]=np.nan
y_test.fillna(y_test.mean(), inplace=True)

X_train[X_train==np.inf]=np.nan
X_train.fillna(X_train.mean(), inplace=True)

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


from sklearn.ensemble import RandomForestClassifier

ranfor = RandomForestClassifier(n_estimators=5, random_state=1)
ranfor.fit(X_train,y_train)
cv_scores = cross_val_score(ranfor, features_final, asd_classes, cv=10)
cv_scores.mean()


# calculate cross-validated AUC
from sklearn.model_selection import cross_val_score
cross_val_score(ranfor, features_final, asd_classes, cv=10, scoring='roc_auc').mean()


from sklearn.metrics import fbeta_score
predictions_test = ranfor.predict(X_test)
fbeta_score(y_test, predictions_test, average='binary', beta=0.5)
ranfor.predict([encoded_input_keys])


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

    if  f_prediction[0]== 1:
        return 1 # Autictic
    else:
        return 0 # N9t Autisitic

def count_a_scores(data):
    return sum(data[key] for key in data if key.startswith('A') and '_Score' in key)