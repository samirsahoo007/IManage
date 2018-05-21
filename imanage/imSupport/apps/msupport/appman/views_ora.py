from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader, RequestContext
from imSupport.apps.msupport.models import Application, Environment, Instance
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from imSupport.apps.msupport.audit import AuditObject
from imSupport.apps.msupport.appman.json_types import instance_j
from imSupport.apps.msupport.tasks import oratools_action
　
import json
import logging
import os
import sys
import subprocess
import shlex
import pwd
import time
　
logger = logging.getLogger('django.request')
　
　
@login_required
def oratools(request):
    request.session.set_expiry(1800)
　
    server = ""
    prod = ""
    inst = ""
    orainst = ""
    orainstv = 0
    action = ""
    cr = ""
　
    logger = logging.getLogger('django.request')
　
    out_user = ""
    out_cmd = ""
　
    if request.method == "GET" and request.GET:
　
        server = request.GET['server']
        prod = request.GET['product']
        inst = request.GET['instance']
        action = request.GET['action']
        try:
            orainst = request.GET['orainst']
            orainstv = 1
        except:
            orainst = ""
            orainstv = 0
        try:
            cr = request.GET['cr']
        except:
            cr = ""
　
    elif request.method == "POST" and request.POST:
　
        server = request.POST['server']
        prod = request.POST['product']
        inst = request.POST['instance']
        action = request.POST['action']
        try:
            orainst = request.POST['orainst']
            orainstv = 1
        except:
            orainst = ""
            orainstv = 0
　
　
        cr = request.POST['cr']
　
        try:
            if orainstv == 0:
                return HttpResponseRedirect('/appman/')
　
            cancel = request.POST['cancel']
            if cancel is not None:
                return HttpResponseRedirect('/appman/')
        except:
            logger.info("do nothing")
            # do nothing
　
    logger.error('ORATOOLS: ' + action)
    instobj = ""
    try:
        instobjs = Instance.objects.filter(server__name=server).filter(name=inst).filter(product__version=prod)
        instobjs.select_related()
　
        for thisinst in instobjs:
            if thisinst.server.name == server:
                instobj = thisinst
    except Exception as e:
        logger.error("no instance object in db" + e.message)
        logger.error(sys.exc_info()[0])
　
        return HttpResponseRedirect('/appman/')
　
    if instobj.server.name == server:
　
        logger.error("Checking Access:")
        if check_access(instobj, request.user, action):
            logger.error("Done Checking Access:")
　
            isprod = False
            envs = instobj.environment_set.all()
            for thisenv in envs:
                if thisenv.type == 'PRD':
                    isprod = True
　
            if isprod:
                if action == "start" or action == "stop":
                    if len(cr) == 0:
                        template = loader.get_template('msupport/oratools_cr_confirm.html')
　
                        context = RequestContext(request, {
                            'oratools': "true",
                            'instance': instobj,
                            'server': server,
                            'product': prod,
                            'action': action,
                            'orainst': orainst,
                            })
　
                        return HttpResponse(template.render(context))
                    else:
                        crerr = False
                        cr = cr.upper()
                        if cr.find(' ') > 0:
                            crerr = True
                            crmsg = "CR or Ticket input contains spaces"
                        elif cr.startswith('CR'):
                            cr = cr.replace('CR', '')
                            if int(cr) < 700000:
                                crerr = True
                                crmsg = "Invalid CR provided."
                        elif cr.startswith('T'):
                            cr = cr.replace('T', '')
                            if int(cr) < 19000000:
                                crerr = True
                                crmsg = "Invalid Ticket provided."
                        elif not cr.startswith('IN'):
                            crerr = True
                            crmsg = "Invalid CR or Ticket provided."
　
                        if crerr:
                            a = AuditObject()
　
                            a.recordAction("Appman Action " + action + " " + crmsg, None, instobj, None, None, request.user.username)
                            template = loader.get_template('msupport/appman_result.html')
　
                            context = RequestContext(request, {
                                'appman': "true",
                                'action': action,
                                'instance': inst,
                                'instobj': instobj,
                                'server': server,
                                'result': "Action Unsuccessful",
                                'message': crmsg,
                                })
　
                            return HttpResponse(template.render(context))
　
            osuser = instobj.product.osuser
　
            action_out = ""
            description = ""
            if action == "start":
                action_out = "oraControl.bash SELECT '.db' start " + orainst
                description = "Start DB Instance: " + orainst
            elif action == "stop":
                action_out = "oraControl.bash SELECT '.db' stop " + orainst
                description = "Stop DB Instance: " + orainst
　
            cmd = ora_tools_commandgen(instobj, action_out, osuser)
　
            logger.error('ORATOOLS: ' + action + 'Command:  ' + cmd)
            json_inst = instance_j(instobj.name, instobj.server.name, instobj.product.version, instobj.product.osuser, "", instobj.cluster)
            json_inst.set_profile(instobj.profile)
            in1 = json_inst.to_JSON()
            in2 = json.dumps(str(request.user), sort_keys=True, indent=4)
            in4 = json.dumps(cmd, sort_keys=True, indent=4)
　
            msg = oratools_action.apply_async((in1, in2, in4), expires=3600)
　
            res = ""
　
            try:
                task_list = request.session['task_list']
            except:
                task_list = []
　
            task_detail = {}
　
            task_detail['key'] = msg
            task_detail['action'] = description
            task_detail['type'] = "oratools"
            task_detail['orainst'] = orainst
            task_detail['instance'] = instobj.name
            task_detail['product'] = instobj.product.version
            task_detail['server'] = instobj.server.name
            datetime = time.strftime("%c")
            datetime = datetime.replace(' ', '&nbsp;')
            task_detail['date'] = time.strftime("%c")
　
            task_list.append(task_detail)
　
            request.session['task_list'] = task_list
　
　
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
            msg = ""
    else:
        res = "Data Error (multiple servers with the same name defined?)"
　
    #msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    #msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    errormsg = ""
    crmsg = ""
    if len(cr) > 0:
        crmsg = " Production CR or Ticket: " + cr
　
    a = AuditObject()
　
    a.recordAction("ORATools Action " + action + crmsg, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/appman_result.html')
　
    context = RequestContext(request, {
        'mqtools': "true",
        'type': action,
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        })
　
    return HttpResponse(template.render(context))
@login_required
def listinst(request):
    request.session.set_expiry(1800)
    server = request.GET['server']
    prod = request.GET['product']
    inst = request.GET['instance']
    try:
        orainst = request.GET['orainst']
        orainstv = 1
    except:
        orainst = ""
        orainstv = 0
　
    try:
        listener = request.GET['listener']
    except:
        listener = "false"
　
　
　
    logger = logging.getLogger('django.request')
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
    orainsts = []
　
    status_list = []
　
    #time.sleep(5)
    try:
        cancel = request.POST['cancel']
        if cancel is not None:
            return HttpResponseRedirect('/appman/')
    except:
        logger.info("do nothing")
        # do nothing
　
    instobj = ""
    try:
        instobjs = Instance.objects.filter(server__name=server)
        instobjs.select_related()
　
        for thisinst in instobjs:
            if thisinst.server.name == server:
                instobj = thisinst
    except Exception as e:
        logger.error("no instance object in db" + e.message)
        logger.error(sys.exc_info()[0])
        return HttpResponseRedirect('/appman/')
　
    if instobj.server.name == server:
　
        logger.error("Checking Access:")
        action = "status"
        if check_access(instobj, request.user, action):
            logger.error("Done Checking Access:")
　
            osuser = instobj.product.osuser
　
            if listener == "false":
                if orainst == "":
                    action_out = "oraControl.bash SELECT '.db' Status "
                else:
                    action_out = "oraControl.bash SELECT '.db' Status " + orainst
            else:
                if orainst == "":
                    action_out = "oraControl.bash SELECT list Status "
                else:
                    action_out = "oraControl.bash SELECT list Status " + orainst
　
            cmd = ora_tools_commandgen(instobj, action_out, osuser)
　
            logger.error("2Executing command:")
            logger.error(cmd)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
                    msg = out
                    out = out.replace("\n"," ");
                    o = find_between(out, "INSTANCES|", "|ENDINSTANCES");
                    orainsts = o.split();
                    msg += err
                else:
                    res = "Action unsuccessful"
                    msg = out
                    msg += err
                    msg += err_s
            except Exception as e:
                logger.error("exception")
                res = "Action unsuccessful"
                msg = str(e)
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/ora_list_instance.html')
　
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instancev': orainstv,
        'instance': orainst,
        'orainsts': orainsts,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'listener': listener,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        })
　
    return HttpResponse(template.render(context))
　
　
def find_between(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""
　
　
def check_access(inst, user, action):
　
    ret = False
    eng_region = []
    is_engineer = False
　
    for g in user.groups.all():
        if "_engineers" in g.name:
            is_engineer = True
            eng_region.append(g.name.split("_")[0])
　
    if is_engineer:
        for thisreg in eng_region:
            if thisreg == inst.region.region:
                ret = True
    else:
        apps = get_objects_for_user(user, 'appdev', Application)
　
        for thisapp in apps:
            envs = Environment.objects.filter(application__appcode=thisapp.appcode)
            #envs = envs.select_related()
            for env in envs:
                for thisinst in env.instances.filter(pk=inst.pk):
                    if thisinst.name == inst.name and thisinst.product.name == inst.product.name:
                        if env.type != 'PRD' and env.type != 'DR':
                            ret = True
                        elif action == 'nistatus':
                            ret = True
    return ret
　
　
def processor(runas, cmd):
　
    logger = logging.getLogger('django.request')
　
    thisosuser = runas
    pwrecord = pwd.getpwnam(thisosuser)
    user_name = pwrecord.pw_name
    user_home_dir = pwrecord.pw_dir
    user_uid = pwrecord.pw_uid
    user_gid = pwrecord.pw_gid
    env = os.environ.copy()
    env['HOME'] = user_home_dir
    env['LOGNAME'] = user_name
    env['USER'] = user_name
    env['E2ROOT'] = settings.E2OSROOT
    try:
        args = shlex.split(cmd)
        process = subprocess.Popen(args, preexec_fn=demote(user_uid, user_gid), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        logger.error("Direct Exception Executing Command: " + str(e))
    out, err = process.communicate()
　
    result = process.returncode
    return result, out, err
　
　
def demote(user_uid, user_gid):
    def result():
        #os.setgid(user_gid)
        #os.setuid(user_uid)
        val = 'do something'
        val += 'do something else'
    return result
　
　
def ora_tools_commandgen(inst, action, osuser):
　
    cmd = settings.E2OSROOT
    cmd += '/scripts/ORAPackageExecutor.pl -host='
    cmd += inst.server.name
    cmd += ' -user='
    cmd += osuser
    cmd += ' -action=ora_tools -command="'
    cmd += action
    cmd += '"'
　
    return cmd
　
