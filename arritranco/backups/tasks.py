from __future__ import absolute_import

from celery import Celery
from kombu import  Queue
from django.conf import settings
import socket

app = Celery(settings.BACKUP_QUEUENAME, broker=settings.BROKER_URL)
if socket.gethostname() == settings.CHECKER:
    """ im the worker """
    queue = []
    queue.append(Queue(settings.CHECKER, routing_key=settings.CHECKER))
    app.conf.CELERY_QUEUES = queue

@app.task()
def verify_backupfile(fqdn, id, directory):
    """ verify the backupfiletask """
    return True

@app.task()
def compress_backupfile(filename,backup_id,directory,fqdn,id):
    """ compress backupfile """
    return True

@app.task()
def delete_backupfile(filename,fqdn):
    """ delete backupfile """
    return True

