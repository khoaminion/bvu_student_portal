from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Tiêu đề',max_length=200)
    desc = models.TextField('Chi tiết ghi chú')

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural = 'notes'

    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField('Môn học',max_length=80)
    title = models.CharField('Tiêu đề',max_length=100)
    desc = models.TextField('Chi tiết bài tập')
    due = models.DateTimeField('Hạn chót')
    is_finished = models.BooleanField('Đã hoàn thành ?',default=False)
    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField('Tiêu đề',max_length=100)
    is_finished = models.BooleanField('Đã hoàn thành ?',default=False)
    def __str__(self):
        return self.title
