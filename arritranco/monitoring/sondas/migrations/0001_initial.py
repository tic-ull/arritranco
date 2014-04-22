# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NagiosNrpeCheckOpts'
        db.create_table(u'sondas_nagiosnrpecheckopts', (
            (u'nagiosopts_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nagios.NagiosOpts'], unique=True, primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nagios.Service'])),
        ))
        db.send_create_signal(u'sondas', ['NagiosNrpeCheckOpts'])

        # Adding M2M table for field sonda on 'NagiosNrpeCheckOpts'
        m2m_table_name = db.shorten_name(u'sondas_nagiosnrpecheckopts_sonda')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagiosnrpecheckopts', models.ForeignKey(orm[u'sondas.nagiosnrpecheckopts'], null=False)),
            ('sonda', models.ForeignKey(orm[u'sondas.sonda'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagiosnrpecheckopts_id', 'sonda_id'])

        # Adding model 'Sonda'
        db.create_table(u'sondas_sonda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('unrackable_networked_device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.UnrackableNetworkedDevice'])),
            ('ssh', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dir_checks', self.gf('django.db.models.fields.CharField')(default='/usr/lib/nagios/plugins', max_length=500)),
            ('servidor_nagios', self.gf('django.db.models.fields.CharField')(default='193.145.118.253', max_length=400)),
            ('nrpe_service_name', self.gf('django.db.models.fields.CharField')(default='nagios-nrpe-server', max_length=400)),
            ('script_inicio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('script_end', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sondas', ['Sonda'])

        # Adding model 'SondaTask'
        db.create_table(u'sondas_sondatask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sondas', ['SondaTask'])

        # Adding model 'SondaTasksLog'
        db.create_table(u'sondas_sondataskslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sonda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sondas.Sonda'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sondas.SondaTask'])),
        ))
        db.send_create_signal(u'sondas', ['SondaTasksLog'])

        # Adding model 'SondaTaskStatus'
        db.create_table(u'sondas_sondataskstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tasklog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sondas.SondaTasksLog'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'sondas', ['SondaTaskStatus'])


    def backwards(self, orm):
        # Deleting model 'NagiosNrpeCheckOpts'
        db.delete_table(u'sondas_nagiosnrpecheckopts')

        # Removing M2M table for field sonda on 'NagiosNrpeCheckOpts'
        db.delete_table(db.shorten_name(u'sondas_nagiosnrpecheckopts_sonda'))

        # Deleting model 'Sonda'
        db.delete_table(u'sondas_sonda')

        # Deleting model 'SondaTask'
        db.delete_table(u'sondas_sondatask')

        # Deleting model 'SondaTasksLog'
        db.delete_table(u'sondas_sondataskslog')

        # Deleting model 'SondaTaskStatus'
        db.delete_table(u'sondas_sondataskstatus')


    models = {
        u'hardware.hwbase': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'HwBase'},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.HwModel']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hardware.networkeddevice': {
            'Meta': {'object_name': 'NetworkedDevice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"})
        },
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hardware.unrackable': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'Unrackable', '_ormbases': [u'hardware.HwBase']},
            u'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"})
        },
        u'hardware.unrackablenetworkeddevice': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'UnrackableNetworkedDevice', '_ormbases': [u'hardware.Unrackable', u'hardware.NetworkedDevice']},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'networkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.NetworkedDevice']", 'unique': 'True'}),
            'place_in_building': ('django.db.models.fields.TextField', [], {}),
            'switch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.Switch']"}),
            u'unrackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.Unrackable']", 'unique': 'True', 'primary_key': 'True'}),
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
        u'inventory.interface': {
            'Meta': {'object_name': 'Interface'},
            'hwaddr': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_new': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.Network']", 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'inventory.machine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['network.Network']", 'through': u"orm['inventory.Interface']", 'symmetrical': 'False'}),
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
            'Meta': {'object_name': 'NagiosCheck'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.Machine']", 'null': 'True', 'through': u"orm['nagios.NagiosMachineCheckOpts']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nrpe': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nrpeservice'", 'to': u"orm['nagios.Service']", 'through': u"orm['sondas.NagiosNrpeCheckOpts']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'os': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.OperatingSystemType']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['nagios.Service']", 'null': 'True', 'through': u"orm['nagios.NagiosServiceCheckOpts']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unrackable_networked_devices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hardware.UnrackableNetworkedDevice']", 'null': 'True', 'through': u"orm['nagios.NagiosUnrackableNetworkedDeviceCheckOpts']", 'blank': 'True'})
        },
        u'nagios.nagioscontactgroup': {
            'Meta': {'object_name': 'NagiosContactGroup', '_ormbases': [u'monitoring.Responsible']},
            'ngcontact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'responsible_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monitoring.Responsible']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'nagios.nagiosmachinecheckopts': {
            'Meta': {'object_name': 'NagiosMachineCheckOpts', '_ormbases': [u'nagios.NagiosOpts']},
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Machine']"}),
            u'nagiosopts_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['nagios.NagiosOpts']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'nagios.nagiosopts': {
            'Meta': {'object_name': 'NagiosOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'nagios.nagiosservicecheckopts': {
            'Meta': {'object_name': 'NagiosServiceCheckOpts', '_ormbases': [u'nagios.NagiosOpts']},
            u'nagiosopts_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['nagios.NagiosOpts']", 'unique': 'True', 'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.Service']"})
        },
        u'nagios.nagiosunrackablenetworkeddevicecheckopts': {
            'Meta': {'object_name': 'NagiosUnrackableNetworkedDeviceCheckOpts', '_ormbases': [u'nagios.NagiosOpts']},
            u'nagiosopts_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['nagios.NagiosOpts']", 'unique': 'True', 'primary_key': 'True'}),
            'unrackable_networked_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']"})
        },
        u'nagios.service': {
            'Meta': {'object_name': 'Service'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Machine']", 'symmetrical': 'False'}),
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
            'first_ip_int': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_ip_int': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'network.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': [u'hardware.NetworkedDevice']},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'managementinfo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.ManagementInfo']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'networkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.NetworkedDevice']", 'unique': 'True', 'primary_key': 'True'}),
            'ports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Rack']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'sondas.nagiosnrpecheckopts': {
            'Meta': {'object_name': 'NagiosNrpeCheckOpts', '_ormbases': [u'nagios.NagiosOpts']},
            u'nagiosopts_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['nagios.NagiosOpts']", 'unique': 'True', 'primary_key': 'True'}),
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
            'servidor_nagios': ('django.db.models.fields.CharField', [], {'default': "'193.145.118.253'", 'max_length': '400'}),
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