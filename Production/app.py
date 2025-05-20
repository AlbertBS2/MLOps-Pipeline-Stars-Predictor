from flask import Flask, request, render_template
from github_api import extract_features
from predict_logic import predict_star_count

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    predictions = []
    if request.method == "POST":
        for i in range(1, 6):  # 5 GitHub repos
            repo_id = request.form.get(f"repo_{i}").strip()
            if not repo_id:
                predictions.append({"repo": f"Repository {i}", "stars": "Missing ID"})
                continue
            try:
                # features = extract_features(repo_id)
                # predicted = predict_star_count(features["commits"], features["forks"], features["watchers"])
                predicted = predict_star_count(1, 2, 3)
                predictions.append({"repo": repo_id, "stars": predicted})
            except Exception as e:
                predictions.append({"repo": repo_id, "stars": f"Error: {e}"})

        # Rank by predicted stars
        predictions.sort(key=lambda x: x["stars"] if isinstance(x["stars"], int) else -1, reverse=True)

    return render_template("index.html", predictions=predictions)

if __name__ == "__main__":
    app.run(debug=True)
