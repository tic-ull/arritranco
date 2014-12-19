from django.core.management.base import BaseCommand
from worker.tasks import inventario_heartbeat


class Command(BaseCommand):
   help = "Send keep alive to celerys workers"

   def handle(self, *args, **options):
         res = inventario_heartbeat.apply_async(serializer="json", queue="dbackup.stic.ull.es", ignore_result=True)

