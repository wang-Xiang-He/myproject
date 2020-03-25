from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from django.contrib.auth.models import User
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from .models import ArticleColumn
from comment.forms import CommentForm
from django.views import View
# Create your views here.
def article_list(request):
    # 從 url 中提取查詢參數
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查詢集
    article_list = ArticlePost.objects.all()

    # 搜索查詢集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 欄目查詢集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 標籤查詢集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
        #filter(tags__name__in=[tag])，
        # 意思是在tags字段中過濾name為tag的數據條目。賦值的字符串tag用方括號包起來。

    # 查詢集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)


    return render(request, 'article/list.html', locals())


@login_required(login_url='/userprofile/login/')
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 引入評論表單
    comment_form = CommentForm()

    # 取出文章評論
    comments = Comment.objects.filter(article=article)
    # 瀏覽量 +1
    article.total_views += 1
    # update_fields=[]指定了數據庫只更新total_views字段，優化執行效率
    article.save(update_fields=['total_views'])

    # 將markdown語法渲染成html樣式

# # 國風·周南·關雎

# **關關雎鳩，在河之洲。窈窕淑女，君子好逑。**

# 參差荇菜，左右流之。窈窕淑女，寤寐求之。

# + 列表一
# + 列表二
#     + 列表二-1
#     + 列表二-2
    # 修改 Markdown 語法渲染
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 目錄
    # 一級標題：# title1，二級標題：## title2
    toc = md.toc
    # 然後你可以在文中的任何地方插入[TOC]字符串，目錄就自動生成好了：
    return render(request, 'article/detail.html', locals())


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判斷用戶是否提交數據
    if request.method == "POST":
        # 將提交的數據賦值到表單實例中
        # 因為POST的表單中包含了圖片文件，
        # 所以要將request.FILES也一併綁定到表單類中，否則圖片無法正確保存：
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判斷提交的數據是否滿足模型的要求
        if article_post_form.is_valid():
            # 保存數據，但暫時不提交到數據庫中
            new_article = article_post_form.save(commit=False)
            # 指定數據庫中 id=1 的用戶為作者
            # 如果你進行過刪除數據表的操作，可能會找不到id=1的用戶
            # 此時請重新創建用戶，並傳入此用戶的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 將新文章保存到數據庫中
            new_article.save()
            # 完成後返回到文章列表
            # 新增代碼，保存 tags 的多對多關係
            article_post_form.save_m2m()
            # 如果提交的表單使用了commit=False選項，
            # 則必須調用save_m2m()才能正確的保存標籤，就像普通的多對多關係一樣。
            return redirect("article:article_list")
        # 如果數據不合法，返回錯誤信息
        else:
            return redirect("article:article_list")
    # 如果用戶請求獲取數據
    else:
        # 創建表單類實例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()

        # 返回模板
        return render(request, 'article/create.html', locals())


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    # 根據 id 獲取需要刪除的文章
    article = ArticlePost.objects.get(id=id)
    # 調用.delete()方法刪除文章
    article.delete()
    # 完成刪除後返回文章列表
    return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("僅允許post請求")

# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的視圖函數
    通過POST方法提交表單，更新titile、body字段
    GET方法進入初始表單頁面
    id： 文章的 id
    """

    # 獲取需要修改的具體文章對象
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你無權修改這篇文章。")
    # 判斷用戶是否為 POST 提交表單數據
    if request.method == "POST":
        # 將提交的數據賦值到表單實例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判斷提交的數據是否滿足模型的要求
        if article_post_form.is_valid():
            # 保存新寫入的 title、body 數據並保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 新增的代碼
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 完成後返回到修改後的文章中。需傳入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果數據不合法，返回錯誤信息
        else:
            return HttpResponse("表單內容有誤，請重新填寫。")

    # 如果用戶 GET 請求獲取數據
    else:
        # 創建表單類實例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 賦值上下文，將 article 文章對象也傳遞進去，以便提取舊的內容
        # 將響應返回到模板中
        return render(request, 'article/update.html', locals())


# 點讚數 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')