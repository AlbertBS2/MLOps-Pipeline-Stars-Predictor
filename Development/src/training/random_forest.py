from sklearn.ensemble import RandomForestRegressor
from utils_training import preprocess
import joblib
import os
from sklearn.metrics import r2_score


# Set paths
base_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'data', 'repo_data.csv'))
model_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'models', 'new_model.pkl'))

# Preprocess and split the data
X_train, X_test, y_train, y_test = preprocess(data_path)

# Define the model
model = RandomForestRegressor(random_state=42)

# Train the model
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(r2_score(y_test, y_pred))

# Save the model
joblib.dump(model, model_path)
