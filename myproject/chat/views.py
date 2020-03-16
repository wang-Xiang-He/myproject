from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import redis
from django.shortcuts import render,HttpResponse
from django_redis import get_redis_connection

# def index(request):
#     conn = get_redis_connection("default")
#     return HttpResponse('设置成功')

# def order(request):
#     conn = get_redis_connection("default")
#     return HttpResponse('获取成功')


@login_required(login_url='/userprofile/login/')
def chat(request):
    # conn = get_redis_connection("default")
    return render(request, 'chat/chat.html')