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
        ))
        db.send_create_signal('hardware', ['HwType'])

        # Adding model 'Manufacturer'
        db.create_table('hardware_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('hardware', ['Manufacturer'])

        # Adding model 'HwModel'
        db.create_table('hardware_hwmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwType'])),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Manufacturer'])),
        ))
        db.send_create_signal('hardware', ['HwModel'])

        # Adding model 'HwBase'
        db.create_table('hardware_hwbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.HwModel'])),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('hardware', ['HwBase'])

        # Adding model 'Rack'
        db.create_table('hardware_rack', (
            ('hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('units_number', self.gf('django.db.models.fields.IntegerField')()),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Place'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('hardware', ['Rack'])

        # Adding model 'RackPlace'
        db.create_table('hardware_rackplace', (
            ('place_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['location.Place'], unique=True, primary_key=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Rack'])),
            ('start_unit', self.gf('django.db.models.fields.IntegerField')()),
            ('end_unit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['RackPlace'])

        # Adding model 'Rackable'
        db.create_table('hardware_rackable', (
            ('hwbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.HwBase'], unique=True, primary_key=True)),
            ('rack_place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.RackPlace'])),
            ('warranty_expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('buy_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('hardware', ['Rackable'])

        # Adding model 'PhysicalServer'
        db.create_table('hardware_physicalserver', (
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('units', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
        ))
        db.send_create_signal('hardware', ['PhysicalServer'])

        # Adding model 'Chasis'
        db.create_table('hardware_chasis', (
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
            ('slots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['Chasis'])

        # Adding model 'BladeServer'
        db.create_table('hardware_bladeserver', (
            ('physicalserver_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.PhysicalServer'], unique=True, primary_key=True)),
            ('slots_number', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
        ))
        db.send_create_signal('hardware', ['BladeServer'])

        # Adding model 'Switch'
        db.create_table('hardware_switch', (
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('ports', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hardware', ['Switch'])


    def backwards(self, orm):
        
        # Deleting model 'HwType'
        db.delete_table('hardware_hwtype')

        # Deleting model 'Manufacturer'
        db.delete_table('hardware_manufacturer')

        # Deleting model 'HwModel'
        db.delete_table('hardware_hwmodel')

        # Deleting model 'HwBase'
        db.delete_table('hardware_hwbase')

        # Deleting model 'Rack'
        db.delete_table('hardware_rack')

        # Deleting model 'RackPlace'
        db.delete_table('hardware_rackplace')

        # Deleting model 'Rackable'
        db.delete_table('hardware_rackable')

        # Deleting model 'PhysicalServer'
        db.delete_table('hardware_physicalserver')

        # Deleting model 'Chasis'
        db.delete_table('hardware_chasis')

        # Deleting model 'BladeServer'
        db.delete_table('hardware_bladeserver')

        # Deleting model 'Switch'
        db.delete_table('hardware_switch')


    models = {
        'hardware.bladeserver': {
            'Meta': {'object_name': 'BladeServer', '_ormbases': ['hardware.PhysicalServer']},
            'physicalserver_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.PhysicalServer']", 'unique': 'True', 'primary_key': 'True'}),
            'slots_number': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        'hardware.chasis': {
            'Meta': {'object_name': 'Chasis', '_ormbases': ['hardware.Rackable']},
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'slots': ('django.db.models.fields.IntegerField', [], {}),
            'units': ('django.db.models.fields.IntegerField', [], {})
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
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.HwType']"})
        },
        'hardware.hwtype': {
            'Meta': {'object_name': 'HwType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hardware.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hardware.physicalserver': {
            'Meta': {'object_name': 'PhysicalServer', '_ormbases': ['hardware.Rackable']},
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'units': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        'hardware.rack': {
            'Meta': {'object_name': 'Rack', '_ormbases': ['hardware.HwBase']},
            'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Place']"}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'hardware.rackable': {
            'Meta': {'object_name': 'Rackable', '_ormbases': ['hardware.HwBase']},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'rack_place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.RackPlace']"}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'hardware.rackplace': {
            'Meta': {'object_name': 'RackPlace', '_ormbases': ['location.Place']},
            'end_unit': ('django.db.models.fields.IntegerField', [], {}),
            'place_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['location.Place']", 'unique': 'True', 'primary_key': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Rack']"}),
            'start_unit': ('django.db.models.fields.IntegerField', [], {})
        },
        'hardware.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': ['hardware.Rackable']},
            'ports': ('django.db.models.fields.IntegerField', [], {}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'location.building': {
            'Meta': {'object_name': 'Building'},
            'area': ('django.db.models.fields.IntegerField', [], {}),
            'campo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_location': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'location.floor': {
            'Meta': {'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'location.place': {
            'Meta': {'object_name': 'Place'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'location.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Floor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['hardware']
