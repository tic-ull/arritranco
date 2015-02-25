# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NagiosNrpeCheckOpts.description'
        db.add_column(u'sondas_nagiosnrpecheckopts', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NagiosNrpeCheckOpts.description'
        db.delete_column(u'sondas_nagiosnrpecheckopts', 'description')


    models = {
        u'hardware.hwbase': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'HwBase'},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.HwModel']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hardware.unrackablenetworkeddevice': {
            'Meta': {'object_name': 'UnrackableNetworkedDevice'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'main_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_in_building': ('django.db.models.fields.TextField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'switch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.Switch']"}),
            'wall_socket': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hardware_model.hwmodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'HwModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.HwType']"})
        },
        u'hardware_model.hwtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'HwType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'hardware_model.manufacturer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'inventory.machine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.OperatingSystem']"}),
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
        u'location.building': {
            'Meta': {'object_name': 'Building'},
            'area': ('django.db.models.fields.IntegerField', [], {}),
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Campus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_location': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'location.campus': {
            'Meta': {'object_name': 'Campus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'location.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Building']"}),
            'floor': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'monitoring.responsible': {
            'Meta': {'object_name': 'Responsible'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'nagios.nagioscheck': {
            'Meta': {'ordering': "['name']", 'object_name': 'NagiosCheck'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'default_params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.Machine']", 'null': 'True', 'through': u"orm['nagios.NagiosMachineCheckOpts']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nrpe': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nrpeservice'", 'to': u"orm['nagios.Service']", 'through': u"orm['sondas.NagiosNrpeCheckOpts']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'os': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.OperatingSystemType']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['nagios.Service']", 'null': 'True', 'through': u"orm['nagios.NagiosServiceCheckOpts']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheckTemplate']"}),
            'unrackable_networked_devices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hardware.UnrackableNetworkedDevice']", 'null': 'True', 'through': u"orm['nagios.NagiosUnrackableNetworkedDeviceCheckOpts']", 'blank': 'True'})
        },
        u'nagios.nagioschecktemplate': {
            'Meta': {'object_name': 'NagiosCheckTemplate'},
            'active_checks_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_command': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'check_freshness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'check_period': ('django.db.models.fields.CharField', [], {'default': "u'24x7'", 'max_length': '55'}),
            'event_handler_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'failure_prediction_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_notification_delay': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'flap_detection_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'freshness_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_volatile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_check_attempts': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notification_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '720'}),
            'notification_options': ('django.db.models.fields.CharField', [], {'default': "u'w,u,c,r'", 'max_length': '10'}),
            'notification_period': ('django.db.models.fields.CharField', [], {'default': "u'24x7'", 'max_length': '55'}),
            'notifications_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'obsess_over_service': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'passive_checks_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'process_perf_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'register': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'retain_nonstatus_information': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retain_status_information': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'retry_interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'nagios.nagioscontactgroup': {
            'Meta': {'object_name': 'NagiosContactGroup', '_ormbases': [u'monitoring.Responsible']},
            'ngcontact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'responsible_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monitoring.Responsible']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'nagios.nagiosmachinecheckopts': {
            'Meta': {'object_name': 'NagiosMachineCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Machine']"}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'nagios.nagiosservicecheckopts': {
            'Meta': {'object_name': 'NagiosServiceCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.Service']"})
        },
        u'nagios.nagiosunrackablenetworkeddevicecheckopts': {
            'Meta': {'object_name': 'NagiosUnrackableNetworkedDeviceCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'unrackable_networked_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']"})
        },
        u'nagios.service': {
            'Meta': {'object_name': 'Service'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Machine']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'network.ip': {
            'Meta': {'object_name': 'IP'},
            'addr': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'network_from_ip'", 'null': 'True', 'to': u"orm['network.Network']"})
        },
        u'network.managementinfo': {
            'Meta': {'object_name': 'ManagementInfo'},
            'backupconfigfile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'backupmethod': ('django.db.models.fields.IntegerField', [], {}),
            'backuppassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'backupusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'configtemplate': ('django.db.models.fields.TextField', [], {}),
            'defaultports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'oid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recommended_version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'network.network': {
            'Meta': {'object_name': 'Network'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'first_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'network.switch': {
            'Meta': {'object_name': 'Switch'},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'main_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'managementinfo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.ManagementInfo']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Rack']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'sondas.nagiosnrpecheckopts': {
            'Meta': {'object_name': 'NagiosNrpeCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.Service']"}),
            'sonda': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sondas.Sonda']", 'symmetrical': 'False'})
        },
        u'sondas.sonda': {
            'Meta': {'object_name': 'Sonda'},
            'dir_checks': ('django.db.models.fields.CharField', [], {'default': "'/usr/lib/nagios/plugins'", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'nrpe_service_name': ('django.db.models.fields.CharField', [], {'default': "'nagios-nrpe-server'", 'max_length': '400'}),
            'script_end': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'script_inicio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servidor_nagios': ('django.db.models.fields.CharField', [], {'default': "'127.0.0.1'", 'max_length': '400'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'ssh': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unrackable_networked_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']"})
        },
        u'sondas.sondatask': {
            'Meta': {'object_name': 'SondaTask'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'sondas.sondataskslog': {
            'Meta': {'object_name': 'SondaTasksLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sonda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sondas.Sonda']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sondas.SondaTask']"})
        },
        u'sondas.sondataskstatus': {
            'Meta': {'object_name': 'SondaTaskStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'tasklog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sondas.SondaTasksLog']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['sondas']