# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ManagementInfo'
        db.create_table('network_managementinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('defaultports', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('backupmethod', self.gf('django.db.models.fields.IntegerField')()),
            ('backupusername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backuppassword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backupconfigfile', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('recommended_version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('configtemplate', self.gf('django.db.models.fields.TextField')()),
            ('oid', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('network', ['ManagementInfo'])

        # Adding model 'Switch'
        db.create_table('network_switch', (
            ('networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True)),
            ('rackable_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.Rackable'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('ports', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('managementinfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.ManagementInfo'])),
        ))
        db.send_create_signal('network', ['Switch'])

        # Adding model 'MACsHistory'
        db.create_table('network_macshistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('captured', self.gf('django.db.models.fields.DateTimeField')()),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('network', ['MACsHistory'])

        # Adding M2M table for field port on 'MACsHistory'
        db.create_table('network_macshistory_port', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('macshistory', models.ForeignKey(orm['network.macshistory'], null=False)),
            ('networkport', models.ForeignKey(orm['hardware.networkport'], null=False))
        ))
        db.create_unique('network_macshistory_port', ['macshistory_id', 'networkport_id'])

        # Adding model 'RoutingZone'
        db.create_table('network_routingzone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bluevlan_prefix', self.gf('django.db.models.fields.IntegerField')()),
            ('public_nets', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cajacanarias_nets', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('network', ['RoutingZone'])

        # Adding model 'NetworkedBuilding'
        db.create_table('network_networkedbuilding', (
            ('building_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['location.Building'], unique=True, primary_key=True)),
            ('routingzone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.RoutingZone'])),
        ))
        db.send_create_signal('network', ['NetworkedBuilding'])


    def backwards(self, orm):
        
        # Deleting model 'ManagementInfo'
        db.delete_table('network_managementinfo')

        # Deleting model 'Switch'
        db.delete_table('network_switch')

        # Deleting model 'MACsHistory'
        db.delete_table('network_macshistory')

        # Removing M2M table for field port on 'MACsHistory'
        db.delete_table('network_macshistory_port')

        # Deleting model 'RoutingZone'
        db.delete_table('network_routingzone')

        # Deleting model 'NetworkedBuilding'
        db.delete_table('network_networkedbuilding')


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
        'hardware.rackplace': {
            'Meta': {'object_name': 'RackPlace'},
            'base_unit': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hardware.Rack']"})
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
        },
        'network.macshistory': {
            'Meta': {'object_name': 'MACsHistory'},
            'captured': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'port': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hardware.NetworkPort']", 'symmetrical': 'False'})
        },
        'network.managementinfo': {
            'Meta': {'object_name': 'ManagementInfo'},
            'backupconfigfile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'backupmethod': ('django.db.models.fields.IntegerField', [], {}),
            'backuppassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'backupusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'configtemplate': ('django.db.models.fields.TextField', [], {}),
            'defaultports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'oid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recommended_version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'network.networkedbuilding': {
            'Meta': {'object_name': 'NetworkedBuilding', '_ormbases': ['location.Building']},
            'building_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['location.Building']", 'unique': 'True', 'primary_key': 'True'}),
            'routingzone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['network.RoutingZone']"})
        },
        'network.routingzone': {
            'Meta': {'object_name': 'RoutingZone'},
            'bluevlan_prefix': ('django.db.models.fields.IntegerField', [], {}),
            'cajacanarias_nets': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'public_nets': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'network.switch': {
            'Meta': {'object_name': 'Switch', '_ormbases': ['hardware.Rackable', 'hardware.NetworkedDevice']},
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'managementinfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['network.ManagementInfo']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'networkeddevice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.NetworkedDevice']", 'unique': 'True'}),
            'ports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rackable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hardware.Rackable']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['network']
