#!/bin/sh

# wait for db server to start
sleep 3

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
celery -A celery_tasks.tasks worker -l info
#celery worker -A dailyfresh.celeryconf -Q default -n default@%h