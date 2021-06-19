from flask import Flask, render_template, request, jsonify

import inference


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get_questions', methods=['POST'])
def get_questions():
    print(request.json)
    tag = request.json
    user = request.json
    questions = [
        {
            'text': "이순신은 어느 시대 사람인가?",
            'tag': 0,
            'answer': "조선",
            'assess': "0",
            'grade': 0,
        },
        {
            'text': "이순신이 최후를 맞은 전투는 무엇인가?",
            'tag': 0,
            'answer': "노량",
            'assess': "1",
            'grade': 1,
        },
        {
            'text': "박지성이 뛰지 않은 팀은 어디인가?",
            'tag': 1,
            'answer': "PSG",
            'assess': "0",
            'grade': 1,
        },
        {
            'text': "손흥민의 팀 동료가 아닌 사람은 누구인가?",
            'tag': 1,
            'answer': "메시",
            'assess': "1",
            'grade': 2
        }]
    return jsonify(questions)

@app.route('/get_score', methods=['POST'])
def get_score():
    data = request.json
    user_data = []
    for d in data:
        if 'answer' in d:
            row = [d['tag'], d['assess'], d['grade'], d['text'], d['answer']]
            user_data.append(row)

    score = inference.inference(user_data)
    score = int(score)
    return str(score)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6006, debug=True)
