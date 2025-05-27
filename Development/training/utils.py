import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np


def preprocess(df):
    """"
    Preprocesses and splits the dataset.

    Args:
        df: Dataframe with the data
    
    Returns:
        X_train
        X_test
        y_train
        y_test
    """
    # Drop irrelevant columns
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
