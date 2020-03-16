from django.db import models
# Create your models here.
class NBAData(models.Model):
    ranking = models.IntegerField(verbose_name='排名')
    ballgame = models.CharField(max_length=50,verbose_name='球隊')
    win = models.IntegerField(verbose_name='勝場')
    transport = models.IntegerField(verbose_name='敗場')
    winrate = models.CharField(max_length=50,verbose_name='勝率')
    logopath = models.ImageField(null=True, upload_to="images", verbose_name="球隊logo",blank=True)
    area = models.CharField(max_length=50,verbose_name='區域')

    def __str__(self):
        return self.ballgame

