import pandas as pd
import math
from tqdm import tqdm
import numpy as np
from datetime import datetime
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder

# data의 종류
# 1. 원본 문제 데이터셋 questions_dataset: 문제들이 들어있는 데이터셋 modify 금지 
# 2. 원본 풀이 데이터셋 data: 문제 풀이들이 모여있는 데이터셋.
# 3. 최신 풀이 데이터셋 new: stack이 100개가 넘으면 원본 풀이 데이터셋과 concat
# 4. stack 데이터셋 stack: 100개가 넘으면 최신 데이터셋과 교체
# 5. feature engineering 풀이 데이터셋 data_fe
# 6. feature engineering 최신 풀이 데이터셋 new_fe

def feature_engineering(df):
    df.sort_values(by=['userID','Timestamp'], inplace=True)
            
    df['hour'] = df['Timestamp'].dt.hour
    df['dow'] = df['Timestamp'].dt.dayofweek
            
    diff = df.loc[:, ['userID','Timestamp']].groupby('userID').diff().fillna(pd.Timedelta(seconds=0))
    diff = diff.fillna(pd.Timedelta(seconds=0))
    diff = diff['Timestamp'].apply(lambda x: x.total_seconds())

    print('start  -  elapsed')
    # 푸는 시간
    df['elapsed'] = diff
    df['elapsed'] = df['elapsed'].apply(lambda x : x if x <650 and x >=0 else 0)
            
    df['problem_number'] = df['assessmentItemID']
            
    
    print('start  -  if')
                
    correct_t = df.groupby(['testId'])['user_answer'].agg(['mean', 'sum'])
    correct_t.columns = ["test_mean", 'test_sum']
    correct_k = df.groupby(['KnowledgeTag'])['user_answer'].agg(['mean', 'sum'])
    correct_k.columns = ["tag_mean", 'tag_sum']
    correct_a = df.groupby(['assessmentItemID'])['user_answer'].agg(['mean', 'sum'])
    correct_a.columns = ["ass_mean", 'ass_sum']
    correct_p = df.groupby(['problem_number'])['user_answer'].agg(['mean', 'sum'])
    correct_p.columns = ["prb_mean", 'prb_sum']
    correct_h = df.groupby(['hour'])['user_answer'].agg(['mean', 'sum'])
    correct_h.columns = ["hour_mean", 'hour_sum']
    correct_d = df.groupby(['dow'])['user_answer'].agg(['mean', 'sum'])
    correct_d.columns = ["dow_mean", 'dow_sum'] 
            
    df = pd.merge(df, correct_t, on=['testId'], how="left")
    df = pd.merge(df, correct_k, on=['KnowledgeTag'], how="left")
    df = pd.merge(df, correct_a, on=['assessmentItemID'], how="left")
    df = pd.merge(df, correct_p, on=['problem_number'], how="left")
    df = pd.merge(df, correct_h, on=['hour'], how="left")
    df = pd.merge(df, correct_d, on=['dow'], how="left")

    o_df = df[df['user_answer']==1]
    x_df = df[df['user_answer']==0]
            
    elp_k = df.groupby(['KnowledgeTag'])['elapsed'].agg('mean').reset_index()
    elp_k.columns = ['KnowledgeTag',"tag_elp"]
    elp_k_o = o_df.groupby(['KnowledgeTag'])['elapsed'].agg('mean').reset_index()
    elp_k_o.columns = ['KnowledgeTag', "tag_elp_o"]
    elp_k_x = x_df.groupby(['KnowledgeTag'])['elapsed'].agg('mean').reset_index()
    elp_k_x.columns = ['KnowledgeTag', "tag_elp_x"]
            
    df = pd.merge(df, elp_k, on=['KnowledgeTag'], how="left")
    df = pd.merge(df, elp_k_o, on=['KnowledgeTag'], how="left")
    df = pd.merge(df, elp_k_x, on=['KnowledgeTag'], how="left")

    ass_k = df.groupby(['assessmentItemID'])['elapsed'].agg('mean').reset_index()
    ass_k.columns = ['assessmentItemID',"ass_elp"]
    ass_k_o = o_df.groupby(['assessmentItemID'])['elapsed'].agg('mean').reset_index()
    ass_k_o.columns = ['assessmentItemID',"ass_elp_o"]
    ass_k_x = x_df.groupby(['assessmentItemID'])['elapsed'].agg('mean').reset_index()
    ass_k_x.columns = ['assessmentItemID',"ass_elp_x"]

    df = pd.merge(df, ass_k, on=['assessmentItemID'], how="left")
    df = pd.merge(df, ass_k_o, on=['assessmentItemID'], how="left")
    df = pd.merge(df, ass_k_x, on=['assessmentItemID'], how="left")

    prb_k = df.groupby(['problem_number'])['elapsed'].agg('mean').reset_index()
    prb_k.columns = ['problem_number',"prb_elp"]
    prb_k_o = o_df.groupby(['problem_number'])['elapsed'].agg('mean').reset_index()
    prb_k_o.columns = ['problem_number',"prb_elp_o"]
    prb_k_x = x_df.groupby(['problem_number'])['elapsed'].agg('mean').reset_index()
    prb_k_x.columns = ['problem_number',"prb_elp_x"]

    df = pd.merge(df, prb_k, on=['problem_number'], how="left")
    df = pd.merge(df, prb_k_o, on=['problem_number'], how="left")
    df = pd.merge(df, prb_k_x, on=['problem_number'], how="left")
            
    df['user_correct_answer'] = df.groupby('userID')['user_answer'].transform(lambda x: x.cumsum().shift(1))
    df['user_total_answer'] = df.groupby('userID')['user_answer'].cumcount()
    df['user_acc'] = df['user_correct_answer']/df['user_total_answer']
    df['Grade_o'] = df.groupby(['userID','grade'])['user_answer'].transform(lambda x: x.cumsum().shift(1))
    df['GradeCount'] = df.groupby(['userID','grade']).cumcount()
    df['GradeAcc'] = df['Grade_o']/df['GradeCount']
    df['GradeElp'] = df.groupby(['userID','grade'])['elapsed'].transform(lambda x: x.cumsum().shift(1))
    df['GradeMElp'] = df['GradeElp']/df['GradeCount']
            
    f = lambda x : len(set(x))
    test_df = df.groupby(['testId']).agg({
        'problem_number':'max',
        'KnowledgeTag':f
    })
    test_df.reset_index(inplace=True)

    test_df.columns = ['testId','problem_count',"tag_count"]
            
    df = pd.merge(df,test_df,on='testId',how='left')
            
    gdf = df[['userID','testId','problem_number','grade','Timestamp']].sort_values(by=['userID','grade','Timestamp'])
    gdf['buserID'] = gdf['userID'] != gdf['userID'].shift(1)
    gdf['bgrade'] = gdf['grade'] != gdf['grade'].shift(1)
    gdf['first'] = gdf[['buserID','bgrade']].any(axis=1).apply(lambda x : 1- int(x))
    gdf['RepeatedTime'] = gdf['Timestamp'].diff().fillna(pd.Timedelta(seconds=0)) 
    gdf['RepeatedTime'] = gdf['RepeatedTime'].apply(lambda x: x.total_seconds()) * gdf['first']
    df['RepeatedTime'] = gdf['RepeatedTime'].apply(lambda x : math.log(x+1))
            
    df['prior_KnowledgeTag_frequency'] = df.groupby(['userID','KnowledgeTag']).cumcount()
            
    df['problem_position'] = df['problem_number'] / df["problem_count"]
    df['solve_order'] = df.groupby(['userID','testId']).cumcount()
    df['solve_order'] = df['solve_order'] - df['problem_count']*(df['solve_order'] > df['problem_count']).apply(int) + 1
    df['retest'] = (df['solve_order'] > df['problem_count']).apply(int)
    T = df['solve_order'] != df['problem_number']
    TT = T.shift(1)
    TT[0] = False
    df['solved_disorder'] = (TT.apply(lambda x : not x) & T).apply(int)
    df['last_problem'] = (df['testId']!=df['testId'].shift(-1)).apply(int)
    df = ELO_function(df)
    
    def percentile(s):
        return np.sum(s) / len(s)
    
    # grade별 정답률
    stu_groupby = df.groupby('grade').agg({
        'assessmentItemID': 'count',
        'user_answer': percentile
    }).rename(columns = {'user_answer' : 'answer_rate'})
    
    # tag별 정답률
    stu_tag_groupby = df.groupby(['grade', 'KnowledgeTag']).agg({
        'assessmentItemID': 'count',
        'user_answer': percentile
    }).rename(columns = {'user_answer' : 'answer_rate'})

    # 시험지별 정답률
    stu_test_groupby = df.groupby(['grade', 'testId']).agg({
        'assessmentItemID': 'count',
        'user_answer': percentile
    }).rename(columns = {'user_answer' : 'answer_rate'})
                                                                    
    # 문항별 정답률
    stu_assessment_groupby = df.groupby(['grade', 'assessmentItemID']).agg({
        'assessmentItemID': 'count',
        'user_answer': percentile
    }).rename(columns = {'assessmentItemID' : 'assessment_count', 'user_answer' : 'answer_rate'})
    
    temp = pd.merge(df, stu_groupby.reset_index()[['grade', 'answer_rate']], on = ['grade'])
    temp = temp.sort_values(by=['userID','Timestamp'], axis=0).reset_index()
    df['answer_delta'] = temp['user_answer'] - temp['answer_rate']

    # 정답 - 태그별 정답률
    temp = pd.merge(df, stu_tag_groupby.reset_index()[['answer_rate', 'KnowledgeTag']], on = ['KnowledgeTag'])
    temp = temp.sort_values(by=['userID','Timestamp'], axis=0).reset_index()
    df['tag_delta'] = temp['user_answer'] - temp['answer_rate']

    # 정답 - 시험별 정답률
    temp = pd.merge(df, stu_test_groupby.reset_index()[['answer_rate', 'testId']], on = ['testId'])
    temp = temp.sort_values(by=['userID','Timestamp'], axis=0).reset_index()
    df['test_delta'] = temp['user_answer'] - temp['answer_rate']

    # 정답 - 문항별 정답률
    temp = pd.merge(df, stu_assessment_groupby.reset_index()[['answer_rate', 'assessmentItemID']], on = ['assessmentItemID'])
    temp = temp.sort_values(by=['userID','Timestamp'], axis=0).reset_index()
    df['assess_delta'] = temp['user_answer'] - temp['answer_rate']
    
    
    # cumsum
    df['prior_relative_assess_ac_sum'] = df.groupby('userID')['assess_delta'].cumsum().shift(fill_value=0)
    df['prior_relative_answer_ac_sum'] = df.groupby('userID')['answer_delta'].cumsum().shift(fill_value=0)
    df['prior_relative_tag_ac_sum'] = df.groupby('userID')['tag_delta'].cumsum().shift(fill_value=0)
    df['prior_relative_test_ac_sum'] = df.groupby('userID')['test_delta'].cumsum().shift(fill_value=0)
    
    # delta rolling
    df.tag_delta = df.tag_delta.shift(fill_value = 0)
    df.assess_delta = df.assess_delta.shift(fill_value = 0)
    df.answer_delta = df.answer_delta.shift(fill_value = 0)
    df.test_delta = df.test_delta.shift(fill_value = 0)
    
    df = df.fillna(0)
    return df


def preprocess_dataset (df) :
    df.userID = df.userID.apply(lambda x : x.replace("'", ''))
    df['KnowledgeTag']=df['KnowledgeTag'].astype(str)
    df['KnowledgeTag']=df['KnowledgeTag'].apply(lambda x:x.replace("'",""))
    df.testId = df.testId.apply(lambda x : x.replace("'", ''))
    df.grade = df.grade.apply(lambda x : int(x.replace("'", '')))
    df.user_answer = df.user_answer.apply(lambda x : int(x.replace("'", '')))
    df.assessmentItemID = df.assessmentItemID.apply(lambda x : int(x.replace("'", '')))
    df.elapsed = df.elapsed.apply(lambda x : int(x.replace("'", '')))
    df.Timestamp = df.Timestamp.apply(lambda x : x.replace("'", ''))
    df.Timestamp = df.Timestamp.apply(lambda x : x.replace('"', ''))
    df.Timestamp = df.Timestamp.apply(lambda x : datetime.fromtimestamp(int(x)/1000))    
    return df


def add_last_problem(df):
    new = []
    pre = df['testId'][0]
    for idx in df['testId']:
        if pre != idx :
            new[-1]=-1
            pre = idx
        new.append(0)
    df['last_problem'] = new
    return df


def is_previous_ordered(row):
    q_num = row.problem_number
    q_num_prev = row.q_num_prev
    delta = row.delta
    delta_thres = 1 # hour
    
    if pd.isnull(delta) or delta > pd.Timedelta(hours=1):
        return -1
    elif q_num == q_num_prev + 1:
        return 1
    else:
        return 0


def is_previous_decreasing(row):
    q_num = row.problem_number
    q_num_prev = row.q_num_prev
    delta = row.delta
    delta_thres = 1 # hour
    
    if pd.isnull(delta) or delta > pd.Timedelta(hours=1):
        return -1
    elif q_num < q_num_prev:
        return 1
    else:
        return 0


def is_probably_easy(row):
    delta = row.delta
    delta_thres = 1 # hour
    
    is_prev_ord = row.is_previous_ordered
    is_prev_dec = row.is_previous_decreasing
    is_prev_ord_shift = row.is_prev_ord_shift
    is_prev_dec_shift = row.is_prev_dec_shift
    
    case = (is_prev_ord_shift, is_prev_dec_shift, is_prev_ord, is_prev_dec)
    
    probably_easy_l = [
        (np.nan, np.nan, -1, -1),
        (-1, -1, 1, 0),
        (1, 0, 1, 0),
        (1, 0, 0, 0),
    ]
    
    if pd.isnull(delta) or delta > pd.Timedelta(hours=1):
        return -1
    elif case in probably_easy_l:
        return 1
    else:
        return 0


def ELO_function (df) :
    def get_new_theta(is_good_answer, beta, left_asymptote, theta, nb_previous_answers):
        return theta + learning_rate_theta(nb_previous_answers) * (
            is_good_answer - probability_of_good_answer(theta, beta, left_asymptote)
        )

    def get_new_beta(is_good_answer, beta, left_asymptote, theta, nb_previous_answers):
        return beta - learning_rate_beta(nb_previous_answers) * (
            is_good_answer - probability_of_good_answer(theta, beta, left_asymptote)
        )

    def learning_rate_theta(nb_answers):
        return max(0.3 / (1 + 0.01 * nb_answers), 0.04)

    def learning_rate_beta(nb_answers):
        return 1 / (1 + 0.05 * nb_answers)

    def probability_of_good_answer(theta, beta, left_asymptote):
        return left_asymptote + (1 - left_asymptote) * sigmoid(theta - beta)

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    
    def estimate_parameters(answers_df, granularity_feature_name='assessmentItemID'):
        item_parameters = {
            granularity_feature_value: {"beta": 0, "nb_answers": 0}
            for granularity_feature_value in np.unique(answers_df[granularity_feature_name])
        }
        student_parameters = {
            student_id: {"theta": 0, "nb_answers": 0}
            for student_id in np.unique(answers_df.userID)
        }

        print("Parameter estimation is starting...")

        for student_id, item_id, left_asymptote, answered_correctly in tqdm(
            zip(answers_df.userID.values, answers_df[granularity_feature_name].values, answers_df.left_asymptote.values, answers_df.user_answer.values)
        ):
            theta = student_parameters[student_id]["theta"]
            beta = item_parameters[item_id]["beta"]

            item_parameters[item_id]["beta"] = get_new_beta(
                answered_correctly, beta, left_asymptote, theta, item_parameters[item_id]["nb_answers"],
            )
            student_parameters[student_id]["theta"] = get_new_theta(
                answered_correctly, beta, left_asymptote, theta, student_parameters[student_id]["nb_answers"],
            )

            item_parameters[item_id]["nb_answers"] += 1
            student_parameters[student_id]["nb_answers"] += 1

        print(f"Theta & beta estimations on {granularity_feature_name} are completed.")
        return student_parameters, item_parameters
    
    def gou_func (theta, beta) :
        return 1 / (1 + np.exp(-(theta - beta)))
    
    
    df['left_asymptote'] = 0

    print(f"Dataset of shape {df.shape}")
    print(f"Columns are {list(df.columns)}")

    student_parameters, item_parameters = estimate_parameters(df)
    
    prob = [gou_func(student_parameters[student]['theta'], item_parameters[item]['beta']) for student, item in zip(df.userID.values, df.assessmentItemID.values)]
    
    df['elo_prob'] = prob
    
    return df

def recent_data_processing(last_data=False):
    df = pd.read_csv('./data/data.csv')
    df = preprocess_dataset(df)
    df = feature_engineering(df)

    ordinal_feats = ['grade']
    label_feats = ['problem_number','solved_disorder','KnowledgeTag','testId','retest']

    for c in ordinal_feats :
        X = df[c].values.reshape(-1,1)
        enc = OrdinalEncoder()
        enc.fit(X)
        X = enc.transform(X)
        df[c] = X
    
    for c in label_feats :
        X = df[c].values.reshape(-1,1)
        enc = LabelEncoder()
        enc.fit(X)
        X = enc.transform(X)
        df[c] = X

    if last_data: df = df.tail(100)
    y_train = df['user_answer']
    train = df.drop(['user_answer'], axis = 1)
    if last_data:        
        y_train.to_csv('./data/new_y_train.csv',index=False)
        train.to_csv('./data/new_train.csv',index=False)
    else:
        y_train.to_csv('./data/y_train.csv',index=False)
        train.to_csv('./data/train.csv',index=False)