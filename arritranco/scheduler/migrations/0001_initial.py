# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'scheduler_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('minute', self.gf('django.db.models.fields.CharField')(default='*', max_length=10)),
            ('hour', self.gf('django.db.models.fields.CharField')(default='*', max_length=10)),
            ('monthday', self.gf('django.db.models.fields.CharField')(default='*', max_length=10)),
            ('month', self.gf('django.db.models.fields.CharField')(default='*', max_length=10)),
            ('weekday', self.gf('django.db.models.fields.CharField')(default='*', max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'scheduler', ['Task'])

        # Adding model 'TaskCheck'
        db.create_table(u'scheduler_taskcheck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Task'])),
            ('task_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'scheduler', ['TaskCheck'])

        # Adding model 'TaskStatus'
        db.create_table(u'scheduler_taskstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_check', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.TaskCheck'])),
            ('check_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'scheduler', ['TaskStatus'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'scheduler_task')

        # Deleting model 'TaskCheck'
        db.delete_table(u'scheduler_taskcheck')

        # Deleting model 'TaskStatus'
        db.delete_table(u'scheduler_taskstatus')


    models = {
        u'scheduler.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'month': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'monthday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '10'}),
            'weekday': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '40'})
        },
        u'scheduler.taskcheck': {
            'Meta': {'object_name': 'TaskCheck'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

    complete_apps = ['scheduler']