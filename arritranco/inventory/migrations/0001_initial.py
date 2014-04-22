# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OperatingSystemType'
        db.create_table(u'inventory_operatingsystemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'inventory', ['OperatingSystemType'])

        # Adding model 'OperatingSystem'
        db.create_table(u'inventory_operatingsystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.OperatingSystemType'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['OperatingSystem'])

        # Adding model 'Machine'
        db.create_table(u'inventory_machine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.OperatingSystem'], null=True, blank=True)),
            ('start_up', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('update_priority', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('up_to_date_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('epo_level', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal(u'inventory', ['Machine'])

        # Adding model 'BalancedService'
        db.create_table(u'inventory_balancedservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['BalancedService'])

        # Adding M2M table for field machine on 'BalancedService'
        m2m_table_name = db.shorten_name(u'inventory_balancedservice_machine')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('balancedservice', models.ForeignKey(orm[u'inventory.balancedservice'], null=False)),
            ('machine', models.ForeignKey(orm[u'inventory.machine'], null=False))
        ))
        db.create_unique(m2m_table_name, ['balancedservice_id', 'machine_id'])

        # Adding model 'Interface'
        db.create_table(u'inventory_interface', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Machine'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('hwaddr', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.Network'], null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Interface'])

        # Adding model 'VirtualMachine'
        db.create_table(u'inventory_virtualmachine', (
            (u'machine_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Machine'], unique=True, primary_key=True)),
            ('hypervisor', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('processors', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
            ('total_disks_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['VirtualMachine'])

        # Adding model 'PhysicalMachine'
        db.create_table(u'inventory_physicalmachine', (
            (u'machine_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Machine'], unique=True, primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hardware.Server'])),
            ('ups', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'inventory', ['PhysicalMachine'])


    def backwards(self, orm):
        # Deleting model 'OperatingSystemType'
        db.delete_table(u'inventory_operatingsystemtype')

        # Deleting model 'OperatingSystem'
        db.delete_table(u'inventory_operatingsystem')

        # Deleting model 'Machine'
        db.delete_table(u'inventory_machine')

        # Deleting model 'BalancedService'
        db.delete_table(u'inventory_balancedservice')

        # Removing M2M table for field machine on 'BalancedService'
        db.delete_table(db.shorten_name(u'inventory_balancedservice_machine'))

        # Deleting model 'Interface'
        db.delete_table(u'inventory_interface')

        # Deleting model 'VirtualMachine'
        db.delete_table(u'inventory_virtualmachine')

        # Deleting model 'PhysicalMachine'
        db.delete_table(u'inventory_physicalmachine')


    models = {
        u'hardware.hwbase': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'HwBase'},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.HwModel']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hardware.processortype': {
            'Meta': {'ordering': "['manufacturer', 'model']", 'object_name': 'ProcessorType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.Manufacturer']"}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'inventory.balancedservice': {
            'Meta': {'object_name': 'BalancedService'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'machine': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Machine']", 'symmetrical': 'False'}),
            'up': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'inventory.interface': {
            'Meta': {'object_name': 'Interface'},
            'hwaddr': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
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
        u'inventory.physicalmachine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'PhysicalMachine', '_ormbases': [u'inventory.Machine']},
            u'machine_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['inventory.Machine']", 'unique': 'True', 'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.Server']"}),
            'ups': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'inventory.virtualmachine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'VirtualMachine', '_ormbases': [u'inventory.Machine']},
            'hypervisor': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'machine_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['inventory.Machine']", 'unique': 'True', 'primary_key': 'True'}),
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'}),
            'processors': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_disks_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '3', 'blank': 'True'})
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
        }
    }

    complete_apps = ['inventory']