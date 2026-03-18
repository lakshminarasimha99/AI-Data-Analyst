import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

def predict_trends(filepath):
    df = pd.read_csv(filepath)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    predictions = {}
    
    if len(numeric_cols) == 0:
        return {"message": "No numeric columns for prediction"}
    
    for col in numeric_cols[:2]:  # First 2 numeric
        if len(df) < 3:  # Need data
            predictions[col] = "Insufficient data"
            continue
        
        X = np.arange(len(df)).reshape(-1, 1)
        y = df[col].fillna(df[col].mean()).values
        
        model = LinearRegression()
        model.fit(X, y)
        next_x = np.array([[len(df)]])
        next_val = model.predict(next_x)[0]
        
        predictions[col] = {
            "next_predicted": float(next_val),
            "trend": "up" if next_val > y[-1] else "down"
        }
    
    return predictions
