from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm

# 記得引入 Comment ！
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User

# 引入JsonResponse, 二級評論是通過iframe + ajax實現的
from django.http import JsonResponse


@login_required(login_url='/userprofile/login/')
# 新增參數  parent_comment_id=None。此參數代表父評論的id值，若為None則表示評論為一級評論，若有具體值則為多級評論。
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 處理 POST 請求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二級回復
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回復層級超過二級，則轉換為二級
                # MPTT的get_root()方法將其父級重置為樹形結構最底部的一級評論
                new_comment.parent_id = parent_comment.get_root().id
                # 被回復人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 新增代碼，給其他用戶發送通知
                # 用戶之間可以互相評論，因此需要發送通知。if語句是為了防止管理員收到重複的通知。
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回復了你',
                        target=article,
                        action_object=new_comment,
                    )
                    return HttpResponse('200 OK')

            new_comment.save()
            # 新增代碼，給管理員發送通知
            # 第二個notify：普通用戶回復時給管理員發送通知。
            if not request.user.is_superuser:
                notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回復了你',
                        target=article,
                        action_object=new_comment,
                    )
            # 新增代碼，添加錨點
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            # 修改redirect參數
            return redirect(redirect_url)
        else:
            return HttpResponse("表單內容有誤，請重新填寫。")
    # 處理 GET 請求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 處理其他請求
    else:
        return HttpResponse("僅接受GET/POST請求。")