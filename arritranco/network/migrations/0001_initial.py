# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Network'
        db.create_table(u'network_network', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('first_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('last_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('first_ip_int', self.gf('django.db.models.fields.IntegerField')()),
            ('last_ip_int', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'network', ['Network'])

        # Adding model 'ManagementInfo'
        db.create_table(u'network_managementinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'network', ['ManagementInfo'])

        # Adding model 'Switch'
        db.create_table(u'network_switch', (
            (u'networkeddevice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hardware.NetworkedDevice'], unique=True, primary_key=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Rack'])),
            ('base_unit', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('ports', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('managementinfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.ManagementInfo'])),
        ))
        db.send_create_signal(u'network', ['Switch'])

        # Adding model 'MACsHistory'
        db.create_table(u'network_macshistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('captured', self.gf('django.db.models.fields.DateTimeField')()),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal(u'network', ['MACsHistory'])

        # Adding M2M table for field port on 'MACsHistory'
        m2m_table_name = db.shorten_name(u'network_macshistory_port')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('macshistory', models.ForeignKey(orm[u'network.macshistory'], null=False)),
            ('networkport', models.ForeignKey(orm[u'hardware.networkport'], null=False))
        ))
        db.create_unique(m2m_table_name, ['macshistory_id', 'networkport_id'])

        # Adding model 'RoutingZone'
        db.create_table(u'network_routingzone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bluevlan_prefix', self.gf('django.db.models.fields.IntegerField')()),
            ('public_nets', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cajacanarias_nets', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'network', ['RoutingZone'])

        # Adding model 'NetworkedBuilding'
        db.create_table(u'network_networkedbuilding', (
            (u'building_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['location.Building'], unique=True, primary_key=True)),
            ('routingzone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.RoutingZone'])),
        ))
        db.send_create_signal(u'network', ['NetworkedBuilding'])


    def backwards(self, orm):
        # Deleting model 'Network'
        db.delete_table(u'network_network')

        # Deleting model 'ManagementInfo'
        db.delete_table(u'network_managementinfo')

        # Deleting model 'Switch'
        db.delete_table(u'network_switch')

        # Deleting model 'MACsHistory'
        db.delete_table(u'network_macshistory')

        # Removing M2M table for field port on 'MACsHistory'
        db.delete_table(db.shorten_name(u'network_macshistory_port'))

        # Deleting model 'RoutingZone'
        db.delete_table(u'network_routingzone')

        # Deleting model 'NetworkedBuilding'
        db.delete_table(u'network_networkedbuilding')


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
            'main_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'hardware.networkport': {
            'Meta': {'object_name': 'NetworkPort'},
            'hw': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.HwBase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uplink': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
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
        u'network.macshistory': {
            'Meta': {'object_name': 'MACsHistory'},
            'captured': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'port': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hardware.NetworkPort']", 'symmetrical': 'False'})
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
        u'network.networkedbuilding': {
            'Meta': {'object_name': 'NetworkedBuilding', '_ormbases': [u'location.Building']},
            u'building_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['location.Building']", 'unique': 'True', 'primary_key': 'True'}),
            'routingzone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.RoutingZone']"})
        },
        u'network.routingzone': {
            'Meta': {'object_name': 'RoutingZone'},
            'bluevlan_prefix': ('django.db.models.fields.IntegerField', [], {}),
            'cajacanarias_nets': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'public_nets': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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

    complete_apps = ['network']