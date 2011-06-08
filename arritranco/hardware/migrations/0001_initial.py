# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HwType'
        db.create_table('hardware_hwtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('hardware', ['HwType'])

        # Adding model 'Manufacturer'
        db.create_table('hardware_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('hardware', ['Manufacturer'])

        # Adding model 'HwModel'
        db.create_table('hardware_hwmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwType'])),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Manufacturer'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('hardware', ['HwModel'])

        # Adding model 'RackableModel'
        db.create_table('hardware_rackablemodel', (
            ('hwmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwModel'], unique=True, primary_key=True)),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['RackableModel'])

        # Adding model 'HwBase'
        db.create_table('hardware_hwbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwModel'])),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('hardware', ['HwBase'])

        # Adding model 'Rack'
        db.create_table('hardware_rack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('units_number', self.gf('django.db.models.fields.IntegerField')()),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Room'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('hardware', ['Rack'])

        # Adding model 'RackPlace'
        db.create_table('hardware_rackplace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Rack'])),
            ('base_unit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['RackPlace'])

        # Adding model 'Rackable'
        db.create_table('hardware_rackable', (
            ('rackplace_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.RackPlace'], unique=True)),
            ('hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('warranty_expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('buy_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('hardware', ['Rackable'])

        # Adding model 'Unrackable'
        db.create_table('hardware_unrackable', (
            ('hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Building'])),
        ))
        db.send_create_signal('hardware', ['Unrackable'])

        # Adding model 'NetworkedDevice'
        db.create_table('hardware_networkeddevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('hardware', ['NetworkedDevice'])

        # Adding model 'NetworkPort'
        db.create_table('hardware_networkport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwBase'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uplink', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hardware', ['NetworkPort'])

        # Adding model 'UserDevice'
        db.create_table('hardware_userdevice', (
            ('networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True)),
            ('unrackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Unrackable'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wall_socket', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.NetworkPort'])),
            ('place_in_building', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('hardware', ['UserDevice'])

        # Adding model 'Phone'
        db.create_table('hardware_phone', (
            ('userdevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.UserDevice'], unique=True, primary_key=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('hardware', ['Phone'])

        # Adding model 'Server'
        db.create_table('hardware_server', (
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('processor_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.ProcessorType'], null=True, blank=True)),
            ('processor_clock', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('processor_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['Server'])

        # Adding model 'Chasis'
        db.create_table('hardware_chasis', (
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
            ('slots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['Chasis'])

        # Adding model 'BladeServer'
        db.create_table('hardware_bladeserver', (
            ('server_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Server'], unique=True, primary_key=True)),
            ('slots_number', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
            ('chasis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Chasis'])),
        ))
        db.send_create_signal('hardware', ['BladeServer'])

        # Adding model 'HardDisk'
        db.create_table('hardware_harddisk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Server'])),
            ('size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('conn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('hardware', ['HardDisk'])

        # Adding model 'ProcessorType'
        db.create_table('hardware_processortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Manufacturer'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('hardware', ['ProcessorType'])


    def backwards(self, orm):
        
        # Deleting model 'HwType'
        db.delete_table('hardware_hwtype')

        # Deleting model 'Manufacturer'
        db.delete_table('hardware_manufacturer')

        # Deleting model 'HwModel'
        db.delete_table('hardware_hwmodel')

        # Deleting model 'RackableModel'
        db.delete_table('hardware_rackablemodel')

        # Deleting model 'HwBase'
        db.delete_table('hardware_hwbase')

        # Deleting model 'Rack'
        db.delete_table('hardware_rack')

        # Deleting model 'RackPlace'
        db.delete_table('hardware_rackplace')

        # Deleting model 'Rackable'
        db.delete_table('hardware_rackable')

        # Deleting model 'Unrackable'
        db.delete_table('hardware_unrackable')

        # Deleting model 'NetworkedDevice'
        db.delete_table('hardware_networkeddevice')

        # Deleting model 'NetworkPort'
        db.delete_table('hardware_networkport')

        # Deleting model 'UserDevice'
        db.delete_table('hardware_userdevice')

        # Deleting model 'Phone'
        db.delete_table('hardware_phone')

        # Deleting model 'Server'
        db.delete_table('hardware_server')

        # Deleting model 'Chasis'
        db.delete_table('hardware_chasis')

        # Deleting model 'BladeServer'
        db.delete_table('hardware_bladeserver')

        # Deleting model 'HardDisk'
        db.delete_table('hardware_harddisk')

        # Deleting model 'ProcessorType'
        db.delete_table('hardware_processortype')


    models = {
        'hardware.bladeserver': {
            'Meta': {'object_name': 'BladeServer', '_ormbases': ['hardware.Server']},
            'chasis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Chasis']"}),
            'server_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Server']", 'unique': 'True', 'primary_key': 'True'}),
            'slots_number': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        'hardware.chasis': {
            'Meta': {'object_name': 'Chasis', '_ormbases': ['hardware.Rackable']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'slots': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        },
        'hardware.harddisk': {
            'Meta': {'object_name': 'HardDisk'},
            'conn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Server']"}),
            'size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'})
        },
        'hardware.hwbase': {
            'Meta': {'object_name': 'HwBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.HwModel']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hardware.hwmodel': {
            'Meta': {'object_name': 'HwModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.HwType']"})
        },
        'hardware.hwtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'HwType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.manufacturer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.networkeddevice': {
            'Meta': {'object_name': 'NetworkedDevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        'hardware.networkport': {
            'Meta': {'object_name': 'NetworkPort'},
            'hw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.HwBase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uplink': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hardware.phone': {
            'Meta': {'object_name': 'Phone', '_ormbases': ['hardware.UserDevice']},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'userdevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.UserDevice']", 'unique': 'True', 'primary_key': 'True'})
        },
        'hardware.processortype': {
            'Meta': {'ordering': "['manufacturer', 'model']", 'object_name': 'ProcessorType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Manufacturer']"}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'hardware.rackable': {
            'Meta': {'object_name': 'Rackable', '_ormbases': ['hardware.HwBase', 'hardware.RackPlace']},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'rackplace_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.RackPlace']", 'unique': 'True'}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'hardware.rackablemodel': {
            'Meta': {'object_name': 'RackableModel', '_ormbases': ['hardware.HwModel']},
            'hwmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwModel']", 'unique': 'True', 'primary_key': 'True'}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        },
        'hardware.rackplace': {
            'Meta': {'object_name': 'RackPlace'},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Rack']"})
        },
        'hardware.server': {
            'Meta': {'object_name': 'Server', '_ormbases': ['hardware.Rackable']},
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_clock': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_number': ('django.db.models.fields.IntegerField', [], {}),
            'processor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.ProcessorType']", 'null': 'True', 'blank': 'True'}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'hardware.unrackable': {
            'Meta': {'object_name': 'Unrackable', '_ormbases': ['hardware.HwBase']},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Building']"}),
            'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'hardware.userdevice': {
            'Meta': {'object_name': 'UserDevice', '_ormbases': ['hardware.Unrackable', 'hardware.NetworkedDevice']},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'networkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.NetworkedDevice']", 'unique': 'True'}),
            'place_in_building': ('django.db.models.fields.TextField', [], {}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.NetworkPort']"}),
            'unrackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Unrackable']", 'unique': 'True', 'primary_key': 'True'}),
            'wall_socket': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'location.building': {
            'Meta': {'object_name': 'Building'},
            'area': ('django.db.models.fields.IntegerField', [], {}),
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Campus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_location': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'location.campus': {
            'Meta': {'object_name': 'Campus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'location.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Building']"}),
            'floor': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['hardware']
