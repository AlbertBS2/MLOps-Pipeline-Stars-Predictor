import joblib
import numpy as np

model = joblib.load("best_model.pkl")

def predict_star_count(commits, forks, watchers):
    features = np.array([[commits, forks, watchers]])
    return int(model.predict(features)[0])

