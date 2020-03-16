from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost



# Create your views here.
# CommentNoticeListView：继承自ListView，用于展示所有的未读通知。
# get_queryset方法返回了传递给模板的上下文对象，
# unread()方法是django-notifications提供的，用于获取所有未读通知的集合。
# 另外视图还继承了“混入类”LoginRequiredMixin，要求调用此视图必须先登录。
class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称,將object_list名稱轉為notices
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/userprofile/login/'

    # 未读通知的查询集,必要函數返回 object_list
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
# CommentNoticeUpdateView：继承自View，获得了如get、post等基础的方法。
# mark_as_read()、mark_all_as_read都是模块提供的方法，
# 用于将未读通知转换为已读。if语句用来判断转换单条还是所有未读通知。
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')