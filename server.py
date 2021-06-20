from flask import Flask, render_template, request, jsonify, Response
import pandas as pd

import inference


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_questions", methods=["POST"])
def get_questions():
    tag = request.json["tag"]
    user = request.json["user"]
    questions = pd.read_csv("question.csv")
    questions = questions.groupby("tag").get_group(int(tag))
    return Response(questions.to_json(orient="records"), mimetype="application/json")


@app.route("/get_score", methods=["POST"])
def get_score():
    data = request.json
    # dictionary to csv
    user_data = []
    for d in data:
        if "answer" in d:
            row = [d["tag"], d["assess"], d["grade"], d["text"], d["answer"], d["elapsed"], d["user_id"]]
            user_data.append(row)
    data = inference.inference(user_data)
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006, debug=True)
