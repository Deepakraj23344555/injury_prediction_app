import pandas as pd

def preprocess_input(distance, intensity, frequency, duration, prev_injuries, chronic_cond):
    return pd.DataFrame({
        'distance': [distance],
        'intensity': [intensity],
        'frequency': [frequency],
        'duration': [duration],
        'previous_injuries': [1 if prev_injuries == "Yes" else 0],
        'chronic_conditions': [1 if chronic_cond == "Yes" else 0]
    })
