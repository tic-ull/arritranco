from django.shortcuts import render_to_response
from rest_framework.views import Response, APIView
from django.template import Context
from monitoring.nagios.models import Service
from monitoring.sondas.models import Sonda, NagiosNrpeCheckOpts


class NrpeCfg(APIView):
    """ Returns cfg file with nrpechecks."""
    def get(self, request, format=None):
        template = "nagioscfg_template.cfg"
        response = render_to_response(template,
                                      Context({
                                          "NrpeCheckOpts": NagiosNrpeCheckOpts.objects.all(),
                                          "sondas": Sonda.objects.all(),
                                          "services": Service.objects.all(),
                                      }),
                                      mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=nrpe_checks.cfg'
        return response

class NrpeHosts(APIView):
    """ Returns hosts entries for services.

    Services will be checked by sondas, so we need that entries if we plan
    to check it from other nagios than our core one.
    """
    def get(self, request, format=None):

        template = "nagios/hosts.cfg"

        response = render_to_response(template,
                                      Context({
                                          "services": Service.objects.all(),
                                      }),
                                      mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=nrpe_hosts.cfg'
        return response