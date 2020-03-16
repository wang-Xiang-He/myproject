from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.models import User

# 引入驗證登錄的裝飾器
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile
# Create your views here.

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user_login_form = UserLoginForm(data=request.POST)
            if user_login_form.is_valid():
                # cleaned_data 清洗出合法數據
                # 檢驗賬號、密碼是否正確匹配數據庫中的某個用戶
                # 如果均匹配則返回這個 user 對象
                data = user_login_form.cleaned_data
                user = authenticate(username=data['username'], password=data['password'])
                if user:
                    # 將用戶數據保存在 session 中，即實現了登錄動作
                    login(request, user)
                    return redirect("article:article_list")
                else:
                    return HttpResponse("賬號或密碼輸入有誤。請重新輸入~")
            else:
                return HttpResponse("賬號或密碼輸入不合法")
        elif request.method == 'GET':
            user_login_form = UserLoginForm()
            return render(request, 'userprofile/login.html', locals())
        else:
            return render(request, 'userprofile/login.html')
    else:
        return redirect("article:article_list")

def user_logout(request):
    logout(request)
    return redirect("nba:homepage")


# 用戶註冊
def user_register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user_register_form = UserRegisterForm(data=request.POST)
            if user_register_form.is_valid():
                data = user_register_form.cleaned_data
                password = User.objects.filter(password=data['password'])
                if not password:
                    new_user = user_register_form.save()
                    # 保存好數據後立即登錄並返回博客列表頁面
                    login(request, new_user,  backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("article:article_list")
                else:
                    message = "註冊表單輸入有誤。請重新輸入~"
                    return render(request, 'userprofile/register.html', locals())
            else:
                message = "註冊表單輸入有誤。請重新輸入~"
                return render(request, 'userprofile/register.html', locals())

        elif request.method == 'GET':
            user_register_form = UserRegisterForm()

            return render(request, 'userprofile/register.html', locals())
        else:
            message = "註冊表單輸入有誤。請重新輸入~"
            return render(request, 'userprofile/register.html', locals())
    else:
        return redirect("article:article_list")



@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 驗證登錄用戶、待刪除用戶是否相同
        if request.user == user:
            #退出登錄，刪除數據並返回博客列表
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你沒有刪除操作的權限。")
    else:
        return HttpResponse("僅接受post請求。")


# 編輯用戶信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自動生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 驗證修改數據者，是否為用戶本人
        if request.user != user:
            return HttpResponse("你沒有權限修改此用戶信息。")

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗後的合法數據
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            # print(profile_cd['phone'])
            # print(profile.phone)
            profile.bio = profile_cd['bio']
            profile.save()
            # 如果 request.FILES 存在文件，則保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
                profile.save()
                print('save')
            # 帶參數的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("註冊表單輸入有誤。請重新輸入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("請使用GET或POST請求數據")
