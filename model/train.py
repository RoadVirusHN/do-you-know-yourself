import pandas as pd
from datetime import datetime

import lightgbm as lgb
from dataloader import recent_data_processing

# import mlflow

# print(dir(mlflow))


def train():
    # try:
    #     # 프로젝트 별로 이름을 다르게 가져가면서 실험들을 기록
    #     mlflow.create_experiment(name='dkdkt-lgbm')
    # except:
    #     print('Exist experiment')

    # mlflow.set_experiment('dkdkt-lgbm')
    # mlflow.start_run()
    # mlflow.set_tag('version', '0.1')
    params = {
        'learning_rate': 0.1,
        'num_iterations': 1000,
        'boosting': 'dart',
        'num_leaves': 31,
        'objective': 'binary',
        'metric': 'auc',
        'boosting': 'dart',
        'seed': 42
    }
    # mlflow.log_params(params)
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

    train_data = pd.read_csv('./data/train.csv')
    ground_truth = pd.read_csv('./data/y_train.csv')
    lgb_train = lgb.Dataset(train_data[features], ground_truth)
    eval_result = {} # eval 검색법 알아보기
    model = lgb.train(params, lgb_train, evals_result=eval_result)
    # mlflow.log_metric('AUC', eval_result['train']['auc'][-1])
    # now = datetime.today().strftime('\%Y-\%m-\%d')
    # model.save_model(f'./model/lgbm/lgbm_{now}.txt')
    model.save_model(f'./model/model.txt')
    # mlflow.lightgbm.log_model(model, 'save_model')
    # mlflow.end_run()
    return model

def finetune(model):
    # try:
    #     # 프로젝트 별로 이름을 다르게 가져가면서 실험들을 기록
    #     mlflow.create_experiment(name='dkdkt-lgbm')
    # except:
    #     print('Exist experiment')

    # mlflow.set_experiment('dkdkt-lgbm')
    # mlflow.start_run()
    # mlflow.set_tag('version', '0.1')
    params = {
        'learning_rate': 0.1,
        'num_iterations': 1000,
        'boosting': 'dart',
        'num_leaves': 31,
        'objective': 'binary',
        'metric': 'auc',
        'boosting': 'dart',
        'seed': 42
    }
    # mlflow.log_params(params)
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
    recent_data_processing(last_data=True)
    train_data = pd.read_csv('./data/new_train.csv')
    ground_truth = pd.read_csv('./data/new_y_train.csv')

    lgb_train = lgb.Dataset(train_data[features], ground_truth, free_raw_data=False)
    eval_result = {}
    model = lgb.train(params, lgb_train, evals_result=eval_result, keep_training_booster=True, init_model=model)
    # mlflow.log_metric('AUC', eval_result['train']['auc'][-1])
   
    now = datetime.today().strftime('\%Y-\%m-\%d')
    model.save_model(f'./model/lgbm/lgbm_{now}_finetunned.txt')
    # mlflow.lightgbm.log_model(model, 'save_model')
    # mlflow.end_run()
    return model