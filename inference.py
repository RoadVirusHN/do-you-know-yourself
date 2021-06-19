import os

import torch
import pandas as pd
import numpy as np



def gen_data(data):
    df = pd.read_csv("questions.csv")
    
    
    new_columns = df.columns.tolist()+['answerCode']
    new_df = pd.DataFrame([],columns=new_columns+['userID'])
    
    for index, row in df.iterrows():
        user_actions = pd.DataFrame(data, columns=new_columns)    
        user_actions['userID'] = index
        new_df=new_df.append(user_actions)
        row['userID'] = index
        new_df=new_df.append(row)
    
    new_df['answerCode'].fillna(-1, inplace=True)
    new_df['answerCode']=new_df['answerCode'].astype(int)
    new_df['KnowledgeTag']=new_df['KnowledgeTag'].astype(str)
    new_df = new_df.reset_index(drop=True)
    return new_df

    
def inference(data):
    result = len([i for i in data if i[-1]])
    print("Before:",data)
    # data = gen_data(data)
    print("After:",data)
    
    #TODO
    #이곳에서 위에서 생성한 데이터를 기반으로 inference한 값들을 평균을 내서 입력해주시면 되겠습니다.
    #probability의 평균
    # hard_problem = {
    #     "tag": 0,
    #     "assess": 9,
    #     "grade": 8,
    #     "text": "이마트 로고송의 원곡 명은?",
    #     "choices": ['happy talk', 'master of puppets', 'butterfly', '고추참치'],
    #     "answer": 0,
    #     "userID": "윤준석",
    #     "elapsed": 21,
    #     "prob": 0.1232,
    # }
    # easy_problem = {
    #     "tag": 0,
    #     "assess": 4,
    #     "grade": 1,
    #     "text": "dkt 6조의 발표 시간은?",
    #     "choices": ['오전 10시', '오전 10시 20분', '오전 10시 40분', '오전 11시'],
    #     "answer": 2,
    #     "userID": "윤준석",
    #     "elapsed": 231,
    #     "prob": 0.8923
    # }
    hard_problem = {
        "tag": 0,
        "assess": 9,
        "grade": 8,
        "text": "이마트 로고송의 원곡 명은?",
        "choice0": 'happy talk',
        "choice1": 'master of puppets',
        "choice2": 'butterfly',
        "choice3" : '고추참치',
        "answer": 0,
        "userID": "윤준석",
        "elapsed": 21,
        "prob": 0.1232,
    }
    easy_problem = {
        "tag": 0,
        "assess": 4,
        "grade": 1,
        "text": "dkt 6조의 발표 시간은?",
        "choice0": '오전 10시',
        "choice1": '오전 10시 20분',
        "choice2": '오전 10시 40분',
        "choice3" : '오전 11시',
        "answer": 2,
        "userID": "윤준석",
        "elapsed": 231,
        "prob": 0.8923
    }
    return {"tag_problem_len": 20, "score":result, "h_problem": hard_problem, "e_problem": easy_problem}    

