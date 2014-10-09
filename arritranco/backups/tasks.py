from __future__ import absolute_import

from celery import Celery
from kombu import  Queue
from django.conf import settings
import socket
from backups.scripts.stic_check import  compress_Checker, deletefile_Checker, verifybackup_Checker
from arritranco.celery import app

#app = Celery(settings.BACKUP_QUEUENAME, broker=settings.BROKER_URL)
if socket.gethostname() == settings.CHECKER:
    """ im the worker """
    queue = []
    queue.append(Queue(settings.CHECKER, routing_key=settings.CHECKER))
    app.conf.CELERY_QUEUES = queue

@app.task(ignore_result=True)
def verify_backupfile(fqdn, id, directory):
    """ verify the backupfiletask """
    return True

<<<<<<< HEAD
@app.task()
def compress_backupfile(filename,backup_id,directory,fqdn,id):
=======
@app.task(ignore_result=True)
def compress_backupfile(filename,backup_id,directory,fqdn, id):
>>>>>>> 402dd460d88f5d860e9e42b82bdf5c3ca673df17
    """ compress backupfile """
    compress_Checker(backup_id,directory + filename)
    verifybackup_Checker(fqdn, id, directory)
    return True

@app.task(ignore_result=True)
def delete_backupfile(filename,fqdn):
    """ delete backupfile """
    deletefile_Checker(filename)
    return True
