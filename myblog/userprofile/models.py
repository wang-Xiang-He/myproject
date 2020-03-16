from django.db import models

from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.
# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)

    # 头像
    avatar = ProcessedImageField(
        upload_to='userprofile/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )

    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# upload_to指定了图片上传的位置，即/media/avatar/%Y%m%d/。%Y%m%d是日期格式化的写法，会最终格式化为系统时间。
# 比如说图片上传是2018年12月5日，则图片会保存在/media/avatar/2018205/中。