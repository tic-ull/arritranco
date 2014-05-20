# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BackupTask'
        db.create_table(u'backups_backuptask', (
            (u'task_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scheduler.Task'], unique=True, primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Machine'])),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('extra_options', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bckp_type', self.gf('django.db.models.fields.IntegerField')(default=3, null=True, blank=True)),
        ))
        db.send_create_signal(u'backups', ['BackupTask'])

        # Adding model 'VCBBackupTask'
        db.create_table(u'backups_vcbbackuptask', (
            (u'backuptask_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backups.BackupTask'], unique=True, primary_key=True)),
            ('tsm_server', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'backups', ['VCBBackupTask'])

        # Adding model 'TSMBackupTask'
        db.create_table(u'backups_tsmbackuptask', (
            (u'backuptask_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backups.BackupTask'], unique=True, primary_key=True)),
            ('tsm_server', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'backups', ['TSMBackupTask'])

        # Adding model 'R1BackupTask'
        db.create_table(u'backups_r1backuptask', (
            (u'backuptask_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backups.BackupTask'], unique=True, primary_key=True)),
            ('r1_server', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'backups', ['R1BackupTask'])

        # Adding model 'FileBackupTask'
        db.create_table(u'backups_filebackuptask', (
            (u'backuptask_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backups.BackupTask'], unique=True, primary_key=True)),
            ('checker_fqdn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('directory', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('days_in_hard_drive', self.gf('django.db.models.fields.IntegerField')(default=180)),
            ('max_backup_month', self.gf('django.db.models.fields.IntegerField')(default=7)),
        ))
        db.send_create_signal(u'backups', ['FileBackupTask'])

        # Adding model 'FileNamePattern'
        db.create_table(u'backups_filenamepattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'backups', ['FileNamePattern'])

        # Adding model 'FileBackupProduct'
        db.create_table(u'backups_filebackupproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_backup_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_backup', to=orm['backups.FileBackupTask'])),
            ('file_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.FileNamePattern'])),
            ('start_seq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('end_seq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('variable_percentage', self.gf('django.db.models.fields.DecimalField')(default=20, null=True, max_digits=2, decimal_places=0, blank=True)),
        ))
        db.send_create_signal(u'backups', ['FileBackupProduct'])

        # Adding model 'BackupFile'
        db.create_table(u'backups_backupfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_backup_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.FileBackupProduct'])),
            ('task_check', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.TaskCheck'], null=True, blank=True)),
            ('original_file_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('original_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('original_file_size', self.gf('django.db.models.fields.FloatField')()),
            ('original_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('compressed_file_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('compressed_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('compressed_file_size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('compressed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deletion_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('disk_id', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('integrity_checked', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('utility_checked', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'backups', ['BackupFile'])


    def backwards(self, orm):
        # Deleting model 'BackupTask'
        db.delete_table(u'backups_backuptask')

        # Deleting model 'VCBBackupTask'
        db.delete_table(u'backups_vcbbackuptask')

        # Deleting model 'TSMBackupTask'
        db.delete_table(u'backups_tsmbackuptask')

        # Deleting model 'R1BackupTask'
        db.delete_table(u'backups_r1backuptask')

        # Deleting model 'FileBackupTask'
        db.delete_table(u'backups_filebackuptask')

        # Deleting model 'FileNamePattern'
        db.delete_table(u'backups_filenamepattern')

        # Deleting model 'FileBackupProduct'
        db.delete_table(u'backups_filebackupproduct')

        # Deleting model 'BackupFile'
        db.delete_table(u'backups_backupfile')


    models = {
        u'backups.backupfile': {
            'Meta': {'ordering': "['-original_date']", 'object_name': 'BackupFile'},
            'compressed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'compressed_file_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'compressed_file_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'compressed_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'deletion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'disk_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'file_backup_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backups.FileBackupProduct']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrity_checked': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'original_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'original_file_size': ('django.db.models.fields.FloatField', [], {}),
            'original_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'task_check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scheduler.TaskCheck']", 'null': 'True', 'blank': 'True'}),
            'utility_checked': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'backups.backuptask': {
            'Meta': {'object_name': 'BackupTask', '_ormbases': [u'scheduler.Task']},
            'bckp_type': ('django.db.models.fields.IntegerField', [], {'default': '3', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'extra_options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Machine']"}),
            u'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['scheduler.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'backups.filebackupproduct': {
            'Meta': {'object_name': 'FileBackupProduct'},
            'end_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'file_backup_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_backup'", 'to': u"orm['backups.FileBackupTask']"}),
            'file_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backups.FileNamePattern']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'variable_percentage': ('django.db.models.fields.DecimalField', [], {'default': '20', 'null': 'True', 'max_digits': '2', 'decimal_places': '0', 'blank': 'True'})
        },
        u'backups.filebackuptask': {
            'Meta': {'object_name': 'FileBackupTask', '_ormbases': [u'backups.BackupTask']},
            u'backuptask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['backups.BackupTask']", 'unique': 'True', 'primary_key': 'True'}),
            'checker_fqdn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'days_in_hard_drive': ('django.db.models.fields.IntegerField', [], {'default': '180'}),
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'max_backup_month': ('django.db.models.fields.IntegerField', [], {'default': '7'})
        },
        u'backups.filenamepattern': {
            'Meta': {'ordering': "['pattern']", 'object_name': 'FileNamePattern'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'backups.r1backuptask': {
            'Meta': {'object_name': 'R1BackupTask', '_ormbases': [u'backups.BackupTask']},
            u'backuptask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['backups.BackupTask']", 'unique': 'True', 'primary_key': 'True'}),
            'r1_server': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'backups.tsmbackuptask': {
            'Meta': {'object_name': 'TSMBackupTask', '_ormbases': [u'backups.BackupTask']},
            u'backuptask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['backups.BackupTask']", 'unique': 'True', 'primary_key': 'True'}),
            'tsm_server': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'backups.vcbbackuptask': {
            'Meta': {'object_name': 'VCBBackupTask', '_ormbases': [u'backups.BackupTask']},
            u'backuptask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['backups.BackupTask']", 'unique': 'True', 'primary_key': 'True'}),
            'tsm_server': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inventory.machine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.OperatingSystem']", 'null': 'True', 'blank': 'True'}),
            'start_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'up_to_date_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'update_priority': ('django.db.models.fields.IntegerField', [], {'default': '30'})
        },
        u'inventory.operatingsystem': {
            'Meta': {'object_name': 'OperatingSystem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.OperatingSystemType']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.operatingsystemtype': {
            'Meta': {'object_name': 'OperatingSystemType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'scheduler.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '10'}),
            'month': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'monthday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'weekday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '40'})
        },
        u'scheduler.taskcheck': {
            'Meta': {'object_name': 'TaskCheck'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scheduler.TaskStatus']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scheduler.Task']"}),
            'task_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'scheduler.taskstatus': {
            'Meta': {'object_name': 'TaskStatus'},
            'check_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task_check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scheduler.TaskCheck']"})
        }
    }

    complete_apps = ['backups']