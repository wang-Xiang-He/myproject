from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost



# Create your views here.
# CommentNoticeListView：繼承自ListView，用於展示所有的未讀通知。
# get_queryset方法返回了傳遞給模板的上下文對象，
# unread()方法是django-notifications提供的，用於獲取所有未讀通知的集合。
# 另外視圖還繼承了“混入類”LoginRequiredMixin，要求調用此視圖必須先登錄。
class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名稱,將object_list名稱轉為notices
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登錄重定向
    login_url = '/userprofile/login/'

    # 未讀通知的查詢集,必要函數返回 object_list
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
# CommentNoticeUpdateView：繼承自View，獲得了如get、post等基礎的方法。
# mark_as_read()、mark_all_as_read都是模塊提供的方法，
# 用於將未讀通知轉換為已讀。if語句用來判斷轉換單條還是所有未讀通知。
    """更新通知狀態"""
    # 處理 get 請求
    def get(self, request):
        # 獲取未讀消息
        notice_id = request.GET.get('notice_id')
        # 更新單條通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')