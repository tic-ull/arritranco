# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FileBackupTask'
        db.create_table('backups_filebackuptask', (
            ('task_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scheduler.Task'], unique=True, primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Machine'])),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('bckp_type', self.gf('django.db.models.fields.IntegerField')(default=3, null=True, blank=True)),
            ('checker_fqdn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('directory', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('days_in_hard_drive', self.gf('django.db.models.fields.IntegerField')(default=90)),
            ('max_backup_month', self.gf('django.db.models.fields.IntegerField')(default=60)),
        ))
        db.send_create_signal('backups', ['FileBackupTask'])

        # Adding model 'FileNamePattern'
        db.create_table('backups_filenamepattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('backups', ['FileNamePattern'])

        # Adding model 'FileBackupProduct'
        db.create_table('backups_filebackupproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_backup_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_backup', to=orm['backups.FileBackupTask'])),
            ('file_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.FileNamePattern'])),
            ('start_seq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('end_seq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.FileBackupTask'])),
            ('variable_percentage', self.gf('django.db.models.fields.DecimalField')(default=20, null=True, max_digits=2, decimal_places=0, blank=True)),
        ))
        db.send_create_signal('backups', ['FileBackupProduct'])

        # Adding model 'BackupFile'
        db.create_table('backups_backupfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_backup_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.FileBackupProduct'])),
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
        db.send_create_signal('backups', ['BackupFile'])


    def backwards(self, orm):
        
        # Deleting model 'FileBackupTask'
        db.delete_table('backups_filebackuptask')

        # Deleting model 'FileNamePattern'
        db.delete_table('backups_filenamepattern')

        # Deleting model 'FileBackupProduct'
        db.delete_table('backups_filebackupproduct')

        # Deleting model 'BackupFile'
        db.delete_table('backups_backupfile')


    models = {
        'backups.backupfile': {
            'Meta': {'ordering': "['-original_date']", 'object_name': 'BackupFile'},
            'compressed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'compressed_file_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'compressed_file_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'compressed_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'deletion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'disk_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'file_backup_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backups.FileBackupProduct']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrity_checked': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'original_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'original_file_size': ('django.db.models.fields.FloatField', [], {}),
            'original_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'utility_checked': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'backups.filebackupproduct': {
            'Meta': {'object_name': 'FileBackupProduct'},
            'end_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'file_backup_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_backup'", 'to': "orm['backups.FileBackupTask']"}),
            'file_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backups.FileNamePattern']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backups.FileBackupTask']"}),
            'variable_percentage': ('django.db.models.fields.DecimalField', [], {'default': '20', 'null': 'True', 'max_digits': '2', 'decimal_places': '0', 'blank': 'True'})
        },
        'backups.filebackuptask': {
            'Meta': {'object_name': 'FileBackupTask', '_ormbases': ['scheduler.Task']},
            'bckp_type': ('django.db.models.fields.IntegerField', [], {'default': '3', 'null': 'True', 'blank': 'True'}),
            'checker_fqdn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'days_in_hard_drive': ('django.db.models.fields.IntegerField', [], {'default': '90'}),
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Machine']"}),
            'max_backup_month': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scheduler.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        'backups.filenamepattern': {
            'Meta': {'ordering': "['pattern']", 'object_name': 'FileNamePattern'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'inventory.machine': {
            'Meta': {'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.OperatingSystem']", 'null': 'True', 'blank': 'True'}),
            'start_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'update_priority': ('django.db.models.fields.IntegerField', [], {'default': '30'})
        },
        'inventory.operatingsystem': {
            'Meta': {'object_name': 'OperatingSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.OperatingSystemType']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'inventory.operatingsystemtype': {
            'Meta': {'object_name': 'OperatingSystemType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'scheduler.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'month': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'monthday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'weekday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'})
        }
    }

    complete_apps = ['backups']
