# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TaskCheck.last_status'
        db.add_column(u'scheduler_taskcheck', 'last_status',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 4, 22, 0, 0), max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TaskCheck.last_status'
        db.delete_column(u'scheduler_taskcheck', 'last_status')


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
            'last_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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