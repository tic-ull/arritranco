# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MACsHistory.port'
        db.add_column('hardware_macshistory', 'port', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['hardware.NetworkPort']), keep_default=False)

        # Removing M2M table for field port on 'MACsHistory'
        db.delete_table('hardware_macshistory_port')


    def backwards(self, orm):
        
        # Deleting field 'MACsHistory.port'
        db.delete_column('hardware_macshistory', 'port_id')

        # Adding M2M table for field port on 'MACsHistory'
        db.create_table('hardware_macshistory_port', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('macshistory', models.ForeignKey(orm['hardware.macshistory'], null=False)),
            ('networkport', models.ForeignKey(orm['hardware.networkport'], null=False))
        ))
        db.create_unique('hardware_macshistory_port', ['macshistory_id', 'networkport_id'])


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
            'Meta': {'object_name': 'HwType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.macshistory': {
            'Meta': {'object_name': 'MACsHistory'},
            'captured': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.NetworkPort']"})
        },
        'hardware.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'hardware.networkbasemodel': {
            'Meta': {'object_name': 'NetworkBaseModel', '_ormbases': ['hardware.RackableModel']},
            'oid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rackablemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.RackableModel']", 'unique': 'True', 'primary_key': 'True'}),
            'recommended_version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.TextField', [], {})
        },
        'hardware.networkport': {
            'Meta': {'object_name': 'NetworkPort'},
            'hw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.HwBase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uplink': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
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
        'hardware.rackablemodel': {
            'Meta': {'object_name': 'RackableModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'hardware.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': ['hardware.Rackable']},
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.NetworkBaseModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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

    complete_apps = ['hardware']
