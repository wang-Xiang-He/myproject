import pandas as pd
import math
import csv
import random
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import cross_val_score


# 設置回歸訓練時所需用到的參數變量
# 當每支隊伍沒有elo等級分時，賦予其基礎elo等級分
base_elo = 1600
team_elos = {}
team_stats = {}
X = []
y = []
# 存放數據的目錄
folder = 'data'


# 根據每支隊伍的Miscellaneous Opponent，Team統計數據csv文件進行初始化
def initialize_data(Mstat, Ostat, Tstat):
    new_Mstat = Mstat.drop(['Rk', 'Arena'], axis=1)
    new_Ostat = Ostat.drop(['Rk', 'G', 'MP'], axis=1)
    new_Tstat = Tstat.drop(['Rk', 'G', 'MP'], axis=1)

    team_stats1 = pd.merge(new_Mstat, new_Ostat, how='left', on='Team')
    team_stats1 = pd.merge(team_stats1, new_Tstat, how='left', on='Team')
    return team_stats1.set_index('Team', inplace=False, drop=True)

# 獲取每支隊伍的Elo Score等級分函數，當在開始沒有等級分時，將其賦予初始base_elo值：
def get_elo(team):
    try:
        return team_elos[team]
    except:
        # 當最初沒有elo時，給每個隊伍最初賦base_elo
        team_elos[team] = base_elo
        return team_elos[team]

# 計算每個球隊的elo值
def calc_elo(win_team, lose_team):
    winner_rank = get_elo(win_team)
    loser_rank = get_elo(lose_team)

    rank_diff = winner_rank - loser_rank
    exp = (rank_diff  * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    # 根據rank級別修改K值
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16

    # 更新 rank 數值
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    new_loser_rank = round(loser_rank + (k * (0 - odds)))
    return new_winner_rank, new_loser_rank



# 基於我們初始好的統計數據，及每支隊伍的 Elo score 計算結果，建立對應 2019~2020 年常規賽和季後賽中每場比賽的數據集
# （在主客場比賽時，我們認為主場作戰的隊伍更加有優勢一點，因此會給主場作戰隊伍相應加上 100 等級分）
def  build_dataSet(all_data):
    print("Building data set..")
    X = []
    skip = 0
    for index, row in all_data.iterrows():

        Wteam = row['WTeam']
        Lteam = row['LTeam']

        #獲取最初的elo或是每個隊伍最初的elo值
        team1_elo = get_elo(Wteam)
        team2_elo = get_elo(Lteam)

        # 給主場比賽的隊伍加上100的elo值
        if row['WLoc'] == 'H':
            team1_elo += 100
        else:
            team2_elo += 100

        # 把elo當為評價每個隊伍的第一個特徵值
        team1_features = [team1_elo]
        team2_features = [team2_elo]

        # 添加我們從basketball reference.com獲得的每個隊伍的統計信息
        for key, value in team_stats.loc[Wteam].iteritems():
            team1_features.append(value)
            # print(key, value)
        for key, value in team_stats.loc[Lteam].iteritems():
            team2_features.append(value)

        # 將兩支隊伍的特徵值隨機的分配在每場比賽數據的左右兩側
        # 並將對應的0/1賦給y值
        if random.random() > 0.5:
            X.append(team1_features + team2_features)
            y.append(0)
        else:
            X.append(team2_features + team1_features)
            y.append(1)

        if skip == 0:
            print('X',X)
            skip = 1

        # 根據這場比賽的數據更新隊伍的elo值
        new_winner_rank, new_loser_rank = calc_elo(Wteam, Lteam)
        team_elos[Wteam] = new_winner_rank
        team_elos[Lteam] = new_loser_rank

    return np.nan_to_num(X), y

def predict_winner(team_1, team_2, model):
    features = []

    # team 1，客場隊伍
    features.append(get_elo(team_1))
    for key, value in team_stats.loc[team_1].iteritems():
        features.append(value)

    # team 2，主場隊伍
    features.append(get_elo(team_2) + 100)
    for key, value in team_stats.loc[team_2].iteritems():
        features.append(value)

    features = np.nan_to_num(features)
    
    return model.predict_proba([features])




if __name__ == '__main__':

    Mstat = pd.read_csv(folder + '/19-20Miscellaneous_Stat.csv')
    Ostat = pd.read_csv(folder + '/19-20Opponent_Per_Game_Stat.csv')
    Tstat = pd.read_csv(folder + '/19-20Team_Per_Game_Stat.csv')

    team_stats = initialize_data(Mstat, Ostat, Tstat)

    result_data = pd.read_csv(folder + '/2019-2020_result.csv')
    X, y = build_dataSet(result_data)

    # 訓練網絡模型
    print("Fitting on %d game samples.." % len(X))

    model = linear_model.LogisticRegression()
    model.fit(X, y)

    # 利用10折交叉驗證計算訓練正確率
    print("Doing cross-validation..")
    print(cross_val_score(model, X, y, cv = 10, scoring='accuracy', n_jobs=-1).mean())


    print('Predicting on new schedule..')
    schedule1920 = pd.read_csv(folder + '/19-20Schedule.csv')
    result = []

    for index, row in schedule1920.iterrows():
        team1 = row['Vteam']
        team2 = row['Hteam']
        pred = predict_winner(team1, team2, model)
        prob = pred[0][0]
        if prob > 0.5:
            winner = team1
            loser = team2
            result.append([winner, loser, prob])
        else:
            winner = team2
            loser = team1
            result.append([winner, loser, 1 - prob])

    with open('19-20Result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['win', 'lose', 'probability'])
        writer.writerows(result)
        print('done.')





# 生成訓練集時，“將特徵值隨機分配在每場比賽數據的左右側”
 # 將勝利隊伍和失敗隊伍的特徵值隨機分配到每場比賽數據的左右側的意思是，為了隨機產生 [winTeam, loseTeam]（勝利隊伍特徵值在左側，對應的 y 值標籤為 0），[loseTeam, winTeam]（失敗隊伍在左側， 對應的 y 值標籤為 1）這樣的訓練樣本。你也可以固定利用數據集前一半為 [winTeam, loseTeam]，後一半為 [loseTeam, winTeam] 這樣來生成數據。只要保證兩類數據的分布比較均衡，且在訓練時隨機的取到兩類訓練樣本即可。