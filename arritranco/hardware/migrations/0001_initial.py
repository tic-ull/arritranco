# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HwBase'
        db.create_table(u'hardware_hwbase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware_model.HwModel'])),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('warranty_expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('buy_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hardware', ['HwBase'])

        # Adding model 'Rack'
        db.create_table(u'hardware_rack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('units_number', self.gf('django.db.models.fields.IntegerField')()),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Room'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'hardware', ['Rack'])

        # Adding model 'Unrackable'
        db.create_table(u'hardware_unrackable', (
            (u'hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Room'])),
        ))
        db.send_create_signal(u'hardware', ['Unrackable'])

        # Adding model 'NetworkedDevice'
        db.create_table(u'hardware_networkeddevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'hardware', ['NetworkedDevice'])

        # Adding model 'NetworkPort'
        db.create_table(u'hardware_networkport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwBase'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uplink', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hardware', ['NetworkPort'])

        # Adding model 'UserDevice'
        db.create_table(u'hardware_userdevice', (
            (u'networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True)),
            (u'unrackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Unrackable'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wall_socket', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.NetworkPort'])),
            ('place_in_building', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'hardware', ['UserDevice'])

        # Adding model 'Phone'
        db.create_table(u'hardware_phone', (
            (u'userdevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.UserDevice'], unique=True, primary_key=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'hardware', ['Phone'])

        # Adding model 'Server'
        db.create_table(u'hardware_server', (
            (u'hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('management_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('processor_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.ProcessorType'], null=True, blank=True)),
            ('processor_clock', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('processor_number', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'hardware', ['Server'])

        # Adding model 'Chassis'
        db.create_table(u'hardware_chassis', (
            (u'hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Rack'])),
            ('base_unit', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('slots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hardware', ['Chassis'])

        # Adding model 'BladeServer'
        db.create_table(u'hardware_bladeserver', (
            (u'server_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Server'], unique=True, primary_key=True)),
            ('slot_number', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
            ('chassis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Chassis'])),
        ))
        db.send_create_signal(u'hardware', ['BladeServer'])

        # Adding model 'RackServer'
        db.create_table(u'hardware_rackserver', (
            (u'server_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Server'], unique=True, primary_key=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Rack'])),
            ('base_unit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hardware', ['RackServer'])

        # Adding model 'HardDisk'
        db.create_table(u'hardware_harddisk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Server'])),
            ('size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('conn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hardware', ['HardDisk'])

        # Adding model 'ProcessorType'
        db.create_table(u'hardware_processortype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware_model.Manufacturer'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'hardware', ['ProcessorType'])


    def backwards(self, orm):
        # Deleting model 'HwBase'
        db.delete_table(u'hardware_hwbase')

        # Deleting model 'Rack'
        db.delete_table(u'hardware_rack')

        # Deleting model 'Unrackable'
        db.delete_table(u'hardware_unrackable')

        # Deleting model 'NetworkedDevice'
        db.delete_table(u'hardware_networkeddevice')

        # Deleting model 'NetworkPort'
        db.delete_table(u'hardware_networkport')

        # Deleting model 'UserDevice'
        db.delete_table(u'hardware_userdevice')

        # Deleting model 'Phone'
        db.delete_table(u'hardware_phone')

        # Deleting model 'Server'
        db.delete_table(u'hardware_server')

        # Deleting model 'Chassis'
        db.delete_table(u'hardware_chassis')

        # Deleting model 'BladeServer'
        db.delete_table(u'hardware_bladeserver')

        # Deleting model 'RackServer'
        db.delete_table(u'hardware_rackserver')

        # Deleting model 'HardDisk'
        db.delete_table(u'hardware_harddisk')

        # Deleting model 'ProcessorType'
        db.delete_table(u'hardware_processortype')


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
            'main_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'hardware.networkport': {
            'Meta': {'object_name': 'NetworkPort'},
            'hw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.HwBase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uplink': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'hardware.phone': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'Phone', '_ormbases': [u'hardware.UserDevice']},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'userdevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.UserDevice']", 'unique': 'True', 'primary_key': 'True'})
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
        u'hardware.userdevice': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'UserDevice', '_ormbases': [u'hardware.Unrackable', u'hardware.NetworkedDevice']},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'networkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.NetworkedDevice']", 'unique': 'True'}),
            'place_in_building': ('django.db.models.fields.TextField', [], {}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.NetworkPort']"}),
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
        }
    }

    complete_apps = ['hardware']