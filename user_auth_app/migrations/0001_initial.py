# Generated by Django 2.2.2 on 2019-07-25 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('mobile', models.CharField(max_length=30, verbose_name='手机号')),
                ('pwd', models.CharField(max_length=50, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='Verity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
            ],
        ),
    ]