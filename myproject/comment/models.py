from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost

# django-mptt 修改评论模型
from mptt.models import MPTTModel, TreeForeignKey

# django-ckeditor
from ckeditor.fields import RichTextField
# Create your models here.
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # body = models.TextField()
    body = RichTextField()
    # Ckeditor编辑器本身有一个inline-block的样式，
    # 阻碍了自适应效果，需要用Jquery语法将其清除掉。在详情页面底部加入

    created = models.DateTimeField(auto_now_add=True)


    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 新增，记录二级评论回复给谁
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # reply_to外键用于存储被评论人。
    # 举例说明：一级评论人为 a，二级评论人为 b（parent 为 a），三级评论人为 c（parent 为 b）
    # 因为我们不允许评论超过两级，
    # 因此将 c 的 parent 重置为 a，reply_to 记录为 b，这样就能正确追溯真正的被评论者了。

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]