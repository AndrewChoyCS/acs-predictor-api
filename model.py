import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
import pandas as pd
import pickle
import joblib

df = pd.read_csv('./player_stats.csv')
df = df.dropna()
rows_with_nulls = df[df.isnull().any(axis=1)]['Game ID'].tolist()
finalData = df[~df['Game ID'].isin(rows_with_nulls)]
# print(finalData.shape)

X = pd.get_dummies(df[['Player', 'Map']], drop_first=True) #This one hot encodes them
# X = pd.get_dummies(df[['Player']], drop_first=True) #This one hot encodes them
print(X.columns)

Y = df[['ACS']].astype(int)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.20, random_state=42)
# print(X_train)


model = LinearRegression().fit(X_train, Y_train)
# Y_hat = model.predict(X_test)
# RSME = root_mean_squared_error(Y_hat, Y_test)
# print(RSME)
modelScore = model.score(X_test, Y_test)
print(modelScore)

with open('playerPredictor.pkl', 'wb') as f:
    pickle.dump(model, f)

modelTest = joblib.load('playerPredictor.pkl')

# User-friendly prediction function
def predict_for_player_and_map(player_name, map_name):
    # Create an empty DataFrame with the same columns as the one-hot encoded training data
    input_vector = pd.DataFrame(0, index=[0], columns=X.columns)
    
    # Set the relevant player and map columns to 1
    player_column = f'Player_{player_name}'
    map_column = f'Map_{map_name}'
    
    if player_column in input_vector.columns:
        input_vector[player_column] = 1
    else:
        raise ValueError(f"Player '{player_name}' not found in training data.")
    
    if map_column in input_vector.columns:
        input_vector[map_column] = 1
    else:
        raise ValueError(f"Map '{map_name}' not found in training data.")
    
    # Make the prediction
    prediction = modelTest.predict(input_vector)
    return prediction[0][0]

# Example usage
player_name = 'TenZ'  # Replace with an actual player name from your data
map_name = 'Ascent'       # Replace with an actual map name from your data

try:
    prediction = predict_for_player_and_map(player_name, map_name)
    print(f'Predicted ACS for {player_name} on {map_name}: {prediction}')
except ValueError as e:
    print(e)