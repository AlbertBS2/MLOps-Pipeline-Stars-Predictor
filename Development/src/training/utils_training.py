import sys
import pandas as pd
import numpy as np
from ray import tune
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


def preprocess(data, test_size=0.2, random_state=42):
    """
    Preprocesses and splits the dataset.

    Args:
        data (str): Path to the CSV file containing the dataset
        test_size (float): Proportion of the dataset to include in the test split
        random_state (int): Random seed for reproducibility
    
    Returns:
        X_train
        X_test
        y_train
        y_test
    """
    # Drop irrelevant columns
    df = pd.read_csv(data)
    drop_cols = ["full_name", "description", "created_at", "updated_at", "watchers_count", "language"]
    df_cleaned = df.drop(columns=drop_cols)

    # Fill NaN values with median
    for col in df_cleaned.select_dtypes(include=[np.number]).columns:
        df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)

    # Split into X and y
    X = df_cleaned.copy()
    y = X.pop("stargazers_count")

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test


def evaluate(model, X_test, y_test):
    """
    Evaluate an ML model on R2-Score.

    Args:
        model
        X_test
        y_test
    
    Returns:
        score
    """
    # Obtain predictions
    y_pred = model.predict(X_test, y_test)

    # Compute R2-Score
    score = r2_score(y_test, y_pred)

    return score


def train_model(config, model_cls, X_train, X_val, y_train, y_val):
    try:
        model = model_cls(**config)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        r2 = r2_score(y_val, preds)
        tune.report({"r2_score": r2})
    except Exception as e:
        tune.report({"r2_score": -1.0})
        print(f"Error: {e}", file=sys.stderr)
