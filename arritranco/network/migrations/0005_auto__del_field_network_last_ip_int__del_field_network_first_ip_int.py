# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Network.last_ip_int'
        db.delete_column(u'network_network', 'last_ip_int')

        # Deleting field 'Network.first_ip_int'
        db.delete_column(u'network_network', 'first_ip_int')


    def backwards(self, orm):
        # Adding field 'Network.last_ip_int'
        db.add_column(u'network_network', 'last_ip_int',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Network.first_ip_int'
        db.add_column(u'network_network', 'first_ip_int',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'last_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
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
        }
    }

    complete_apps = ['network']