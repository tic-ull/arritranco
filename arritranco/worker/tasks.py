from __future__ import absolute_import

from celery import Celery
from kombu import  Queue
from django.conf import settings
import socket
from worker.celery_app import app

@app.task()
def verify_backupfile(filename,backup_id,fqdn,id):
    """ verify backupfile """
    pass

@app.task()
def inventario_heartbeat():
    pass

