# Generated by Django 5.2 on 2025-05-17 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='category',
            field=models.CharField(choices=[('아이디어·창업·네이밍', '아이디어·창업·네이밍'), ('사진·영상', '사진·영상'), ('디자인·그림·웹툰', '디자인·그림·웹툰'), ('문학·학술·공학', '문학·학술·공학'), ('기타', '기타')], default='기타', max_length=30),
        ),
    ]
