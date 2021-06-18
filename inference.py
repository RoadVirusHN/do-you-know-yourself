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
    result = len([i for i in data if i[-1].isnumeric() == True])*20
    print("Before:",data)
    # data = gen_data(data)
    print("After:",data)
    
    #TODO
    #이곳에서 위에서 생성한 데이터를 기반으로 inference한 값들을 평균을 내서 입력해주시면 되겠습니다.
    #probability의 평균


    return result    

