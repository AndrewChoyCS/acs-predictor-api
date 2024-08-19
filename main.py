from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('playerPredictor.pkl')

# Load the one-hot encoded column names used during training
df = pd.read_csv('./player_stats.csv')
df = df.dropna()
X = pd.get_dummies(df[['Player', 'Map']], drop_first=True)

# Initialize the FastAPI app
app = FastAPI()

# Define the input data model
class PredictionRequest(BaseModel):
    player_name: str
    map_name: str

# API route to get predictions
@app.post("/predict/")
def predict(request: PredictionRequest):
    # Create an empty DataFrame with the same columns as the one-hot encoded training data
    input_vector = pd.DataFrame(0, index=[0], columns=X.columns)
    
    # Set the relevant player and map columns to 1
    player_column = f'Player_{request.player_name}'
    map_column = f'Map_{request.map_name}'
    
    if player_column in input_vector.columns:
        input_vector[player_column] = 1
    else:
        raise HTTPException(status_code=404, detail=f"Player '{request.player_name}' not found in training data.")
    
    if map_column in input_vector.columns:
        input_vector[map_column] = 1
    else:
        raise HTTPException(status_code=404, detail=f"Map '{request.map_name}' not found in training data.")
    
    # Make the prediction
    prediction = model.predict(input_vector)
    return {"predicted_acs": prediction[0][0]}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Player Performance Prediction API"}
