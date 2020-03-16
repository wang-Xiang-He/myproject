from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm

# 记得引入 Comment ！
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User

# 引入JsonResponse, 二级评论是通过iframe + ajax实现的
from django.http import JsonResponse


@login_required(login_url='/userprofile/login/')
# 新增参数  parent_comment_id=None。此参数代表父评论的id值，若为None则表示评论为一级评论，若有具体值则为多级评论。
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                # MPTT的get_root()方法将其父级重置为树形结构最底部的一级评论
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 新增代码，给其他用户发送通知
                # 用户之间可以互相评论，因此需要发送通知。if语句是为了防止管理员收到重复的通知。
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                    return HttpResponse('200 OK')

            new_comment.save()
            # 新增代码，给管理员发送通知
            # 第二个notify：普通用户回复时给管理员发送通知。
            if not request.user.is_superuser:
                notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
            # 新增代码，添加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            # 修改redirect参数
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")