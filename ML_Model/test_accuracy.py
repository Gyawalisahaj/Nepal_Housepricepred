import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.simplefilter("ignore")

df = pd.read_csv('nepal_homes_all_listings.csv')

def parse_price(x):
    if pd.isna(x) or not isinstance(x, str): return None
    x = x.strip().lower()
    if 'on call' in x or '/m' in x or '/y' in x or 'per month' in x: return None
    num_match = re.findall(r'\d+\.?\d*', x.replace(',', ''))
    if not num_match: return None
    val = float(num_match[0])
    if val <= 0: return None
    if 'cr' in x: return val
    elif 'lac' in x or 'lakh' in x: return val / 100.0
    elif 'k' in x or 'thousand' in x: return val / 10000.0
    else:
        if val < 1000: return val
        else: return val / 10000000.0

df['Price'] = df['Price'].apply(parse_price)
df = df.dropna(subset=['Price'])

df['ROAD ACCESS'] = df['ROAD ACCESS'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float).fillna(0)
df['PARKING'] = df['PARKING'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float).fillna(0)
df['BEDROOM'] = df['BEDROOM'].astype(str).str.replace(r'\+|-', '', regex=True).astype(float)
df['BATHROOM'] = df['BATHROOM'].astype(str).str.replace(r'\+|-', '', regex=True).astype(float)

df['LAND AREA'] = df['LAND AREA'].fillna(df['BUILTUP AREA']).dropna()
def convert_to_sqm(land_area):
    if pd.isna(land_area): return np.nan
    land_area = str(land_area).lower()
    conversion_factors = {"aana": 31.79, "paisa": 7.95, "dam": 1.99, "sq. ft.": 0.0929, "sq. m.": 1}
    total_sqm = 0
    land_area = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", str(land_area).lower()).strip()
    matches = re.findall(r"([\d]+(?:\.\d+)?)\s*(aana|paisa|dam|sq\. ft\.|sq\. m\.)?", land_area)
    if not matches: return np.nan
    for value, unit in matches:
        try:
            value = float(value)
            if unit in conversion_factors: total_sqm += value * conversion_factors[unit]
            else: total_sqm += value
        except ValueError: continue
    return total_sqm if total_sqm > 10 else np.nan

df["LAND AREA (sq m)"] = df["LAND AREA"].apply(convert_to_sqm)
df = df.dropna(subset=['LAND AREA (sq m)'])

def bhk_find(data):
    if pd.isna(data): return np.nan
    if data <= 30: return 2
    elif data <= 60: return 3
    elif data <= 90: return 4
    elif data <= 130: return 5
    else: return 6

df["BHK"] = df["BEDROOM"].fillna(df['LAND AREA (sq m)'].apply(bhk_find))
df['BATHROOM'] = df['BATHROOM'].fillna(df.BHK)

def split_capital_words(lst):
    if not isinstance(lst, str): return []
    return re.findall(r'[A-Z][a-z]*|\d+', lst)

df['Location'] = df['Location'].apply(split_capital_words)
df['Location'] = df['Location'].apply(lambda lst: lst[2:-2] if len(lst) >= 6 else lst)

def concatenate_if_three(lst):
    if isinstance(lst, list):
        if len(lst) >= 3: return [lst[0] + " " + lst[1], lst[2]]
        elif len(lst) == 2: return lst
        elif len(lst) == 1: return [np.nan, lst[0]]
    return [np.nan, np.nan]

df['Location'] = df['Location'].apply(concatenate_if_three)
df[['City', 'District']] = pd.DataFrame(df['Location'].tolist(), index=df.index)
df["Location"] = df["City"] + ", " + df["District"]
df["Location"] = df["Location"].fillna(df["District"]).fillna("Unknown")

location_counts = df['Location'].value_counts()
common_locations = location_counts[location_counts >= 5].index
df['Location'] = df['Location'].apply(lambda x: x if x in common_locations else 'Other')

df['Price_Per_Sqm'] = df['Price'] / df['LAND AREA (sq m)']

# Remove extreme 10% outliers
df = df[(df['Price_Per_Sqm'] > df['Price_Per_Sqm'].quantile(0.10)) & 
        (df['Price_Per_Sqm'] < df['Price_Per_Sqm'].quantile(0.90))]

df = df[(df['LAND AREA (sq m)'] > 10) & (df['LAND AREA (sq m)'] < 2000)]
df = df[(df['Price'] > 0.05) & (df['Price'] < 20)]

X = df[["ROAD ACCESS", "PARKING", "BATHROOM", "Location", "LAND AREA (sq m)", "BHK"]]
y = df['Price'] # predicting price directly or price_per_sqm
X = pd.get_dummies(X, columns=["Location"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=300, max_depth=20, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print("Predicting Price directly:")
print(f"R2: {r2_score(y_test, y_pred)}")

# Now try predicting Price_Per_Sqm
y_train_sqm = y_train / X_train['LAND AREA (sq m)']
y_test_sqm = y_test / X_test['LAND AREA (sq m)']

rf_sqm = RandomForestRegressor(n_estimators=300, max_depth=20, random_state=42, n_jobs=-1)
rf_sqm.fit(X_train, y_train_sqm)
y_pred_sqm = rf_sqm.predict(X_test)
y_pred_price = y_pred_sqm * X_test['LAND AREA (sq m)']

print("Predicting Price per SQM:")
print(f"R2: {r2_score(y_test, y_pred_price)}")
