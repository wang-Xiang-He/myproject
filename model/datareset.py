import pandas as pd
import math
import csv

df = pd.read_csv('19-20Result.csv')

team_list=[]

for i in range(len(df)):
    team = df.iloc[i,0]
    if team not in team_list:
        team_list.append(team)


# print(len(team_list))

def predict(team1, team2):
    prob = '請選擇不同隊'
    for i in range(len(df)):
        teama = df.iloc[i,0]
        teamb = df.iloc[i,1]
        if teama == team1 and teamb == team2:
            prob = df.iloc[i,2]
            win = team1
            lose = team2
            break
        elif teama == team2 and teamb == team1:
            prob = df.iloc[i,2]
            win = team2
            lose = team1
            break
    return win,lose,prob

x,y,z = predict(a,b)
print(x,y,z)


