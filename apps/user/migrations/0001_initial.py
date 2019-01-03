# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', max_length=30, unique=True)),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, related_query_name='user', related_name='user_set', verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'df_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('receiver', models.CharField(verbose_name='收件人', max_length=20)),
                ('addr', models.CharField(verbose_name='收件地址', max_length=256)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=6, null=True)),
                ('phone', models.CharField(verbose_name='联系电话', max_length=11)),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
                ('user', models.ForeignKey(verbose_name='所属账户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
