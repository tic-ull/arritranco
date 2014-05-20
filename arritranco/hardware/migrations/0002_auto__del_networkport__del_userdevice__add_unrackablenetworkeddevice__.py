# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NetworkPort'
        db.delete_table(u'hardware_networkport')

        # Deleting model 'UserDevice'
        db.delete_table(u'hardware_userdevice')

        # Adding model 'UnrackableNetworkedDevice'
        db.create_table(u'hardware_unrackablenetworkeddevice', (
            (u'networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True)),
            (u'unrackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Unrackable'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wall_socket', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('switch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.Switch'])),
            ('place_in_building', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hardware', ['UnrackableNetworkedDevice'])

        # Deleting field 'Phone.userdevice_ptr'
        db.delete_column(u'hardware_phone', u'userdevice_ptr_id')

        # Adding field 'Phone.unrackablenetworkeddevice_ptr'
        db.add_column(u'hardware_phone', u'unrackablenetworkeddevice_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.UnrackableNetworkedDevice'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'Server.management_ip_new'
        db.add_column(u'hardware_server', 'management_ip_new',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.IP'], null=True, blank=True),
                      keep_default=False)


        # Renaming column for 'NetworkedDevice.main_ip' to match new field type.
        db.rename_column(u'hardware_networkeddevice', 'main_ip', 'main_ip_id')
        # Changing field 'NetworkedDevice.main_ip'
        db.alter_column(u'hardware_networkeddevice', 'main_ip_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.IP']))
        # Adding index on 'NetworkedDevice', fields ['main_ip']
        db.create_index(u'hardware_networkeddevice', ['main_ip_id'])


    def backwards(self, orm):
        # Removing index on 'NetworkedDevice', fields ['main_ip']
        db.delete_index(u'hardware_networkeddevice', ['main_ip_id'])

        # Adding model 'NetworkPort'
        db.create_table(u'hardware_networkport', (
            ('uplink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwBase'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'hardware', ['NetworkPort'])

        # Adding model 'UserDevice'
        db.create_table(u'hardware_userdevice', (
            ('port', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.NetworkPort'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'unrackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Unrackable'], unique=True, primary_key=True)),
            ('wall_socket', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('place_in_building', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'hardware', ['UserDevice'])

        # Deleting model 'UnrackableNetworkedDevice'
        db.delete_table(u'hardware_unrackablenetworkeddevice')

        # Adding field 'Phone.userdevice_ptr'
        db.add_column(u'hardware_phone', u'userdevice_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['hardware.UserDevice'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Phone.unrackablenetworkeddevice_ptr'
        db.delete_column(u'hardware_phone', u'unrackablenetworkeddevice_ptr_id')

        # Deleting field 'Server.management_ip_new'
        db.delete_column(u'hardware_server', 'management_ip_new_id')


        # Renaming column for 'NetworkedDevice.main_ip' to match new field type.
        db.rename_column(u'hardware_networkeddevice', 'main_ip_id', 'main_ip')
        # Changing field 'NetworkedDevice.main_ip'
        db.alter_column(u'hardware_networkeddevice', 'main_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15))

    models = {
        u'hardware.bladeserver': {
            'Meta': {'ordering': "['slot_number']", 'object_name': 'BladeServer', '_ormbases': [u'hardware.Server']},
            'chassis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Chassis']"}),
            u'server_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.Server']", 'unique': 'True', 'primary_key': 'True'}),
            'slot_number': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        u'hardware.chassis': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'Chassis', '_ormbases': [u'hardware.HwBase']},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            u'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Rack']"}),
            'slots': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'hardware.harddisk': {
            'Meta': {'object_name': 'HardDisk'},
            'conn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Server']"}),
            'size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'})
        },
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
        u'hardware.phone': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'Phone', '_ormbases': [u'hardware.UnrackableNetworkedDevice']},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'unrackablenetworkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'hardware.processortype': {
            'Meta': {'ordering': "['manufacturer', 'model']", 'object_name': 'ProcessorType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.Manufacturer']"}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hardware.rackserver': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'RackServer', '_ormbases': [u'hardware.Server']},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Rack']"}),
            u'server_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.Server']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'hardware.server': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'Server', '_ormbases': [u'hardware.HwBase']},
            u'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'management_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'management_ip_new': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']", 'null': 'True', 'blank': 'True'}),
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_clock': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'processor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.ProcessorType']", 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['hardware']