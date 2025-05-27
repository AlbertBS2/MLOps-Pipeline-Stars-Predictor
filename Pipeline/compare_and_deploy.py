# This script compares the challenger and the champion models.
# If the challenger model obtains an increase in the R2-Score, it is deployed into production

import os
import shutil
import joblib
import pandas as pd
from Development.src.training.utils import fetch_and_clean_data
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


# Paths
base_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(base_dir, '..', 'Development', 'data', 'repo_data.csv'))
challenger_model_path = os.path.abspath(os.path.join(base_dir, '..', 'Development', 'models', 'new_model.pkl'))
champion_model_path = os.path.abspath(os.path.join(base_dir, '..', 'Production', 'best_model.pkl'))

# Load models
challenger_model = joblib.load(challenger_model_path)
champion_model = joblib.load(champion_model_path)

# Load and clean data
data = fetch_and_clean_data(data_path)
X = data.drop(columns=["stargazers_count"])
y = data["stargazers_count"]

# Extract test data
_, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Evaluate the models
new_r2 = r2_score(y_test, challenger_model.predict(X_test))
old_r2 = r2_score(y_test, champion_model.predict(X_test))

print(f"New R²: {new_r2}, Old R²: {old_r2}")

# Compare and deploy
if new_r2 > old_r2:
    print("New model is better. Deploying...")
    shutil.copy(challenger_model_path, champion_model_path)

else:
    print("Old model is still better. No changes made.")
