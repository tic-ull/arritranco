'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import FileBackupTask, FileNamePattern, FileBackupProduct, BackupFile

admin.site.register(FileBackupTask)
admin.site.register(FileNamePattern)
admin.site.register(FileBackupProduct)
admin.site.register(BackupFile)
