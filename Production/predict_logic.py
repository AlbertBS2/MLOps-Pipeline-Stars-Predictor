import joblib
import numpy as np
from datetime import datetime
from celery_worker import celery

# Load the model once at module level to avoid reloading it on every prediction
model = joblib.load("best_model.pkl")

@celery.task
def predict_star_count(features):
    """
    Predict star count from a single list of features.
    """
    return int(model.predict(np.array([features]))[0])



@celery.task
def rank_predictions(predictions):
    return sorted(
        predictions,
        key=lambda x: x["stars"] if isinstance(x["stars"], int) else -1,
        reverse=True
    )
def extract_form_features(i, form):
    try:
        forks_count = int(form.get(f"forks_count_{i}", 0))
        size = int(form.get(f"size_{i}", 0))
        open_issues_count = int(form.get(f"open_issues_count_{i}", 0))
        full_name = form.get(f"full_name_{i}", f"Repository {i}")


        bool_fields = [
            "has_issues", "has_projects", "has_downloads", "has_wiki",
            "has_pages", "has_discussions", "archived"
        ]
        bool_values = [int(form.get(f"{field}_{i}") == "on") for field in bool_fields]

        features = [
            forks_count, size, open_issues_count
        ] + bool_values

        return full_name, features

    except Exception as e:
        return f"Repository {i}", f"Error: {e}"
