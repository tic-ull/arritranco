from __future__ import absolute_import

from celery import Celery
from kombu import  Queue
from django.conf import settings
import socket
from backups.scripts.stic_check import  compress_Checker, deletefile_Checker, verifybackup_Checker

app = Celery(settings.BACKUP_QUEUENAME, broker=settings.BROKER_URL)
if socket.gethostname() == settings.CHECKER:
    """ im the worker """
    queue = []
    queue.append(Queue(socket.gethostname(), routing_key=socket.gethostname()))
    app.conf.CELERY_QUEUES = queue

@app.task()
def verify_backupfile(fqdn, id, directory):
    """ verify the backupfiletask """
    verifybackup_Checker(fqdn, id, directory)

@app.task()
def compress_backupfile(filename,backup_id,directory,fqdn, id):
    """ compress backupfile """
    compress_Checker(backup_id,directory + filename)
    verifybackup_Checker(fqdn, id, directory)

@app.task()
def delete_backupfile(filename,fqdn):
    """ delete backupfile """
    deletefile_Checker(filename)
