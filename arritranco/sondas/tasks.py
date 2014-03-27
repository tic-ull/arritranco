from __future__ import absolute_import

from celery import shared_task
from fabric.api import env, run, put
from fabric.contrib.files import exists
from django.conf import settings
from sondas.models import Sonda, SondaTasksLog, SondaTask, SondaTaskStatus, NagiosNrpeCheckOpts
import sys
import datetime
from django.template import Template, Context


@shared_task
def ssh_key_send_task(sonda_pk, user, passwd, tasklog_pk):
    sonda = Sonda.objects.get(pk=sonda_pk)
    if SondaTask.objects.filter(name="ssh_key").count() == 0:
        task = SondaTask()
        task.name = "ssh_key"
        task.description = "send the ssh key to a sonda"
        task.save()
    if tasklog_pk is None:
        tasklog = SondaTasksLog()
        tasklog.sonda = sonda
        tasklog.task = SondaTask.objects.get(name="ssh_key")
        tasklog.save()
    else:
        tasklog = SondaTasksLog.objects.get(pk=tasklog_pk)
    taskstatus = SondaTaskStatus()
    taskstatus.tasklog = tasklog

    try:
        env.skip_bad_hosts = True
        env.abort_on_prompts = True
        env.user = user
        env.password = passwd
        env.host_string = str(sonda.address)

        if sonda.script_inicio != "":
            f = open("tmp/script_inicio_" + sonda.name, "w")
            f.write(sonda.script_inicio.replace("\r", ""))
            f.close()
            put("tmp/script_inicio_" + sonda.name, "/tmp/script_inicio")
            run("chmod 700 /tmp/script_inicio")
            run("/tmp/script_inicio")

        if not exists('/root/.ssh/'):
            run("mkdir /root/.ssh")
        if not exists('/root/.ssh/authorized/'):
            run("mkdir /root/.ssh/authorized")
        put(settings.PROJECT_ROOT + "/keys/id_rsa.pub", "/root/.ssh/authorized/id_rsa.pub")
        run("cat /root/.ssh/authorized/id_rsa.pub >> /root/.ssh/authorized_keys")
        sonda.ssh = True
        sonda.save()
        print("Config done with " + sonda.name)
        taskstatus.message = "Config done with " + sonda.name
        taskstatus.status = 0
        env.password = ""
    except Exception as e:
        taskstatus.message = str(e)
        taskstatus.status = 1

    except:
        fail = "Unknow exeption !\n sys exc info : \n"
        for fails in sys.exc_info()[0:5]:
            fail += str(fails) + "\n"
        taskstatus.message = fail
        taskstatus.status = 2

    taskstatus.timestamp = datetime.datetime.now()
    taskstatus.save()


@shared_task
def send_nrpecfg(sonda_pk, tasklog_pk):
    sonda = Sonda.objects.get(pk=sonda_pk)
    if SondaTask.objects.filter(name="send_nrpecfg").count() == 0:
        task = SondaTask()
        task.name = "send_nrpecfg"
        task.description = "send the nrpe configuration to the sonda"
        task.save()
    if tasklog_pk is None:
        tasklog = SondaTasksLog()
        tasklog.sonda = sonda
        tasklog.task = SondaTask.objects.get(name="send_nrpecfg")
        tasklog.save()
    else:
        tasklog = SondaTasksLog.objects.get(pk=tasklog_pk)
    taskstatus = SondaTaskStatus()
    taskstatus.tasklog = tasklog

    try:

        data = {"NAGIOS_SERVER": sonda.servidor_nagios, "checks": []}
        custom_checks = []
        for nagiosnrpecheckopts in NagiosNrpeCheckOpts.objects.filter(sonda=sonda):
            data["checks"].append("[" + sonda.name + "_" +
                                  nagiosnrpecheckopts.service.name + "_" +
                                  nagiosnrpecheckopts.host.name + "]=" +
                                  sonda.dir_checks + "/" +
                                  nagiosnrpecheckopts.service.command.replace("$HOST", nagiosnrpecheckopts.host.address))
            if not nagiosnrpecheckopts.service.command_nativo:
                f = open("tmp/" + nagiosnrpecheckopts.service.name, "w")
                f.write(nagiosnrpecheckopts.service.command_script.replace("$HOST", nagiosnrpecheckopts.host.name))
                f.close()
                custom_checks.append(nagiosnrpecheckopts.service.name)

        f = open("templates/nrpe.cfg", "r")
        template = Template(f.read())
        f.close()

        nrpecfg = open("tmp/nrpe_" + sonda.name + ".cfg", "w")
        nrpecfg.write(template.render(Context(data)))
        nrpecfg.close()

        env.skip_bad_hosts = True
        env.abort_on_prompts = True
        env.user = "root"
        env.host_string = str(sonda.address)
        env.key_filename = settings.PROJECT_ROOT + '/keys/id_rsa'

        if sonda.script_inicio is not None:
            f = open("tmp/script_inicio_" + sonda.name, "w")
            f.write(sonda.script_inicio.replace("\r", ""))
            f.close()
            put("tmp/script_inicio_" + sonda.name, "/tmp/script_inicio")
            run("chmod 700 /tmp/script_inicio")
            run("/tmp/script_inicio")

        put("tmp/nrpe_" + sonda.name + ".cfg", "/etc/nagios/nrpe.cfg")
        for check in custom_checks:
            put("tmp/" + check, sonda.dir_checks + "/check_" + check)  # FAIL = Problem Space in rpi !!
            run("chmod +x " + sonda.dir_checks + "/check_" + check)

        run("service " + sonda.nrpe_service_name + " restart")

        taskstatus.message = "nrpe.cfg send to " + sonda.name
        taskstatus.status = 0

    except Exception as e:
        taskstatus.message = str(e)
        taskstatus.status = 1
    except:
        fail = "Unknow exeption !\n sys exc info : \n"
        for fails in sys.exc_info()[0:5]:
            fail += str(fails) + "\n"
        taskstatus.message = fail
        taskstatus.status = 2

    taskstatus.timestamp = datetime.datetime.now()
    taskstatus.save()
