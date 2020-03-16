from django.db import models

from django.contrib.auth.models import User
# timezone 用於處理時間相關事務。
from django.utils import timezone

# 引入內置信號
from django.db.models.signals import post_save
# 引入信號接收器的裝飾器
from django.dispatch import receiver

from django.urls import reverse

# Django-taggit
from taggit.managers import TaggableManager

from ckeditor.fields import RichTextField

# 記得導入處理圖片！
from PIL import Image

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class ArticleColumn(models.Model):
    """
    欄目的 Model
    """
    # 欄目標題
    title = models.CharField(max_length=100, blank=True)
    # 創建時間
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章數據模型
class ArticlePost(models.Model):
    # 文章作者。參數 on_delete 用於指定數據刪除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章標題。models.CharField 為字符串字段，用於保存較短的字符串，比如標題
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    # body = models.TextField()
    body = RichTextField()

    # 文章創建時間。參數 default=timezone.now 指定其在創建數據時將默認寫入當前的時間
    created = models.DateTimeField(default=timezone.now)

    # 文章更新時間。參數 auto_now=True 指定每次數據更新時自動寫入當前時間
    updated = models.DateTimeField(auto_now=True)

    total_views = models.PositiveIntegerField(default=0)

    # 文章標籤
    tags = TaggableManager(blank=True)

    # 文章標題圖
    # avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 注意上傳地址中的%Y%m%d是日期格式化的寫法。比如上傳時間是2019年2月26日，
    # 則標題圖會上傳到media/article/20190226這個目錄中。

    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 新增点赞数统计
    likes = models.PositiveIntegerField(default=0)

        # 內部類 class Meta 用於給 model 定義元數據
    class Meta:
        # ordering 指定模型返回的數據的排列順序
        # '-created' 表明數據應該以倒序排列
        ordering = ('-created',)
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    # 獲取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])


# 保存時處理圖片
# avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)才要用
    def save(self, *args, **kwargs):
        # 調用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)
        # super(ArticlePost, self).save(*args, **kwargs)
        # 的作用是調用父類中原有的save()方法，即將model中的字段數據保存到數據庫中

        # 固定寬度縮放圖片大小
        # 博文的標題圖不是必須的，if中的self.avatar剔除掉沒有標題圖的文章，
        # 這些文章不需要處理圖片。
        # 不太好理解的是if中的這個not kwargs.get('update_fields')。
        # 還記得article_detail()視圖中為了統計瀏覽量而調用了
        # save(update_fields=['total_views'])嗎？沒錯，
        # 就是為了排除掉統計瀏覽量調用的save()，
        # 免得每次用戶進入文章詳情頁面都要處理標題圖，太影響性能了。

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            #Image.ANTIALIAS表示縮放採用平滑濾波
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            #self.avatar.path 為圖片要保存的路徑
            resized_image.save(self.avatar.path)

        return article

    # 函數 __str__ 定義當調用對象的 str() 方法時的返回值內容
    def __str__(self):
        # return self.title 將文章標題返回
        return self.title


