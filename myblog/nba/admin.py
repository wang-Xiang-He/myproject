from django.contrib import admin
# Register your models here.
from .models import NBAData
# 把創建的model庫 連接網頁
admin.site.register(NBAData)
