import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Create mock data
data = pd.DataFrame({
    "commits": [100, 150, 200, 250, 300, 400, 120, 180, 260, 310],
    "forks":   [10, 20, 25, 30, 40, 60, 15, 22, 33, 45],
    "watchers": [5, 8, 10, 12, 15, 18, 6, 9, 13, 16],
    "stars":   [50, 70, 90, 100, 120, 180, 65, 85, 110, 160]
})
# Features and target
X = data[["commits", "forks", "watchers"]]
y = data["stars"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("R^2 score:", r2_score(y_test, y_pred))  # Just for info

# Save model
joblib.dump(model, "best_model.pkl")
