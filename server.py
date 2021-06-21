from flask import Flask, render_template, request, Response
import pandas as pd
import sqlite3
from model import inference

app = Flask(__name__)

def insert_data(data):
    with open("data/data.csv", mode="a") as file_:
        for d in data:
            file_.write(
                "'{}','{}','{}', '{}', '{}', '{}','{}','{}'".format(
                    d[0],
                    d[1],
                    d[2],
                    d[3],
                    d[4],
                    d[5],
                    d[6],
                    d[7],
                )
            )
            file_.write("\n")

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    qry = "SELECT userID FROM problems ORDER BY userID DESC LIMIT 1;"
    cur.execute(qry)
    rows = cur.fetchall()
    for row in data:
        qry_values = "NULL,'{}','{}','{}', '{}', '{}', '{}','{}','{}'".format(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
        )
        query = """INSERT INTO problems VALUES ({})""".format(qry_values)
        cur.execute(query)
    con.commit()
    con.close()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_questions", methods=["POST"])
def get_questions():
    tag = request.json["tag"]
    questions = pd.read_csv("./data/questions_dataset.csv")
    questions = questions.groupby("KnowledgeTag").get_group(int(tag))
    questions = questions.sample(5)
    return Response(questions.to_json(orient="records"), mimetype="application/json")


@app.route("/get_score", methods=["POST"])
def get_score():
    data = request.json
    # dictionary to csv
    user_data = []
    for d in data:
        if "answer" in d:
            row = [
                d["user_id"],
                d["KnowledgeTag"],
                d["assessmentItemID"],
                d["testId"],
                d["grade"],
                d["user_answer"],
                d["elapsed"],
                d["Timestamp"],
            ]
            user_data.append(row)
    insert_data(user_data)
    data = pd.DataFrame.from_dict(data)
    data = inference.inference(data, "f")
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
