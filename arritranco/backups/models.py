from django.db import models
from django.utils.translation import ugettext_lazy as _
from scheduler.models import Task
from inventory.models import Machine
import datetime

#class RevisionBackup(models.Model):
# This file
#    maquina = models.ForeignKey(Maquina)
#    # core = True
#    fecha = models.DateField(blank=True, null=True, help_text='Fecha creaci0n')
#
#    def __unicode__(self):
#        return "%s %s" % (self.maquina, self.fecha.strftime('%d-%m-%Y'))
#
#    class Meta:
#        ordering = ['-fecha',]
#        verbose_name_plural = 'Revisiones de backup'
#        verbose_name = 'Revision de backup'

class FileBackupTask(Task):
    """
        File backup task
    """
    FILE_BACKUP = 1
    DATABASE_BACKUP = 2
    SYSTEM_BACKUP = 3

    BACKUP_TYPE_CHOICES = (
        (FILE_BACKUP, _(u'File')),
        (DATABASE_BACKUP, _(u'Database')),
        (SYSTEM_BACKUP, _(u'System')),
    )

    machine = models.ForeignKey(Machine)
    duration = models.TimeField(_(u"Duration"), blank=True, null=True)

    bckp_type = models.IntegerField(blank=True, null=True, choices=BACKUP_TYPE_CHOICES, default = SYSTEM_BACKUP)

    checker_fqdn = models.CharField(max_length=255, verbose_name=_(u"Checker fqdn"),
        help_text=_(u"Machine fqdn where this backups shoud be checked."))
    directory = models.CharField(max_length=255,
        help_text=_(u'Directory where files shoud be.'))
    days_in_hard_drive = models.IntegerField(blank=False, null=False, default=90,
        help_text=_(u'Number of days that this backup shoud be on disk at most.'))
    max_backup_month = models.IntegerField(blank=False, null=False, default=60,
        help_text=_(u'Number of backups that shoud to be on disk after a month.'))

    def __unicode__(self):
        return _(u"%s @ %s/%s") % (self.machine.fqdn, self.get_bckp_type_display(), self.cron_syntax())

    def fecha_fin(self, day):
        """
            Devuelve el dia y la hora en el que terminara la planificacion.
        """
        if self.duracion:
            duracion = self.duracion
        else:
            duracion = datetime.time(hour = 0, minute = 30)
        return datetime.datetime.combine(day, self.time) + datetime.timedelta(
                    hours = duracion.hour,
                    minutes = duracion.minute,
                    seconds = duracion.second
            )

class FileNamePattern(models.Model):
    """
        File name patterns.
    """
    pattern = models.CharField('Nombre del archivo', max_length=255, blank=True, null=True,
        help_text=_(u'File name pattern, you can use regexp and date patterns here.'))

    def get_re (self):
        # FIXME: Change month list based on default locale language
        sustituciones = (
                ('%Y', '(?P<year4>\d{4})'),
                ('%y', '(?P<year2>\d{2})'),
                ('%m', '(?P<month>\d{2})'),
                ('%d', '(?P<day>\d{2})'),
                ('%B', '(?P<month_large>' + _(u'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre))')),
                ('#', '(?P<chunk>\d+)'),
            )
        patron_re = self.pattern
        #patron_re = patron_re.replace('__FQDN__', self.planificacion.maquina)
        for o, d in sustituciones:
            patron_re = patron_re.replace (o, d)
        return re.compile (patron_re)

    def __unicode__(self):
        return u"%s" % self.pattern

    class Meta:
        ordering = ['pattern',]
        verbose_name_plural = _(u'File name patterns')
        verbose_name = _(u'File name pattern')

#    def __unicode__(self):
#        m = unicode(self.planificacion.maquina.nombre)
#        d = unicode(self.planificacion.descripcion)
#        f = unicode(self.fichero)
#        f = len(f)>20 and f[:15]+"..."+f[-5:] or f
#        if (self.seq_inicio is None) or (self.seq_fin is None):
#            return u"%s (%s) %s" % (m, d, f)
#        else:
#            return u"%s (%s) %s [%d:%d]" % (m, d, f, self.seq_inicio, self.seq_fin)
#
#    def get_maquina_planificacion(self):
#        return self.planificacion.maquina

#    class Meta:
#        ordering = ['pattern',]
#        verbose_name_plural = _(u'File backup products')
#        verbose_name = _(u'File backup product')

class FileBackupProduct(models.Model):
    file_backup_task = models.ForeignKey(FileBackupTask, related_name = 'file_backup')
    file_pattern = models.ForeignKey(FileNamePattern)
    start_seq = models.IntegerField(blank=True, null=True,
        help_text=_(u'If there is more than one file_pattern, the initial value of the sequence'))
    end_seq= models.IntegerField(blank=True, null=True,
        help_text=_(u'If there is more than one file_pattern, the last value of the sequence'))
    task = models.ForeignKey(FileBackupTask, verbose_name=_(u"Task"))
    variable_percentage = models.DecimalField(default=20, max_digits=2, decimal_places=0, null=True, blank=True,
        help_text=_(u"% size that you expect to change between two backups"))

class BackupFile(models.Model):
    file_backup_product = models.ForeignKey(FileBackupProduct)

    original_file_name = models.CharField(_(u'Original file name'), max_length=512,
        help_text=_(u'Exact file name generated by a backup task.'))
    original_md5 = models.CharField(_(u'MD5 original file hash'), max_length=32,
        help_text=_(u'MD5 original file hash.'))
    original_file_size= models.FloatField(_(u'Original file size'), help_text=_(u'Original file size in bytes'))

    original_date = models.DateTimeField(blank=True, null=True, help_text=_(u'Original file creation date'))

    compressed_file_name = models.CharField(_(u'Compressed file name'), max_length=512,
        help_text=_(u'Exact file name generated by a backup task once it has been compressed.'))
    compressed_md5 = models.CharField(_(u'Compressed MD5 file hash'), max_length=32,
        help_text=_(u'Compressed MD5 file hash.'))
    compressed_file_size= models.FloatField(_(u'Compressed file size'),
        help_text=_(u'Compressed file size in bytes.'), blank=True, null=True)

    compressed_date = models.DateTimeField(blank=True, null=True, help_text=_(u'Compression date'))

    deletion_date = models.DateTimeField(blank=True, null=True, help_text = _(u"Deletion date"))

    disk_id = models.CharField(_(u'External disk'), max_length=512,
        help_text=_(u'External disk where this file is.'), blank=True, null=True)
    integrity_checked = models.NullBooleanField(blank=True, null=True,
        help_text=_(u'Integrity checked (uncompressable, MD5 hash is correct).'))
    utility_checked = models.NullBooleanField(blank=True, null=True,
        help_text=_(u'Useful.'))

    def machine(self):
        return self.file_backup_product.file_backup_task.machine

    def directory(self):
        return self.file_backup_product.file_backup_task.directory

    def checker(self):
        return self.file_backup_product.file_backup_task.checker_fqdn

    def original_file_size_display (self):
        if self.original_file_size:
            return str(self._sizeof_fmt (self.original_file_size))
        else:
            return '0'

    def compressed_file_size_display (self):
        if self.compressed_file_size:
            return str(self._sizeof_fmt (self.compressed_file_size))
        else:
            return '0'

    def _sizeof_fmt(self, num):
        num = float (num)
        for x in ['bytes','KB','MB','GB','TB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0

    def __unicode__(self):
        return "%s" % self.original_file_name

    class Meta:
        ordering = ['-original_date',]
        verbose_name_plural = _(u'Backup files')
        verbose_name = _(u'Backup file')

