from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader, RequestContext
from imSupport.apps.msupport.models import Application, Environment, Instance
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from imSupport.apps.msupport.audit import AuditObject
from imSupport.apps.msupport.appman.json_types import instance_j
from imSupport.apps.msupport.tasks import mqtools_action
　
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
def mqtools(request):
    request.session.set_expiry(1800)
　
    qmgr = ""
    queue = ""
    errormsg = ""
    msg = ""
    res = ""
    cr = ""
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
　
    if request.method == "GET" and request.GET:
　
        try:
            qmgr = request.GET['qmgr']
        except:
            pass
　
        try:
            queue = request.GET['queue']
        except:
            pass
        inst = request.GET['instance']
        server = request.GET['server']
        prod = request.GET['product']
        action = request.GET['command']
　
    elif request.method == "POST" and request.POST:
　
        try:
            qmgr = request.POST['qmgr']
        except:
            pass
　
        try:
            queue = request.POST['queue']
        except:
            pass
　
        inst = request.POST['instance']
        server = request.POST['server']
        prod = request.POST['product']
        action = request.POST['command']
　
        cr = request.POST['cr']
　
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
                if action == "start" or action == "stop" or action == "clearq":
                    if len(cr) == 0:
                        template = loader.get_template('msupport/mqtools_cr_confirm.html')
　
                        context = RequestContext(request, {
                            'mqtools': "true",
                            'instance': instobj,
                            'server': server,
                            'product': prod,
                            'action': action,
                            'qmgr': qmgr,
                            'queue': queue,
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
            if action == "check":
                action_out = "MQ_check.sh " + qmgr + " detail"
                description = "Check QMGR"
            elif action == "start":
                action_out = "MQ_start.sh manager " + qmgr
                description = "Start QMGR"
            elif action == "stop":
                action_out = "MQ_stop.sh manager " + qmgr
                description = "Stop QMGR"
            elif action == "browseq":
                action_out = "MQ_queue.sh browse " + qmgr + " " + queue
                description = "Browse Queue"
            elif action == "clearq":
                action_out = "MQ_queue.sh clear " + qmgr + " " + queue
                description = "Clear Queue"
　
            cmd = mq_tools_commandgen(instobj, action_out, osuser)
　
            json_inst = instance_j(instobj.name, instobj.server.name, instobj.product.version, instobj.product.osuser, "", instobj.cluster)
            json_inst.set_profile(instobj.profile)
            in1 = json_inst.to_JSON()
            in2 = json.dumps(str(request.user), sort_keys=True, indent=4)
            in4 = json.dumps(cmd, sort_keys=True, indent=4)
　
            msg = mqtools_action.apply_async((in1, in2, in4), expires=3600)
            res = ""
　
            try:
                task_list = request.session['task_list']
            except:
                task_list = []
　
            task_detail = {}
　
            task_detail['key'] = msg
            task_detail['action'] = description
            task_detail['type'] = "mqtools"
            task_detail['instance'] = instobj.name
            task_detail['qmgr'] = qmgr
            task_detail['queue'] = queue
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
　
    crmsg = ""
    if len(cr) > 0:
        crmsg = " Production CR or Ticket: " + cr
　
    a = AuditObject()
　
    a.recordAction("MQTools Action " + action + crmsg, None, instobj, None, None, request.user.username)
　
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
        'qms': qms,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def dispqmgr(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser)
            logger.error("2Executing command:")
            logger.error(cmd)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
　
                    for s in out.splitlines():
                        if s.startswith("USER"):
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            key = find_between(s, "QMNAME=", "|")
                            val = s.split("STATUS=", 1)[1]
                            logger.error("----->K:" + key + "----" + val)
                            qms[key] = val
　
                    logger.error("----->U:" + out_user + "----C:" + out_cmd)
　
                    msg = out
                    msg += err
                else:
                    res = "Action unsuccessful"
                    msg = out
                    msg += err
            except Exception as e:
                logger.error("exception")
                res = "Action unsuccessful"
                msg = str(e)
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_dispqmgr.html')
　
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        'qms': qms,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def getqmgr(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
    qmgr = request.GET['qmgr']
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
　
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser, qmgr)
            logger.error("2Executing command:")
            logger.error(cmd)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
　
                    for s in out.splitlines():
                        if s.startswith("USER"):
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            qmprops = s.split("|")
                            for prop in qmprops:
                                kvpair = prop.split("=")
                                qms[kvpair[0]] = kvpair[1]
　
                    logger.error("----->U:" + out_user + "----C:" + out_cmd)
　
                    msg = out
                    msg += err
                else:
                    res = "Action unsuccessful"
                    msg = out
                    msg += err
            except Exception as e:
                logger.error("exception")
                res = "Action unsuccessful"
                msg = str(e)
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_getqmgr.html')
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        'qms': qms,
        'qmgr': qmgr,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def dispchannel(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
    qmgr = request.GET['qmgr']
    try:
        pattern = request.GET['pattern']
    except:
        pattern = None
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
　
    status_list = []
　
    #time.sleep(5)
    try:
        cancel = request.POST['cancel']
        if cancel is not None:
            return HttpResponseRedirect('/appman/')
    except:
        logger.info("do nothing")
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser, qmgr, pattern)
            logger.error("2Executing command:")
            logger.error(cmd)
　
            cmd_s = commandgen(instobj, "dispchannelstatus", osuser, qmgr, pattern)
            logger.error("2Executing command:")
            logger.error(cmd_s)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                result_s = 0
                out_s = ""
                err_s = ""
　
                try:
                    result_s, out_s, err_s = processor(settings.RUNAS, cmd_s)
                except:
                    logger.error("----->exception getting status for channels: " + cmd_s)
                if result == 0:
                    res = "Action successful"
　
                    for s in out.splitlines():
                        if s.startswith("USER"):
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            if pattern is None:
                                qmprops = s.split("|")
                                qmprops[0] = qmprops[0].replace("CHANNEL=", "")
                                qmprops[1] = qmprops[1].replace("CHLTYPE=", "")
                                qms[qmprops[0]] = qmprops[1]
                            else:
                                qmprops = s.split("|")
                                for prop in qmprops:
                                    kvpair = prop.split("=")
                                    qms[kvpair[0]] = kvpair[1]
　
                    logger.error("----->U:" + out_user + "----C:" + out_cmd)
　
                    logger.error("Doing status checks")
　
                    try:
                        if result_s == 0:
                            for chs in out_s.splitlines():
                                if not chs.startswith("USER"):
                                    if not chs.startswith("CMD"):
                                        thisstat = find_between(chs, "CHANNEL=", "|")
                                        thisstat = thisstat.split("|", 1)[0]
                                        logger.error("---->" + thisstat)
                                        status_list.append(thisstat)
                    except Exception as e:
                        logger.error("Exception Doing status checks" + str(e))
　
                    msg = out
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
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_dispchannel.html')
　
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        'qms': qms,
        'qmgr': qmgr,
        'pattern': pattern,
        'status_list': status_list,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def dispchannelstatus(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
    qmgr = request.GET['qmgr']
    try:
        pattern = request.GET['pattern']
    except:
        pattern = None
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
　
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser, qmgr, pattern)
            logger.error("2Executing command:")
            logger.error(cmd)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
　
                    for s in out.splitlines():
                        if s.startswith("USER"):
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            if pattern is None:
                                qmprops = s.split("|")
                                qmprops[0] = qmprops[0].replace("CHANNEL=", "")
                                qmprops[1] = qmprops[1].replace("CHLTYPE=", "")
                                qms[qmprops[0]] = qmprops[1]
                            else:
                                qmprops = s.split("|")
                                for prop in qmprops:
                                    kvpair = prop.split("=")
                                    qms[kvpair[0]] = kvpair[1]
　
                    logger.error("----->U:" + out_user + "----C:" + out_cmd)
　
                    msg = out
                    msg += err
                else:
                    res = "Action unsuccessful"
                    msg = out
                    msg += err
            except Exception as e:
                logger.error("exception")
                res = "Action unsuccessful"
                msg = str(e)
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_dispchannel.html')
　
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        'qms': qms,
        'qmgr': qmgr,
        'pattern': pattern,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def dispq(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
    qmgr = request.GET['qmgr']
    try:
        pattern = request.GET['pattern']
    except:
        pattern = None
　
    try:
        filterby = request.GET['filterby']
        cond = request.GET['cond']
        filtertxt = request.GET['filtertxt']
        if filterby == "CURDEPTH":
            attrib = "CURDEPTH_where-curdepth_" + cond + "_" + filtertxt + "-"
        elif filterby == "DEFPSIST":
            attrib = "where-DEFPSIST_" + cond + "_" + filtertxt + "-"
    except:
        filterby = None
        cond = None
        filtertxt = None
        attrib = None
　
    url = request.path
　
    logger = logging.getLogger('django.request')
    qms = {}
    out_user = ""
    out_cmd = ""
    errormsg = ""
    msg = ""
    res = ""
　
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser, qmgr, pattern, attrib)
            logger.error("2Executing command:")
            logger.error(cmd)
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
                    logger.error("HERE1")
                    for s in out.splitlines():
                        logger.error("HERE2")
                        if s.startswith("USER"):
                            logger.error("HERE3")
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            logger.error("HERE4")
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            logger.error("HERE5")
                            if pattern is None:
                                qmprops = s.split("|")
                                logger.error("---->Q:" + qmprops[0] + "====" + qmprops[1])
                                qmprops[0] = qmprops[0].replace("QUEUE=", "")
                                qmprops[1] = qmprops[1].replace("TYPE=", "")
                                qms[qmprops[0]] = qmprops[1]
                            else:
                                qmprops = s.split("|")
                                for prop in qmprops:
                                    kvpair = prop.split("=")
                                    qms[kvpair[0]] = kvpair[1]
　
                    logger.error("----->U:" + out_user + "----C:" + out_cmd)
　
                    msg = out
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
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_dispq.html')
　
    context = RequestContext(request, {
        'appman': "true",
        'action': action,
        'instance': inst,
        'instobj': instobj,
        'server': server,
        'result': res,
        'message': msg,
        'errormsg': errormsg,
        'out_user': out_user,
        'out_cmd': out_cmd,
        'qms': qms,
        'qmgr': qmgr,
        'product': prod,
        'pattern': pattern,
        'attrib': attrib,
        'status_list': status_list,
        'requrl': url,
        'filterby': filterby,
        'cond': cond,
        'filtertxt': filtertxt,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def dispmqver(request):
    request.session.set_expiry(1800)
    action = request.GET['command']
    inst = request.GET['instance']
    server = request.GET['server']
    prod = request.GET['product']
　
    logger = logging.getLogger('django.request')
    out_user = ""
    out_cmd = ""
    msg = ""
    errormsg = ""
    msg = ""
    res = ""
    try:
        cancel = request.POST['cancel']
        if cancel is not None:
            return HttpResponseRedirect('/appman/')
    except:
        logger.info("do nothing")
        # do nothing
　
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
　
            osuser = instobj.product.osuser
　
            cmd = commandgen(instobj, action, osuser)
            logger.error("2Executing command:")
            logger.error(cmd)
　
            try:
                result = 0
                out = ""
                err = ""
　
                result, out, err = processor(settings.RUNAS, cmd)
　
                if result == 0:
                    res = "Action successful"
　
                    for s in out.splitlines():
                        if s.startswith("USER"):
                            out_user = s.split("USER|", 1)[1]
                        elif s.startswith("CMD"):
                            out_cmd = s.split("CMD|", 1)[1]
                        else:
                            msg = msg + s + "<BR>"
　
                    msg += err
                else:
                    res = "Action unsuccessful"
                    msg = out
                    msg += err
            except Exception as e:
                logger.error("exception")
                res = "Action unsuccessful"
                msg = str(e)
　
            msg = msg.replace("\n", "<BR>\n")
        else:
            errormsg = "User " + request.user.username + " has no access to this instance " + inst + "."
    else:
        res = "App Man Data Error (multiple servers with the same name defined?)"
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    a = AuditObject()
　
    a.recordAction("Appman MQ Action " + action, None, instobj, None, None, request.user.username)
　
    template = loader.get_template('msupport/mq_appman_dispmqver.html')
　
    context = RequestContext(request, {
        'appman': "true",
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
　
　
def commandgen(inst, action, osuser, qmgr=None, pattern=None, attrib=None):
　
    cmd = settings.E2OSROOT
    cmd += '/scripts/MQManager.pl -host='
    cmd += inst.server.name
    cmd += ' -version=default'
    cmd += ' -action='
    cmd += action
    cmd += ' -user='
    cmd += osuser
　
    if qmgr is not None:
        cmd += ' -qmgr='
        cmd += qmgr
　
    if attrib is not None:
        cmd += ' -attrib='
        cmd += attrib
　
    if pattern is not None:
        cmd += ' -pattern='
        cmd += pattern
　
    return cmd
def mq_tools_commandgen(inst, action, osuser):
　
    cmd = settings.E2OSROOT
    cmd += '/scripts/MQPackageExecutor.pl -host='
    cmd += inst.server.name
    cmd += ' -user='
    cmd += osuser
    cmd += ' -command="'
    cmd += action
    cmd += '"'
　
    return cmd
　
