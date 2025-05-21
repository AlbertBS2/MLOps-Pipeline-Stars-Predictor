import joblib
import numpy as np
from celery_worker import celery

def loadmodel():
    # Load the pre-trained model
    # This should be the path to your model file
    # Ensure that the model file is in the same directory as this script or provide the full path
    model = joblib.load("best_model.pkl")
    return model

@celery.task
def predict_star_count(commits, forks, watchers):
    # Load the model
    model = loadmodel()
    features = np.array([[commits, forks, watchers]])
    return int(model.predict(features)[0])



@celery.task
def rank_predictions(predictions):
    """
    Takes a list of {"repo": ..., "stars": ...} and returns them ranked by stars descending.
    """
    sorted_predictions = sorted(
        predictions,
        key=lambda x: x["stars"] if isinstance(x["stars"], int) else -1,
        reverse=True
    )
    return sorted_predictions
