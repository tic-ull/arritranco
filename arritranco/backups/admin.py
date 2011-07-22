'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import FileBackupTask, FileNamePattern, FileBackupProduct, BackupFile

class FileBackupTaskAdmin(admin.ModelAdmin):
    list_display = ('machine', 'duration', 'bckp_type', 'checker_fqdn', 'directory', 'days_in_hard_drive', 'max_backup_month')
    list_filter = ('bckp_type', 'checker_fqdn')
    list_editable = ('bckp_type', )

admin.site.register(FileBackupTask, FileBackupTaskAdmin)
admin.site.register(FileNamePattern)
admin.site.register(FileBackupProduct)
admin.site.register(BackupFile)
