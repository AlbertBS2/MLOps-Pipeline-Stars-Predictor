import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os


# Set paths
base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, '..', 'scraping', 'repo_data.csv')
model_path = os.path.join(base_dir, '..', 'new_model.pkl')

# Load the data
df = pd.read_csv(data_path)

X = df.copy()
y = X.pop("stargazers_count")

# Label encoding
label_encoder = LabelEncoder()
X_categorical = df.select_dtypes(include=['object']).apply(label_encoder.fit_transform)
X_numerical = df.select_dtypes(exclude=['object']).values
X = pd.concat([pd.DataFrame(X_numerical), X_categorical], axis=1).values

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Build and train the model
model = RandomForestRegressor(random_state=42, max_depth=30)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, model_path)
