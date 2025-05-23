from flask import Flask, request, render_template
from predict_logic import predict_star_count, extract_form_features, rank_predictions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        predictions = []

        for i in range(1, 6):
            full_name, features = extract_form_features(i, request.form)

            if isinstance(features, str):
                predictions.append({"repo": full_name, "stars": features})
            else:
                task = predict_star_count.delay(features)
                stars = task.get()
                predictions.append({"repo": full_name, "stars": stars})

        sort_task = rank_predictions.delay(predictions)
        sorted_predictions = sort_task.get()
        return render_template("result.html", predictions=sorted_predictions)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)

