from flask import Flask, request, render_template
from github_api import extract_features
from predict_logic import predict_star_count, rank_predictions  # ✅ include both tasks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    predictions = []

    if request.method == "POST":
        task_results = []

        for i in range(1, 6):  # 5 GitHub repos
            repo_id = request.form.get(f"repo_{i}").strip()
            if not repo_id:
                predictions.append({"repo": f"Repository {i}", "stars": "Missing ID"})
                continue

            try:
                features = extract_features(repo_id)
                task = predict_star_count.delay(
                    features["commits"], features["forks"], features["watchers"]
                )
                task_results.append((repo_id, task))
            except Exception as e:
                predictions.append({"repo": repo_id, "stars": f"Error: {e}"})

        unsorted_predictions = []
        for repo_id, task in task_results:
            try:
                result = task.get(timeout=10)
                unsorted_predictions.append({"repo": repo_id, "stars": result})
            except Exception as e:
                unsorted_predictions.append({"repo": repo_id, "stars": f"Timeout/Error: {e}"})

        # ✅ DELEGATE SORTING TO CELERY
        sort_task = rank_predictions.delay(unsorted_predictions)
        predictions = sort_task.get(timeout=5)

    return render_template("index.html", predictions=predictions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
