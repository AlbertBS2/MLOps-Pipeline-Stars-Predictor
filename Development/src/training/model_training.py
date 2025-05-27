import os
import joblib
import ray
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import preprocess, train_model

from ray import tune
from ray.tune import CLIReporter, with_parameters
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from xgboost import XGBRegressor

# ========== Load and Clean Data ==========
base_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "repo_data.csv"))
model_path = os.path.abspath(os.path.join(base_dir, "..", "..", "models", "new_model.pkl"))

X_train, X_val, y_train, y_val = preprocess(data_path, test_size=0.2, random_state=42)

# ========== Ray Tune Setup ==========
ray.init(ignore_reinit_error=True)

search_spaces = {
    "RandomForest": {
        "cls": RandomForestRegressor,
        "space": {
            "n_estimators": tune.choice([100, 150, 200]),
            "max_depth": tune.choice([5, 10, 15]),
            "min_samples_split": tune.choice([2, 4])
        }
    },
    "GradientBoosting": {
        "cls": GradientBoostingRegressor,
        "space": {
            "n_estimators": tune.choice([100, 150]),
            "learning_rate": tune.choice([0.05, 0.1]),
            "max_depth": tune.choice([3, 5, 7])
        }
    },
    "XGBoost": {
        "cls": XGBRegressor,
        "space": {
            "n_estimators": tune.choice([100, 150]),
            "max_depth": tune.choice([3, 6]),
            "learning_rate": tune.choice([0.05, 0.1]),
            "verbosity": 0
        }
    },
    "LinearRegression": {
        "cls": LinearRegression,
        "space": {}
    },
    "RidgeRegression": {
        "cls": Ridge,
        "space": {
            "alpha": tune.choice([0.1, 1.0, 10.0])
        }
    }
}

best_models = {}

for name, spec in search_spaces.items():
    print(f"Tuning {name}...")
    trainable = with_parameters(
        train_model,
        model_cls=spec["cls"],
        X_train=X_train,
        X_val=X_val,
        y_train=y_train,
        y_val=y_val
    )

    analysis = tune.run(
        trainable,
        config=spec["space"],
        num_samples=10 if spec["space"] else 1,
        metric="r2_score",
        mode="max",
        resources_per_trial={"cpu": 1},
        progress_reporter=CLIReporter(metric_columns=["r2_score"]),
        fail_fast=False
    )

    best_config = analysis.best_config
    best_model = spec["cls"](**best_config)
    best_model.fit(X_train, y_train)
    best_models[name] = best_model

# ========== Evaluation ==========
results = []
best_model = None
best_score = -np.inf

for name, model in best_models.items():
    preds = model.predict(X_val)
    r2 = r2_score(y_val, preds)
    mse = mean_squared_error(y_val, preds)
    mae = mean_absolute_error(y_val, preds)

    results.append({"Model": name, "R2": r2, "MSE": mse, "MAE": mae})

    if r2 > best_score:
        best_score = r2
        best_model = model

joblib.dump(best_model, model_path)

# ========== Plot Results ==========
print("\nModel Evaluation Results:")
for r in results:
    print(f"{r['Model']}: R2 = {r['R2']:.4f}, MSE = {r['MSE']:.2f}, MAE = {r['MAE']:.2f}")

plt.figure(figsize=(8, 5))
plt.bar([r['Model'] for r in results], [r['R2'] for r in results])
plt.ylabel("R² Score")
plt.title("Model Comparison with Ray Tune")
plt.ylim(0, 1)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
plt.savefig(os.path.abspath(os.path.join(base_dir, "model_comparison_plot.png")), dpi=300)

ray.shutdown()
