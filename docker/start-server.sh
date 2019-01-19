#!/bin/bash

echo "※※※==============正在启动Django服务器======================※※※"
sleep 5
python manage.py makemigrations
python manage.py migrate
uwsgi --ini uwsgi.ini
uwsgi --ini uwsgi2.ini
python manage.py runserver 0.0.0.0:8000
echo "※※※==============正在启动队列任务管理后台======================※※※"
sleep 5
celery flower --broker=redis://redis:6379/1

echo "※※※==============部署已完成,谢谢=======================※※※"

