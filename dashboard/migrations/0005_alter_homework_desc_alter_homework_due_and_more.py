# Generated by Django 4.1.4 on 2022-12-30 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_homework_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='desc',
            field=models.TextField(verbose_name='Chi tiết bài tập'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='due',
            field=models.DateTimeField(verbose_name='Hạn chót'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='Đã hoàn thành ?'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Tiêu đề'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='desc',
            field=models.TextField(verbose_name='Chi tiết ghi chú'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Tiêu đề'),
        ),
    ]
