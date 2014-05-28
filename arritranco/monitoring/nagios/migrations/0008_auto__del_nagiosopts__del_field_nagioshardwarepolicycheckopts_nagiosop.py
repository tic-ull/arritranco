# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NagiosOpts'
        #db.delete_table(u'nagios_nagiosopts')

        # Removing M2M table for field contact_groups on 'NagiosOpts'
        #db.delete_table(db.shorten_name(u'nagios_nagiosopts_contact_groups'))

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #               HARDWARE POLICY
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        db.rename_column(u'nagios_nagioshardwarepolicycheckopts', u'nagiosopts_ptr_id', u'id')

        # Adding field 'NagiosHardwarePolicyCheckOpts.check'
        db.add_column(u'nagios_nagioshardwarepolicycheckopts', 'check',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['nagios.NagiosCheck']),
                      keep_default=False)

        # Adding field 'NagiosHardwarePolicyCheckOpts.options'
        db.add_column(u'nagios_nagioshardwarepolicycheckopts', 'options',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field contact_groups on 'NagiosHardwarePolicyCheckOpts'
        m2m_table_name = db.shorten_name(u'nagios_nagioshardwarepolicycheckopts_contact_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagioshardwarepolicycheckopts', models.ForeignKey(orm[u'nagios.nagioshardwarepolicycheckopts'], null=False)),
            ('nagioscontactgroup', models.ForeignKey(orm[u'nagios.nagioscontactgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagioshardwarepolicycheckopts_id', 'nagioscontactgroup_id'])
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #           UNRACKABLE NETWORKED DEVICE
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        db.rename_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', u'nagiosopts_ptr_id', u'id')

        # Adding field 'NagiosUnrackableNetworkedDeviceCheckOpts.check'
        db.add_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', 'check',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['nagios.NagiosCheck']),
                      keep_default=False)

        # Adding field 'NagiosUnrackableNetworkedDeviceCheckOpts.options'
        db.add_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', 'options',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field contact_groups on 'NagiosUnrackableNetworkedDeviceCheckOpts'
        m2m_table_name = db.shorten_name(u'nagios_nagiosunrackablenetworkeddevicecheckopts_contact_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagiosunrackablenetworkeddevicecheckopts', models.ForeignKey(orm[u'nagios.nagiosunrackablenetworkeddevicecheckopts'], null=False)),
            ('nagioscontactgroup', models.ForeignKey(orm[u'nagios.nagioscontactgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagiosunrackablenetworkeddevicecheckopts_id', 'nagioscontactgroup_id'])

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #                   MACHINE
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        db.rename_column(u'nagios_nagiosmachinecheckopts', u'nagiosopts_ptr_id', u'id')
        # Deleting field 'NagiosMachineCheckOpts.nagiosopts_ptr'

        # Adding field 'NagiosMachineCheckOpts.check'
        db.add_column(u'nagios_nagiosmachinecheckopts', 'check',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['nagios.NagiosCheck']),
                      keep_default=False)

        # Adding field 'NagiosMachineCheckOpts.options'
        db.add_column(u'nagios_nagiosmachinecheckopts', 'options',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field contact_groups on 'NagiosMachineCheckOpts'
        m2m_table_name = db.shorten_name(u'nagios_nagiosmachinecheckopts_contact_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagiosmachinecheckopts', models.ForeignKey(orm[u'nagios.nagiosmachinecheckopts'], null=False)),
            ('nagioscontactgroup', models.ForeignKey(orm[u'nagios.nagioscontactgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagiosmachinecheckopts_id', 'nagioscontactgroup_id'])

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #                   SERVICE
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        db.rename_column(u'nagios_nagiosservicecheckopts', u'nagiosopts_ptr_id', u'id')

        # Adding field 'NagiosServiceCheckOpts.check'
        db.add_column(u'nagios_nagiosservicecheckopts', 'check',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['nagios.NagiosCheck']),
                      keep_default=False)

        # Adding field 'NagiosServiceCheckOpts.options'
        db.add_column(u'nagios_nagiosservicecheckopts', 'options',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field contact_groups on 'NagiosServiceCheckOpts'
        m2m_table_name = db.shorten_name(u'nagios_nagiosservicecheckopts_contact_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagiosservicecheckopts', models.ForeignKey(orm[u'nagios.nagiosservicecheckopts'], null=False)),
            ('nagioscontactgroup', models.ForeignKey(orm[u'nagios.nagioscontactgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagiosservicecheckopts_id', 'nagioscontactgroup_id'])


    def backwards(self, orm):
        # Adding model 'NagiosOpts'
        db.create_table(u'nagios_nagiosopts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('options', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nagios.NagiosCheck'])),
        ))
        db.send_create_signal(u'nagios', ['NagiosOpts'])

        # Adding M2M table for field contact_groups on 'NagiosOpts'
        m2m_table_name = db.shorten_name(u'nagios_nagiosopts_contact_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nagiosopts', models.ForeignKey(orm[u'nagios.nagiosopts'], null=False)),
            ('nagioscontactgroup', models.ForeignKey(orm[u'nagios.nagioscontactgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nagiosopts_id', 'nagioscontactgroup_id'])


        # User chose to not deal with backwards NULL issues for 'NagiosHardwarePolicyCheckOpts.nagiosopts_ptr'
        raise RuntimeError("Cannot reverse this migration. 'NagiosHardwarePolicyCheckOpts.nagiosopts_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NagiosHardwarePolicyCheckOpts.nagiosopts_ptr'
        db.add_column(u'nagios_nagioshardwarepolicycheckopts', u'nagiosopts_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nagios.NagiosOpts'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'NagiosHardwarePolicyCheckOpts.id'
        db.delete_column(u'nagios_nagioshardwarepolicycheckopts', u'id')

        # Deleting field 'NagiosHardwarePolicyCheckOpts.check'
        db.delete_column(u'nagios_nagioshardwarepolicycheckopts', 'check_id')

        # Deleting field 'NagiosHardwarePolicyCheckOpts.options'
        db.delete_column(u'nagios_nagioshardwarepolicycheckopts', 'options')

        # Removing M2M table for field contact_groups on 'NagiosHardwarePolicyCheckOpts'
        db.delete_table(db.shorten_name(u'nagios_nagioshardwarepolicycheckopts_contact_groups'))


        # User chose to not deal with backwards NULL issues for 'NagiosUnrackableNetworkedDeviceCheckOpts.nagiosopts_ptr'
        raise RuntimeError("Cannot reverse this migration. 'NagiosUnrackableNetworkedDeviceCheckOpts.nagiosopts_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NagiosUnrackableNetworkedDeviceCheckOpts.nagiosopts_ptr'
        db.add_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', u'nagiosopts_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nagios.NagiosOpts'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'NagiosUnrackableNetworkedDeviceCheckOpts.id'
        db.delete_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', u'id')

        # Deleting field 'NagiosUnrackableNetworkedDeviceCheckOpts.check'
        db.delete_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', 'check_id')

        # Deleting field 'NagiosUnrackableNetworkedDeviceCheckOpts.options'
        db.delete_column(u'nagios_nagiosunrackablenetworkeddevicecheckopts', 'options')

        # Removing M2M table for field contact_groups on 'NagiosUnrackableNetworkedDeviceCheckOpts'
        db.delete_table(db.shorten_name(u'nagios_nagiosunrackablenetworkeddevicecheckopts_contact_groups'))


        # User chose to not deal with backwards NULL issues for 'NagiosMachineCheckOpts.nagiosopts_ptr'
        raise RuntimeError("Cannot reverse this migration. 'NagiosMachineCheckOpts.nagiosopts_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NagiosMachineCheckOpts.nagiosopts_ptr'
        db.add_column(u'nagios_nagiosmachinecheckopts', u'nagiosopts_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nagios.NagiosOpts'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'NagiosMachineCheckOpts.id'
        db.delete_column(u'nagios_nagiosmachinecheckopts', u'id')

        # Deleting field 'NagiosMachineCheckOpts.check'
        db.delete_column(u'nagios_nagiosmachinecheckopts', 'check_id')

        # Deleting field 'NagiosMachineCheckOpts.options'
        db.delete_column(u'nagios_nagiosmachinecheckopts', 'options')

        # Removing M2M table for field contact_groups on 'NagiosMachineCheckOpts'
        db.delete_table(db.shorten_name(u'nagios_nagiosmachinecheckopts_contact_groups'))


        # User chose to not deal with backwards NULL issues for 'NagiosServiceCheckOpts.nagiosopts_ptr'
        raise RuntimeError("Cannot reverse this migration. 'NagiosServiceCheckOpts.nagiosopts_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NagiosServiceCheckOpts.nagiosopts_ptr'
        db.add_column(u'nagios_nagiosservicecheckopts', u'nagiosopts_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nagios.NagiosOpts'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'NagiosServiceCheckOpts.id'
        db.delete_column(u'nagios_nagiosservicecheckopts', u'id')

        # Deleting field 'NagiosServiceCheckOpts.check'
        db.delete_column(u'nagios_nagiosservicecheckopts', 'check_id')

        # Deleting field 'NagiosServiceCheckOpts.options'
        db.delete_column(u'nagios_nagiosservicecheckopts', 'options')

        # Removing M2M table for field contact_groups on 'NagiosServiceCheckOpts'
        db.delete_table(db.shorten_name(u'nagios_nagiosservicecheckopts_contact_groups'))


    models = {
        u'hardware.hwbase': {
            'Meta': {'ordering': "['model', 'serial_number']", 'object_name': 'HwBase'},
            'buy_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware_model.HwModel']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'warranty_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hardware.rack': {
            'Meta': {'object_name': 'Rack'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'units_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hardware.unrackablenetworkeddevice': {
            'Meta': {'object_name': 'UnrackableNetworkedDevice'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            u'hwbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hardware.HwBase']", 'unique': 'True', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'main_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_in_building': ('django.db.models.fields.TextField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Room']"}),
            'switch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.Switch']"}),
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
        u'inventory.machine': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Machine'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'epo_level': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'monitoring.responsible': {
            'Meta': {'object_name': 'Responsible'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'nagios.nagioscheck': {
            'Meta': {'ordering': "['name']", 'object_name': 'NagiosCheck'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'default_params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.Machine']", 'null': 'True', 'through': u"orm['nagios.NagiosMachineCheckOpts']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nrpe': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nrpeservice'", 'to': u"orm['nagios.Service']", 'through': u"orm['sondas.NagiosNrpeCheckOpts']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'os': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.OperatingSystemType']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['nagios.Service']", 'null': 'True', 'through': u"orm['nagios.NagiosServiceCheckOpts']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unrackable_networked_devices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hardware.UnrackableNetworkedDevice']", 'null': 'True', 'through': u"orm['nagios.NagiosUnrackableNetworkedDeviceCheckOpts']", 'blank': 'True'})
        },
        u'nagios.nagioscontactgroup': {
            'Meta': {'object_name': 'NagiosContactGroup', '_ormbases': [u'monitoring.Responsible']},
            'ngcontact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'responsible_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monitoring.Responsible']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'nagios.nagioshardwarepolicycheckopts': {
            'Meta': {'object_name': 'NagiosHardwarePolicyCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            'excluded_os': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.OperatingSystem']", 'null': 'True', 'blank': 'True'}),
            'hwmodel': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hardware_model.HwModel']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'nagios.nagiosmachinecheckdefaults': {
            'Meta': {'object_name': 'NagiosMachineCheckDefaults'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nagioscheck': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"})
        },
        u'nagios.nagiosmachinecheckopts': {
            'Meta': {'object_name': 'NagiosMachineCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Machine']"}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'nagios.nagiosnetworkparent': {
            'Meta': {'object_name': 'NagiosNetworkParent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.Network']"}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'nagios.nagiosservicecheckopts': {
            'Meta': {'object_name': 'NagiosServiceCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.Service']"})
        },
        u'nagios.nagiosunrackablenetworkeddevicecheckopts': {
            'Meta': {'object_name': 'NagiosUnrackableNetworkedDeviceCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'unrackable_networked_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']"})
        },
        u'nagios.service': {
            'Meta': {'object_name': 'Service'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['network.IP']"}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inventory.Machine']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        },
        u'sondas.nagiosnrpecheckopts': {
            'Meta': {'object_name': 'NagiosNrpeCheckOpts'},
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.NagiosCheck']"}),
            'contact_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nagios.NagiosContactGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nagios.Service']"}),
            'sonda': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sondas.Sonda']", 'symmetrical': 'False'})
        },
        u'sondas.sonda': {
            'Meta': {'object_name': 'Sonda'},
            'dir_checks': ('django.db.models.fields.CharField', [], {'default': "'/usr/lib/nagios/plugins'", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'nrpe_service_name': ('django.db.models.fields.CharField', [], {'default': "'nagios-nrpe-server'", 'max_length': '400'}),
            'script_end': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'script_inicio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servidor_nagios': ('django.db.models.fields.CharField', [], {'default': "'193.145.118.253'", 'max_length': '400'}),
            'ssh': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unrackable_networked_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hardware.UnrackableNetworkedDevice']"})
        }
    }

    complete_apps = ['nagios']