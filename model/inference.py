import pandas as pd
from model import train
from dataloader import recent_data_processing


features = [
    'last_problem',
    'KnowledgeTag', 'assessmentItemID', 'testId', 'grade', 'elapsed',
    'prior_KnowledgeTag_frequency', 'retest',
    'problem_number', 'test_mean', 'test_sum', 'tag_mean', 'tag_sum', 'elo_prob',
    'tag_delta', 'answer_delta', 'test_delta', 'assess_delta',
    'prior_relative_assess_ac_sum', 'prior_relative_answer_ac_sum',
    'prior_relative_tag_ac_sum', 'prior_relative_test_ac_sum',
    'ass_mean', 'ass_sum', 'prb_mean', 'prb_sum', 'tag_elp', 'tag_elp_o',
    'tag_elp_x', 'ass_elp', 'ass_elp_o', 'ass_elp_x', 'prb_elp',
    'prb_elp_o', 'prb_elp_x', 'user_correct_answer', 'user_total_answer',
    'user_acc', 'Grade_o', 'GradeCount', 'GradeAcc', 'GradeElp',
    'GradeMElp', 'problem_count', 'tag_count',
    'problem_position', 'solve_order', 'solved_disorder'
]


def inference(data, mode="nope"):
    problem_df = pd.read_csv("./data/questions_dataset.csv")
    solved_df = pd.read_csv("./data/train.csv")
    tag_num = data['KnowledgeTag'][0]
    tag_problem = problem_df[problem_df['KnowledgeTag'] == tag_num] # tag에 해당하는 문제들
    # tag에 해당하는 풀이들
    solved_problem = solved_df[solved_df['KnowledgeTag'] == tag_num]

    # 해당하는 태그의 문제를 모두 가져오고, predict한 뒤, 가장 어려운 문제, 가장 쉬운 문제를 가져오기,
    # 해당 태그 문제들 중 0.5를 넘는 것은 정답, 못넘으면 틀린 것으로 result 내기
    # model = lgb.Booster(model_file='model.txt')
    # 노 train 모드에서는 그냥 model로 예측치 가져오기

    if mode=="w":
        recent_data_processing()

    # 새로 모델을 생성
    model = train.train()

    if mode=="f":
    # 가져온 모델을 finetune
        model = train.finetune(model)
        
    solved_problem = solved_problem.fillna(0)
    # tag에 해당하는 풀이들의 풀 확률 계산
    solved_problem['result'] = model.predict(solved_problem[features])
    # 각 문제들의 유저별, 시간대별 평균 풀 확률 계산 
    problem_acc = solved_problem.groupby("assessmentItemID")['result'].agg('mean').reset_index()
    problem_acc.columns = ['assessmentItemID', 'prob']
    # 각 문제들의 풀이 확률에 대입
    

    tag_problem = pd.merge(tag_problem, problem_acc, on=['assessmentItemID'], how="left")

    # 만약, 이미 유저가 틀렸거나 맞았다면, 제외
    new_tag_problem = tag_problem[~tag_problem['assessmentItemID'].isin(data['assessmentItemID'].unique())]
    hard_problem = new_tag_problem.loc[new_tag_problem[['prob']].idxmin()].to_dict()
    easy_problem = new_tag_problem.loc[new_tag_problem[['prob']].idxmax()].to_dict()
    hard_problem = { k:list(v.items())[0][1] for k, v in hard_problem.items()}
    easy_problem = { k:list(v.items())[0][1] for k, v in easy_problem.items()}
    # user가 풀었거나, 정답확률이 0.5 이상이면 score로 추가
    result = len(data[data['user_answer']==1])
    result += len(new_tag_problem[new_tag_problem['prob'] >= 0.5])
    result += int((new_tag_problem.isna().any(axis=1).sum())//2) # 아무도 푼적이 없는 데이터 처리
    return {"tag_problem_len": len(tag_problem), "score": result, "h_problem": hard_problem, "e_problem": easy_problem}
