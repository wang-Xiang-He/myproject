from django.shortcuts import render,HttpResponse
from .models import NBAData
from django.views import generic # 通用模块
from django.db import connection
import requests
import random
from bs4 import BeautifulSoup
import pymysql.cursors
import os
import pandas as pd
import math
import csv
from .models import NBAData



# Create your views here.
def predict(request):
    # 判斷用戶是否提交數據
    df = pd.read_csv('static/19-20Result.csv')
    team_list=[]

    for i in range(len(df)):
        team = df.iloc[i,0]
        if team not in team_list:
            team_list.append(team)

    if request.method == "POST":
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        prob = None
        win = None
        lose = None

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
        return render(request,'nba/predict.html', locals())




    if request.method == "GET":

        return render(request,'nba/predict.html',locals())



class IndexViews(generic.ListView):
    model = NBAData # 設置後取數據庫中的全部數據
    template_name = 'nba/index.html' # 指定模塊
    context_object_name = 'GGGG' # 獲取數據名字 上下文中使用的變量的名稱

    # queryset = NBAData.objects.filter().all()[0:5]  # 如果提供，則 queryset取代所提供的值model。
    #              ||(等價)
    def get_queryset(self):
        '''根據winrate列進行排序從大到小 -winrate 從小到大'''
        return NBAData.objects.order_by('-winrate')

class EastViews(generic.ListView):
    template_name = 'nba/east.html'
    context_object_name = 'GGGG'
    def get_queryset(self):
        return NBAData.objects.filter(area='东部').all()

class WestViews(generic.ListView):
    template_name = 'nba/west.html'
    context_object_name = 'GGGG'
    def get_queryset(self):
        return NBAData.objects.filter(area='西部').all()


class FirstViews(generic.DetailView):
    model = NBAData
    template_name = 'nba/first.html'

    # def get_context_data(self, **kwargs):
    #     如果视图将model属性设置为 User，则默认上下文对象名称user将覆盖上下文处理器中的user变量 所以NBAData --> nbadata
    #     context = super().get_context_data(**kwargs) # 重置函数
    #     print(context)
    #     {'object': <NBAData: 猛龙>, 'nbadata': <NBAData: 猛龙>, 'view': <index.views.FirstViews object at 0x0000016E47A314A8>}
    #     return context



# def east(request):
#     if request.method == "GET":
#         try:
#             sql = "select * from nba_nbadata where area='东部'  order by(winrate) desc"
#             datas = NBAData.objects.raw(sql)
#             win_list = []
#             ballgame_list = []
#             transport_list = []
#             winrate_list = []
#             for x in list(datas):
#                 win_list.append(x.win)
#                 ballgame_list.append(x.ballgame.encode('utf-8').decode('utf-8'))
#                 transport_list.append(x.transport)
#                 winrate_list.append(float(x.winrate.replace('%','')))

#             ballgame_str = '_'.join(ballgame_list)
#             datass = list(datas)
#             NBAdata = {
#                 "win":win_list,
#                 "ballgame":ballgame_str,
#                 "transport":transport_list,
#                 "winrate":winrate_list,
#             }
#         except:
#             NBAdata = {
#                 "win":[],
#                 "ballgame":[],
#                 "transport":[],
#                 "winrate":[],
#             }

#             datass=[]
#         finally:
#             return render(request,'east.html',{'NBAdata':NBAdata,'datas':list(datas)})



# def west(request):
#     if request.method == "GET":
#         try:
#             sql = "select * from nba_nbadata where area='西部'  order by(winrate) desc"
#             datas = NBAData.objects.raw(sql)
#             win_list = []
#             ballgame_list = []
#             transport_list = []
#             winrate_list = []
#             for x in list(datas):
#                 win_list.append(x.win)
#                 ballgame_list.append(x.ballgame.encode('utf-8').decode('utf-8'))
#                 transport_list.append(x.transport)
#                 winrate_list.append(float(x.winrate.replace('%','')))


#             ballgame_str = '_'.join(ballgame_list)
#             datass = list(datas)
#             NBAdata = {
#                 "win":win_list,
#                 "ballgame":ballgame_str,
#                 "transport":transport_list,
#                 "winrate":winrate_list,
#             }
#         except:
#             NBAdata = {
#                 "win":[],
#                 "ballgame":[],
#                 "transport":[],
#                 "winrate":[],
#             }

#             datass=[]
#         finally:
#             return render(request,'west.html',{'NBAdata':NBAdata,'datas':list(datas)})


def first(request, pk):
    try:
        sql = "select * from nba_nbadata order by(winrate) desc;"
        datas = NBAData.objects.raw(sql)
        nbadata = list(datas)[0]
    except:
        nbadata=''
    finally:
        return render(request,'nba/first.html',{"nbadata":nbadata})


def get_data():
    headers = Ua_headers()
    response = requests.get('https://nba.hupu.com/standings',headers=headers,verify=False)
    return response.text


def Ua_headers():
    user_agent_list = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',]
    user_agent = random.choice(user_agent_list)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    headers['user_agent'] = user_agent
    return headers




def Analyze_data(data):
    soup = BeautifulSoup(data,'html.parser')
    datas = soup.find('tbody')
    datas_tr = datas.find_all('tr')
    cursor = connection.cursor()
    cursor.execute('truncate table nba_nbadata')
    for tr in datas_tr:
        print(tr)
        td = tr.find_all("td")
        if len(td) == 1:
            area = td[0].text
        else:
            da1 = td[0].text # 排名
            da2 = td[1].text # 隊名
            da3 = td[2].text # 勝場
            da4 = td[3].text # 敗場
            da5 = td[4].text # 勝率
            img = "/static/images/"+ da2 + '.png'
            # try:
            #     img_url = td[1].find("a")['href']
            #     get_img(img_url,td[1].text)
                # img = "/static/images/"+ da2 + '.png' # os.getcwd() + "\\NBA\\
            # except TypeError:
            #     pass
            try:
                cursor.execute("INSERT INTO nba_nbadata (ranking,ballgame,win,transport,winrate,logopath,area) VALUES ('%d','%s','%d','%d','%s','%s','%s')"%(
                    int(da1),da2,int(da3),int(da4),da5,img,area))

            except ValueError:
                pass
            connection.commit()

        try:
            team = NBAdata.objects.get(ballgame = da2)
            team.logopath = "/static/images/" + da2 + '.png'
            team.save()
        except:
            pass


# def get_img(url,name):
#     path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ '\\' + "static"+'\\' +"images"+'\\'
#     print(path)
#     headers = Ua_headers()
#     response = requests.get(url, headers=headers, verify=False)
#     soup = BeautifulSoup(response.text,'lxml')
#     img = soup.find('div',{'class':'img'})
#     img_url = img.find("img")['src']
#     pon = requests.get(img_url)
#     with open(path+name+'.png','ab+') as im:
#         im.write(pon.content)
#         im.close()
#     print('保存圖片成功')



def homepage(request):
    # pon = get_data()
    # Analyze_data(pon)

    sql = "select * from nba_nbadata"
    datas = NBAData.objects.raw(sql)
    win_list = []
    ballgame_list = []
    transport_list = []
    winrate_list = []
    for x in list(datas):
        win_list.append(x.win)
        ballgame_list.append(x.ballgame.encode('utf-8').decode('utf-8'))
        transport_list.append(x.transport)
        winrate_list.append(float(x.winrate.replace('%', '')))

    # map(lambda x:x.win,list(datas))
    ballgame_str = '_'.join(ballgame_list)
    NBAdata = {"win": win_list, "ballgame": ballgame_str, "transport": transport_list, "winrate": winrate_list, }
    return render(request, 'nba/Homepage.html', locals())

def renew(request):
    pon = get_data()
    Analyze_data(pon)
    return render(request, 'nba/Homepage.html')
