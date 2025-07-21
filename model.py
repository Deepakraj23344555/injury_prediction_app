import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Synthetic training data
df = pd.DataFrame({
    'distance': [5, 10, 15, 20, 25, 30],
    'intensity': [2, 4, 6, 8, 7, 9],
    'frequency': [1, 2, 3, 4, 5, 6],
    'duration': [30, 60, 90, 120, 150, 180],
    'previous_injuries': [0, 1, 0, 1, 0, 1],
    'chronic_conditions': [0, 0, 1, 0, 1, 1],
    'injury': [0, 1, 0, 1, 0, 1]
})

X = df.drop('injury', axis=1)
y = df['injury']

model = LogisticRegression()
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
