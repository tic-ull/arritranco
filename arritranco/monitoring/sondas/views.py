from django.shortcuts import render_to_response
from rest_framework.views import Response, APIView
from django.template import Context
from monitoring.nagios.models import Service
from monitoring.sondas.models import Sonda, NagiosNrpeCheckOpts


class NrpeCfg(APIView):

    def get(self, request, format=None):

        template = "nagioscfg_template.cfg"

        response = render_to_response(template,
                                      Context({
                                          "NrpeCheckOpts": NagiosNrpeCheckOpts.objects.all(),
                                          "sondas": Sonda.objects.all(),
                                          "services": Service.objects.all(),
                                      }),
                                      mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=nagios.cfg'
        return response