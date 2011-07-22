# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OperatingSystemType'
        db.create_table('inventory_operatingsystemtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('inventory', ['OperatingSystemType'])

        # Adding model 'OperatingSystem'
        db.create_table('inventory_operatingsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.OperatingSystemType'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['OperatingSystem'])

        # Adding model 'Machine'
        db.create_table('inventory_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('up', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.OperatingSystem'], null=True, blank=True)),
            ('start_up', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('update_priority', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('epo_level', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('inventory', ['Machine'])

        # Adding model 'VirtualMachine'
        db.create_table('inventory_virtualmachine', (
            ('machine_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Machine'], unique=True, primary_key=True)),
            ('processors', self.gf('django.db.models.fields.IntegerField')()),
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('total_disks_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('inventory', ['VirtualMachine'])

        # Adding model 'PhysicalMachine'
        db.create_table('inventory_physicalmachine', (
            ('machine_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Machine'], unique=True, primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Server'], null=True, blank=True)),
            ('ups', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('inventory', ['PhysicalMachine'])


    def backwards(self, orm):
        
        # Deleting model 'OperatingSystemType'
        db.delete_table('inventory_operatingsystemtype')

        # Deleting model 'OperatingSystem'
        db.delete_table('inventory_operatingsystem')

        # Deleting model 'Machine'
        db.delete_table('inventory_machine')

        # Deleting model 'VirtualMachine'
        db.delete_table('inventory_virtualmachine')

        # Deleting model 'PhysicalMachine'
        db.delete_table('inventory_physicalmachine')


    models = {
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
            'Meta': {'object_name': 'HwType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.processortype': {
            'Meta': {'object_name': 'ProcessorType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Manufacturer']"}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hardware.rack': {
            'Meta': {'object_name': 'Rack', '_ormbases': ['hardware.HwBase']},
            'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Place']"}),
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
        'hardware.rackplace': {
            'Meta': {'object_name': 'RackPlace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Rack']"}),
            'units': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        'hardware.server': {
            'Meta': {'object_name': 'Server', '_ormbases': ['hardware.Rackable']},
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_clock': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processor_number': ('django.db.models.fields.IntegerField', [], {}),
            'processor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.ProcessorType']", 'null': 'True', 'blank': 'True'}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'inventory.machine': {
            'Meta': {'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.OperatingSystem']", 'null': 'True', 'blank': 'True'}),
            'start_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
        'inventory.physicalmachine': {
            'Meta': {'object_name': 'PhysicalMachine', '_ormbases': ['inventory.Machine']},
            'machine_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inventory.Machine']", 'unique': 'True', 'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Server']", 'null': 'True', 'blank': 'True'}),
            'ups': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'inventory.virtualmachine': {
            'Meta': {'object_name': 'VirtualMachine', '_ormbases': ['inventory.Machine']},
            'machine_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inventory.Machine']", 'unique': 'True', 'primary_key': 'True'}),
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processors': ('django.db.models.fields.IntegerField', [], {}),
            'total_disks_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'})
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

    complete_apps = ['inventory']
