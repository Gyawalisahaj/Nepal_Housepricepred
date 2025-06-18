from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
from predhou import PredHou
import pandas as pd

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('property_price_model.pkl')
train_columns = joblib.load('train_columns.pkl')

@app.get("/")
def root():
    return {"message": "Hello World"}

def preprocess_input(data: dict):
    input_df = pd.DataFrame([data])
    input_encoded = pd.get_dummies(input_df, columns=["FACING", "Location"], drop_first=True)
    input_encoded = input_encoded.reindex(columns=train_columns, fill_value=0)
    return input_encoded

def predict_price(data: dict):
    processed_data = preprocess_input(data)
    prediction = model.predict(processed_data)[0]
    return prediction

@app.post("/predict")
def predict(data: PredHou):
    data_dict = {
        "ROAD ACCESS": data.road_access,
        "FACING": data.facing,
        "PARKING": data.parking,
        "BATHROOM": data.bathroom,
        "Location": data.location,
        "LAND AREA (sq m)": data.land_area_sq_m,
        "BHK": data.bhk
    }

    predicted_price = predict_price(data_dict)
    return {"predicted_price": predicted_price}
