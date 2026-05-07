#!/usr/bin/env python
# coding: utf-8
Importing python libaries
# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

import os
import warnings
import random
import joblib


# In[2]:


warnings.simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", RuntimeWarning)


# In[73]:


df = pd.read_csv('nepal_homes_all_listings.csv')
df.head()

Working with RoadAccess (Distance from house)
# In[4]:


df['ROAD ACCESS'] = df['ROAD ACCESS'].str.extract(r'(\d+\.?\d*)')


df['ROAD ACCESS'] = df['ROAD ACCESS'].astype(float)
df["ROAD ACCESS"] = df['ROAD ACCESS'].fillna(random.choice(df['ROAD ACCESS']))
df['ROAD ACCESS'].isnull().sum()

Working with Facing and Parking
# In[5]:


df["FACING"] = df['FACING'].fillna("N/A")
df['FACING'].isnull().sum()


# In[6]:


df['PARKING'] = df['PARKING'].str.extract(r'(\d+\.?\d*)')
df


# In[7]:


df['PARKING'] = df['PARKING'].fillna(1)


# In[8]:


df['PARKING'].replace('', np.nan, inplace=True)
df['PARKING'].isnull().sum()


# In[9]:


df['BEDROOM'] = df['BEDROOM'].str.replace(r'\+|-', '', regex=True).astype(float)


# In[10]:


df['BATHROOM'] = df['BATHROOM'].str.replace(r'\+|-', '', regex = True).astype(float)


# In[11]:


df

Land Area Data Cleaning and working with null values
# In[12]:


df['LAND AREA'] = df['LAND AREA'].fillna(df['BUILTUP AREA'])


# In[13]:


df['LAND AREA'].isnull().sum()


# In[14]:


df["LAND AREA"]= df["LAND AREA"].dropna()


# In[15]:


df['LAND AREA'] = df['LAND AREA'].str.strip('()').str.split(' ')


# In[16]:


def convert_to_sqm(land_area):
    if isinstance(land_area, list): 
        land_area = " ".join(map(str, land_area))  

    if not isinstance(land_area, str) or not land_area.strip():  
        return np.nan 

    
    conversion_factors = {
        "aana": 31.79,
        "paisa": 7.95,
        "dam": 1.99
    }

    total_sqm = 0

   
    land_area = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", str(land_area).lower()).strip()

    
    matches = re.findall(r"([\d]+(?:\.\d+)?)\s*(aana|paisa|dam)?", land_area)

    if not matches:
        return np.nan  

    for value, unit in matches:
        try:
            value = float(value)  
            if unit in conversion_factors:
                total_sqm += value * conversion_factors[unit]  
            else:
                total_sqm += value  
        except ValueError:
            continue  

    return total_sqm if total_sqm > 30 else np.nan  


df["LAND AREA (sq m)"] = df["LAND AREA"].apply(convert_to_sqm)


print(df[["LAND AREA", "LAND AREA (sq m)"]].head())


# In[17]:


df['LAND AREA (sq m)']

BHK and Bathrooms
# In[18]:


def bhk_find(data):
    if pd.isna(data):  
        return np.nan 
    
    if data <= 30:
        return 2
    elif data <= 60:
        return 3
    elif data <= 90:
        return 4
    elif data <= 130:
        return 5
    elif data > 130:
        return 6
    else:
        return np.nan 

df["BHK"] = df["BEDROOM"]
df['BHK'] = df['BHK'].fillna(df['LAND AREA (sq m)'].apply(bhk_find))



# In[19]:


df['BHK'].isnull().sum()


# In[20]:


df = df.dropna(subset=['LAND AREA (sq m)'])
#df1 = df1.dropna(subset=['Price'])


# In[21]:


df['BATHROOM'] = df['BATHROOM'].fillna(df.BHK +df.FLOOR)
df['BATHROOM'] = df['BATHROOM'].fillna(df.BHK +1)


# In[22]:


df.isnull().sum()

Working with locations
# In[23]:


df['Location'] = df['Location'].str.strip('()').str.split(' ')
df


# In[24]:


def split_capital_words(lst):
    if not isinstance(lst, list):  
        return []
    
    new_list = []
    for item in lst:
        if isinstance(item, str):  
            words = re.findall(r'[A-Z][a-z]*|\d+', item)  
            new_list.extend(words)
        else:
            new_list.append(item)  
            
    return new_list

df['Location'] = df['Location'].apply(split_capital_words)


# In[25]:


def modify_list(lst):
    if isinstance(lst, list) and len(lst) == 6:  
        return lst[2:-2]  
    return lst  

df['Location'] = df['Location'].apply(modify_list)


# In[26]:


df.isnull().sum()


# In[27]:


df.describe()


# In[28]:


def concatenate_if_three(lst):
    if isinstance(lst, list):
        if len(lst) == 3:
            return [lst[0] + " " + lst[1], lst[2]]  
        elif len(lst) == 2:
            return lst 
        elif len(lst) == 1:
            return [np.nan, lst[0]]  
        else:
            return [np.nan, np.nan]
    return [np.nan, np.nan]

df['Location'] = df['Location'].apply(concatenate_if_three)

df[['City', 'District']] = pd.DataFrame(df['Location'].tolist(), index=df.index)


# In[29]:


df['District'].unique()


# In[30]:


df['City'].unique()


# In[31]:


df.drop(['FLOOR', 'BEDROOM', 
                'FURNISH STATUS', 'LAND AREA', 'BUILT YEAR', 'BUILTUP AREA',  'Kitchen'],axis = 1, inplace=True)


# In[32]:


df["Location"] = df["City"] + ", " + df["District"]


# In[33]:


df["Location"] = df["Location"].fillna(random.choice(df["District"].dropna().tolist()))


# In[34]:


df = df.drop(columns=['Living ', 'City','District'])

Working with price 
# In[35]:


df['Price'].unique


# In[36]:


def strrem(x):
    if isinstance(x, str):
        num = re.findall(r'\d+\.?\d*', x.replace(',', ''))
        if num:
            value = float(num[0])
            return value if value < 100 else value / 1e7  
        else:
            return None
    elif isinstance(x, (int, float)):
        return x if x < 100 else x / 1e7
    else:
        return None


df['Price'] = df['Price'].apply(strrem)

df['Price']


# In[37]:


X_data = df.drop(columns=["FACING", "Price", "Location"])
df


# In[38]:


dfprice = df.dropna(subset=["Price"])
X1 = dfprice[['LAND AREA (sq m)','BHK']]
y1 = dfprice["Price"]


# In[39]:


X1.isnull().sum()


# In[40]:


from sklearn.model_selection import train_test_split
X1_train, X1_test, y1_train, y1_test = train_test_split(
    X1, y1, test_size=0.33, random_state=42)


# In[41]:


from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X1_train, y1_train)


# In[42]:


y1_pred = model.predict(X1_test) 


# In[43]:


X_data =  df[['LAND AREA (sq m)','BHK']]


# In[44]:


y_pricedata =  model.predict(X_data)


# In[45]:


y_pricedata_series = pd.Series(y_pricedata, index=df.index)
df['Price'] = df['Price'].fillna(y_pricedata_series)


# In[75]:


def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    initial_shape = df.shape[0]
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df_filtered



print("Outliers removed. New dataset size:", df.shape)


# In[47]:


df.describe()


# In[48]:


df['Price'].unique()


# In[49]:


sns.lineplot(data=df, x="LAND AREA (sq m)", y="Price")
plt.title("Land area in sq m vs Price")


# In[50]:


df.isnull().sum()


# In[51]:


sns.lineplot(data=df, x="BHK", y="Price")
plt.title("BHK vs Price")


# In[52]:


df["log_sqft"] = np.log1p(df["LAND AREA (sq m)"])


# In[53]:


X = df[["ROAD ACCESS", "FACING", "PARKING", "BATHROOM", "Location", "LAND AREA (sq m)", "BHK"]]
y = df["Price"]
X = pd.get_dummies(X, columns=["FACING", "Location"], drop_first=True)
train_columns = X.columns

 Predict house price with RandomForestRegressor
# In[54]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[55]:


from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

param_grid = {
    "n_estimators": [100, 500, 1000],
    "max_depth": [10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
}

rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(rf, param_grid, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1)
grid_search.fit(X_train, y_train)


# In[67]:


y3_pred = grid_search.predict(X_test)
y3_pred


# In[68]:


from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
mae = mean_absolute_error(y_test, y3_pred)
print(f"Mean Absolute Error: {mae}")
print("Mean Squared Error:", mean_squared_error(y_test, y3_pred))
print("R2 Score:", r2_score(y_test, y3_pred))


# In[72]:


# If your data was preprocessed with get_dummies, make sure to pass those column names here
best_model = grid_search.best_estimator_
feat_importances = pd.Series(best_model.feature_importances_, index=train_columns)

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x=feat_importances, y=feat_importances.index, palette="crest")
plt.title("Feature Importance of Best Random Forest Model")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()


# In[69]:


plt.figure(figsize=(12, 8))
sns.regplot(x=y_test, y=y3_pred, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.xlabel("Actual House Prices")
plt.ylabel("Predicted House Prices")
plt.title("Actual vs Predicted House Prices")
plt.show()


# In[59]:


def prepare_input(location, facing, parking, sqft, bath, bhk, road_access):
    input_dict = {
        "ROAD ACCESS": road_access,
        "FACING": facing,
        "PARKING": parking,
        "BATHROOM": bath,
        "Location": location,
        "LAND AREA (sq m)": sqft,
        "BHK": bhk,
    }
    input_df = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=train_columns, fill_value=0)

    return input_encoded

def predict_price(location, facing, parking, sqft, bath, bhk, road_access):
    input_df = prepare_input(location, facing, parking, sqft, bath, bhk, road_access)
    price = grid_search.predict(input_df)[0]
    return price


print()


# In[66]:


price = predict_price("Lalitpur", "South", 15, 700, 8, 3, 2)
print("Predicted price Rs:", price,"Cr")


# In[61]:


joblib.dump(grid_search.best_estimator_, 'property_price_model.pkl')
joblib.dump(train_columns, 'train_columns.pkl')



# In[64]:


df["Price"].describe()


# In[65]:


import json


loc = df["Location"].unique().tolist()

# Save to JSON
with open("locations.json", "w") as f:
    json.dump(loc, f)


# In[ ]:





# In[63]:


df['FACING'].unique()

