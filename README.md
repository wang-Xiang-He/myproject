# 感謝各位來到我的網站
### 在此先貼上連結 我的 NBA資訊網(https://nbaliveshow.herokuapp.com/nba/homepage/)
#### 此專案 以 DJANGO(2.0) 為基礎開發並布署在 heroku 上

## 此網站主要分四大部分
_________________________________________________________________________________________________________________________

### 第一部分: 搭建具有會員 本地登錄 第三方登錄 註冊 功能之部落格
#### 用戶可在登錄後編輯個人基本信息及撰寫文章,
#### 並有對他人文章做回覆點讚等功能且設有消息通知功能
###### (原有聊天大廳功能,但因 heroku 上要啟用此功能需要用到 redis 但我並無信用卡認證故目前聊天大廳為無法使用)

__________________________________________________________________________________________________________________________

### 第二部分為 NBA 相關信息
##### 功能之一為使用爬蟲爬取 聯合新聞網之圖片內容等 並顯示在 NBA新聞頁面上
##### 並使用爬蟲爬取 虎撲nba的統計資料 並結合 Echarts 將各隊務據以圖表形式顯示於網頁上
##### 再者使用 機器學習(LogisticRegression) 預測各隊比賽勝率
##### 資料來源為 Basketball Reference.com (利用每支隊伍過去的比賽情況作為特徵值 和 Elo等級分 來判斷每支比賽隊伍的勝率)
###### 此部分主要參考 [利用Python预测NBA比赛结果](https://blog.csdn.net/MOY37RQW1JarN33BgZk/article/details/80602924) 檔案在 model 資料夾中

__________________________________________________________________________________________________________________________

### 第三部分為電商網站功能
#### 用戶可於網站內購買商品加入購物車並以信用卡付款

__________________________________________________________________________________________________________________________

###### 最後附上參考文章連結
###### https://mp.weixin.qq.com/s/hqaPrPS7w3D-9SeegQAB2Q
###### https://ithelp.ithome.com.tw/articles/10212659
###### https://mp.weixin.qq.com/s/hqaPrPS7w3D-9SeegQAB2Q
##### https://www.cnblogs.com/huguodong/p/6611602.html
##### https://www.itread01.com/p/523920.html


