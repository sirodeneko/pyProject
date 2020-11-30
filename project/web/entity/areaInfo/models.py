from django.db import models


# Create your models here.
class AreaInfo(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    des = models.CharField(max_length=200)
    time = models.CharField(max_length=50)
    grade = models.CharField(max_length=20)
    t_time = models.CharField(max_length=50)
    max_num = models.IntegerField()
    ssd = models.CharField(max_length=50)
    num = models.IntegerField()
    type = models.CharField(max_length=100)
    t_code = models.CharField(max_length=100)
    v_id = models.ForeignKey('Versions', on_delete=models.PROTECT, verbose_name='更新版本号')

    class Meta:
        db_table = "area_info"


class Versions(models.Model):
    v_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "versions"
