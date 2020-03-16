from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse

# Create your views here.
def news(request):
	search_list = []

	res = requests.get("https://udn.com/search/word/2/NBA")

	# 關鍵字多加一個雙引號是精準搜尋
	# num: 一次最多要request的筆數, 可減少切換頁面的動作
	# tbs: 資料時間, hour(qdr:h), day(qdr:d), week(qdr:w), month(qdr:m), year(qdr:w)

	if res.status_code == 200:
	    content = res.content
	    soup = BeautifulSoup(content, "html.parser")
	    # print(soup.prettify())

	    items = soup.findAll("div", {"class": "story-list__news"})
	    # print(items)
	    for item in items:
	        # print(item)
	        news= item.find('a')
	        # title
	        newstitle = news.get('aria-label')
	        if newstitle:
	            # title
	            news_title = newstitle
	            print(news_title)

	            # url
	            url = item.find('a')
	            news_link = item.find('a').get('href')
	            print(news_link)

	            #content
	            news_text = item.find('p').text
	            print(news_text)

	            # img
	            news_img = item.find('source').get('data-srcset')
	            print(news_img)
	            # news_img = item.find('img')
	            # news_imgs = soup.findAll("picture")
	            # for news_img in news_imgs:
	            #     news_img = news_img.find('source').get('data-srcset')
	            #     print(news_img)

	            # time
	            time_created = item.find('time').text
	            print(time_created)

	            search_list.append({
	            "news_title": news_title,
	            "news_link": news_link,
	            "news_text": news_text,
	            "news_img": news_img,
	            "time_created": time_created
	        })

	        else:
	            break

	        # add item into json object


	return render(request, 'news/news.html', locals())

