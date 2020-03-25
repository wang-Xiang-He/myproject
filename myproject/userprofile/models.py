from django.db import models

from django.contrib.auth.models import User
# 引入內置信號
from django.db.models.signals import post_save
# 引入信號接收器的裝飾器
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.
# 用戶擴展信息
class Profile(models.Model):
    # 與 User 模型構成一對一的關係
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 電話號碼字段
    phone = models.CharField(max_length=20, blank=True)

    # 頭像
    avatar = ProcessedImageField(
        upload_to='userprofile/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )

    # 個人簡介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# upload_to指定了圖片上傳的位置，即/media/avatar/%Y%m%d/。%Y%m%d是日期格式化的寫法，會最終格式化為系統時間。
# 比如說圖片上傳是2018年12月5日，則圖片會保存在/media/avatar/2018205/中。