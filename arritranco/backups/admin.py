'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import FileBackupTask, FileNamePattern, FileBackupProduct, BackupFile
from models import BackupTask, R1BackupTask, TSMBackupTask

class FileBackupProductAdmin(admin.ModelAdmin):
    list_display = ('file_backup_task', 'file_pattern', 'variable_percentage')

class FileBackupProductInline(admin.TabularInline):
    model = FileBackupProduct
    extra = 4

class FileBackupTaskAdmin(admin.ModelAdmin):
    list_display = ('machine', 'active', 'duration', 'bckp_type', 'description', 'checker_fqdn', 'directory', 'days_in_hard_drive', 'max_backup_month')
    list_filter = ('bckp_type', 'checker_fqdn')
    list_editable = ('bckp_type', )
    search_fields = ['machine__fqdn', 'directory', 'checker_fqdn', 'description']
    inlines = [FileBackupProductInline, ]  

class BackupFileAdmin(admin.ModelAdmin):
    list_display = ('original_file_name', 'original_date', 'original_file_size_display', 'machine', 'checker', 'deletion_date')
    search_fields = ['original_file_name', 'compressed_file_name', 'file_backup_product__file_backup_task__machine__fqdn']
    raw_id_fields = ('file_backup_product', 'task_check')
    date_hierarchy = 'original_date'
    list_filter = ('file_backup_product__file_backup_task__checker_fqdn',)

class FileNamePatternAdmin(admin.ModelAdmin):
    search_fields = ['pattern', ]

class TSMBackupTaskAdmin(admin.ModelAdmin):
    list_display = ('machine', 'description', 'tsm_server', )
    list_filter = ('bckp_type', 'tsm_server')
    list_editable = ('tsm_server', )
    search_fields = ['machine__fqdn', 'tsm_server', 'description']

admin.site.register(FileBackupTask, FileBackupTaskAdmin)
admin.site.register(TSMBackupTask, TSMBackupTaskAdmin)
admin.site.register(FileNamePattern, FileNamePatternAdmin)
admin.site.register(R1BackupTask)
admin.site.register(BackupFile, BackupFileAdmin)
