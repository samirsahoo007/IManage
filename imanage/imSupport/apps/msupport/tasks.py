from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm
from imSupport.apps.msupport.appman.json_types import instance_j
　
import threading
import logging
import os
import subprocess
import shlex
import json
import time
import traceback
import sys
from imSupport.apps.msupport.appman import pwd
from imSupport.apps.msupport.models import Application, ApplicationRoles, Environment, Instance, Datacenter, User, Roles, Server
from imSupport.apps.msupport.audit import AuditObject
from imSupport.apps.msupport.e2admin.views import envScanFunction
　
import pexpect, time
　
　
logger = logging.getLogger('django.request')
　
　
@shared_task
def do_something(thisin):
    logger.error("----->Celery " + thisin)
    return None
　
　
@shared_task
def oratools_action(instobj_json, user_json, command_json):
　
    instance = json.loads(instobj_json)
    user = json.loads(user_json)
    command = json.loads(command_json)
　
    logger = logging.getLogger('django.request')
　
    out_user = ""
    out_cmd = ""
    osuser = ""
　
    instobj = ""
    try:
        instobjs = Instance.objects.filter(server__name=instance['server_name']).filter(name=instance['name']).filter(product__version=instance['product_version'])
        instobjs.select_related()
        for thisinst in instobjs:
            if thisinst.server.name == instance['server_name']:
                instobj = thisinst
　
    except Exception as e:
        logger.error("no instance object in db" + e.message)
        logger.error(sys.exc_info()[0])
　
        return HttpResponseRedirect('/devtools/')
　
    osuser = instobj.product.osuser
　
    logger.error("2Executing command:")
    logger.error(command)
　
    try:
        result = 0
        out = ""
        err = ""
　
        result, out, err = processor(settings.RUNAS, command)
　
        if result == 0:
            res = "Action successful"
　
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
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    return msg, result, res, out, err, time.strftime("%c")
　
　
@shared_task
def mqtools_action(instobj_json, user_json, command_json):
　
    instance = json.loads(instobj_json)
    user = json.loads(user_json)
    command = json.loads(command_json)
    logger = logging.getLogger('django.request')
　
    out_user = ""
    out_cmd = ""
    osuser = ""
　
    instobj = ""
    try:
        instobjs = Instance.objects.filter(server__name=instance['server_name']).filter(name=instance['name']).filter(product__version=instance['product_version'])
        instobjs.select_related()
　
        for thisinst in instobjs:
            if thisinst.server.name == instance['server_name']:
                instobj = thisinst
　
    except Exception as e:
        logger.error("no instance object in db" + e.message)
        logger.error(sys.exc_info()[0])
　
        return HttpResponseRedirect('/devtools/')
　
    osuser = instobj.product.osuser
　
    logger.error("2Executing command:")
    logger.error(command)
　
    try:
        result = 0
        out = ""
        err = ""
　
        result, out, err = processor(settings.RUNAS, command)
　
        if result == 0:
            res = "Action successful"
　
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
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
    return msg, result, res, out, err, time.strftime("%c")
　
　
@shared_task
def devtools_action(instobj_json, user_json, action_json, command_json):
　
    instance = json.loads(instobj_json)
    user = json.loads(user_json)
    action = json.loads(action_json)
    command = json.loads(command_json)
　
    logger = logging.getLogger('django.request')
　
    out_user = ""
    out_cmd = ""
    osuser = ""
　
    instobj = ""
    try:
        instobjs = Instance.objects.filter(server__name=instance['server_name']).filter(name=instance['name']).filter(product__version=instance['product_version'])
        instobjs.select_related()
　
        for thisinst in instobjs:
            if thisinst.server.name == instance['server_name']:
                instobj = thisinst
　
    except Exception as e:
        logger.error("no instance object in db" + e.message)
        logger.error(sys.exc_info()[0])
　
        return HttpResponseRedirect('/devtools/')
　
    osuser = instobj.product.osuser
　
    action_out = ""
    if action == "archivelogs":
        action_out = "archiveLogs"
    elif action == "cleartemp":
        action_out = "clearTemp"
    else:
        action_out = action
　
    logger.error("2Executing command:")
    logger.error(command)
　
    try:
        result = 0
        out = ""
        err = ""
　
        result, out, err = processor(settings.RUNAS, command)
        if result == 0:
            res = "Action successful"
　
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
　
    msg = msg.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.", "")
    msg = msg.replace("tcgetattr: Inappropriate ioctl for device", "")
　
    return msg, result, res, out, err, time.strftime("%c")
　
　
@shared_task
def rv_download_action(*args, **kwargs):
    instobj = ""
    osuser = ""
    action = ""
　
    instobjs = []
　
    logger.error("----->HERE1")
　
    instobj = json.loads(args[0])
    target = json.loads(args[1])
    logdir = json.loads(args[2])
    dest = json.loads(args[3])
　
    cmd = rv_commandgen(instobj, "cp", target, logdir, dest)
　
    logger.error("Executing command:")
    logger.error(cmd)
　
    result = 0
    out = ""
    err = ""
    msg = ""
    res = ""
    try:
　
        result, out, err = processor(settings.RUNAS, cmd)
        res = "File copied to dest"
　
    except Exception as e:
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("exception" + str(e) + "--" + str(sys.exc_info()[0]))
        #logger.error(str(exc_type) + fname + str(exc_tb.tb_lineno))
        res = "Action unsuccessful"
        msg = str(e)
　
    out = out.replace("\n", "<BR>\n")
    err = err.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.\n", "")
    err = err.replace("tcgetattr: Inappropriate ioctl for device\n", "")
    err = err.replace("\n", "<BR>\n")
    return msg, result, res, out, err, time.strftime("%c")
　
　
@shared_task
def appman_action(*args, **kwargs):
    instobj = ""
    osuser = ""
    action = ""
　
    instobjs = []
　
    logger.error("----->HERE1")
    if len(args) == 5:
        action = json.loads(args[4])
　
        if action == "pause10":
            time.sleep(10)
            return
        elif action == "pause30":
            time.sleep(30)
            return
　
        instobj = json.loads(args[1])
        osuser = json.loads(args[3])
        for thisinst in args[2]:
            instobjs.append(json.loads(thisinst))
    else:
        action = json.loads(args[3])
　
        if action == "pause10":
　
            time.sleep(10)
            return
　
        elif action == "pause30":
　
            time.sleep(30)
            return
　
        instobj = json.loads(args[0])
        osuser = json.loads(args[2])
　
        for thisinst in args[1]:
            instobjs.append(json.loads(thisinst))
　
    logger.error("----->HERE2")
　
    if action.startswith("all"):
        cmds = []
        osuser = instobj['product_osuser']
　
        if instobj['product_version'].startswith("bpm"):
　
            bpmcmds = []
　
            bpmcmds.insert(1, "apptarget")
            bpmcmds.insert(2, "webapp")
            bpmcmds.insert(3, "support")
            bpmcmds.insert(4, "messaging")
            bpmcmds.insert(5, "nodeagent")
            bpmcmds.insert(6, "dmgr")
　
            if action == "allstop":
                # apptarget, webapp, support, messaging
                for x in range(0, 6):
                    try:
                        for thisinst in instobjs:
                            if bpmcmds[x].lower() in thisinst['name'].lower():
                                cmds.append(commandgen(thisinst, "stop", osuser))
                    except:
                        logger.error("Except 1 on all stop range: " + str(x) + "--" + str(traceback.format_exc())+ "--" + str(sys.exc_info()[0]))
　
                for thiscmd in cmds:
                    logger.error("----->CMDi:" + thiscmd)
                for thisinst in instobjs:
                    logger.error("----->CMDti:" + str(thisinst))
            elif action == "allstart":
                #messaging, support, webapp, apptarget
                for x in reversed(range(0, 6)):
                    try:
                        for thisinst in instobjs:
                            if bpmcmds[x].lower() in thisinst['name'].lower():
                                cmds.insert(0, commandgen(thisinst, "start", osuser))
                    except Exception as e:
#                        exc_type, exc_obj, exc_tb = sys.exc_info()
#                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                        logger.error(str(exc_type) + fname + str(exc_tb.tb_lineno))
                        logger.error("Except1 on all start range: " + str(x))
        else:
            for thisinst in instobjs:
                cmd = "not supported"
　
    else:
        osuser = instobj['product_osuser']
　
        cmd = commandgen(instobj, action, osuser)
        logger.error("Executing command:")
        logger.error(cmd)
　
    try:
        result = 0
        res = ""
        out = ""
        err = ""
        msg = ""
　
        if action.startswith("all") and instobj['product_version'].startswith("bpm"):
            tmp_res = 0
            tmp_out = ""
            tmp_err = ""
　
            if action == "allstop":
                # apptarget, webapp, support, messaging
                for x in range(0, 6):
                    try:
                        tmp_res, tmp_out, tmp_err = processor(settings.RUNAS, cmds[x])
                        if tmp_res != 0:
                            result = tmp_res
                        out = out + "\n\n" + tmp_out
                        err = err + "\n\n" + tmp_err
                    except:
                        logger.error("Except 1 on all stop range: " + str(x) + "--" + str(traceback.format_exc())+ "--" + str(sys.exc_info()[0]))
            elif action == "allstart":
                #messaging, support, webapp, apptarget
                for x in reversed(range(0, 6)):
                    try:
                        tmp_res, tmp_out, tmp_err = processor(settings.RUNAS, cmds[x])
                        if tmp_res != 0:
                            result = tmp_res
                        out = out + "\n\n" + tmp_out
                        err = err + "\n\n" + tmp_err
                    except Exception as e:
                        logger.error("Except2 on all start range: " + str(e))
        else:
            result, out, err = processor(settings.RUNAS, cmd)
    except Exception as e:
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("exception" + str(e) + "--" + str(sys.exc_info()[0]))
        #logger.error(str(exc_type) + fname + str(exc_tb.tb_lineno))
        res = "Action unsuccessful"
        msg = str(e)
　
    out = out.replace("\n", "<BR>\n")
    err = err.replace("Pseudo-terminal will not be allocated because stdin is not a terminal.\n", "")
    err = err.replace("tcgetattr: Inappropriate ioctl for device\n", "")
    err = err.replace("\n", "<BR>\n")
    return msg, result, res, out, err, time.strftime("%c")
　
　
def processorStub(runas, cmd):  # stubb
    out = "Test Output"
    err = "Test Error"
    result = 0
    return result, out, err
　
　
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
        out, err = process.communicate()
        result = process.returncode
        return result, out, err
    except Exception as e:
        logger.error("Direct Exception Executing Command: " + str(e))
        return 1, "", ""
　
　
　
　
def time_processor(runas, cmd):
　
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
        #time.sleep(15)
        #process.terminate()
        out, err = process.communicate() # get what has been printed to standard out so far
        return 0, out, err
    except Exception as e:
        logger.error("Direct Exception Executing Command: " + str(e))
        return 1
　
　
def demote(user_uid, user_gid):
    def result():
        #os.setgid(user_gid)
        #os.setuid(user_uid)
        val = 'do something'
        val += 'do something else'
    return result
　
def chk_commandgen(host, user):
    cmd = settings.E2OSROOT
    cmd += '/scripts/TestSSH.sh -host='
    cmd += host
    cmd += ' -user='
    cmd += user
    return cmd
　
　
def rv_commandgen(inst, action, target, logdir, dest):
    cmd = settings.E2OSROOT
    cmd += '/scripts/RemoteView.pl -host='
    cmd += inst['server_name']
    cmd += ' -instance='
    cmd += inst['name']
    cmd += ' -version='
    cmd += inst['product_version']
    cmd += ' -viewpath='
    cmd += logdir
    cmd += ' -user='
    cmd += inst['product_osuser']
    cmd += ' -action='
    cmd += action
    cmd += ' -target='
    cmd += target
    cmd += ' -dest='
    cmd += dest
    return cmd
　
　
def commandgen(inst, action, osuser):
　
    if (action == 'genplugin'):
        cmd = settings.E2OSROOT
        cmd += '/scripts/GenPlugin.pl -host='
        cmd += inst['server_name']
        cmd += ' -webhost='
        cmd += inst['associated_server_name']
        cmd += ' -instance='
        cmd += inst['name']
        cmd += ' -version='
        cmd += inst['product_version']
        cmd += ' -action=instance'
        cmd += ' -user='
        cmd += osuser
    elif (action == 'ripplestart'):
        cmd = settings.E2OSROOT
        cmd += '/scripts/PackageExecutor.pl -host='
        cmd += inst['server_name']
        cmd += ' -inst='
        cmd += inst['cluster']
        cmd += ' -version='
        cmd += inst['product_version']
        cmd += ' -action=ripplestart'
        cmd += ' -user='
        cmd += osuser
　
    else:
        cmd = settings.E2OSROOT
        cmd += '/scripts/AppManager.pl -host='
        cmd += inst['server_name']
        cmd += ' -instance='
        cmd += inst['name']
        cmd += ' -version='
        cmd += inst['product_version']
        cmd += ' -action='
        cmd += action
        cmd += ' -user='
        cmd += osuser
        logger.error('---->HERE BP')
        try:
             if "na" not in inst['profile'].lower() and "n/a" not in inst['profile'].lower() and "dmgrprofile" not in inst['profile'] and inst['profile'] != "appprofile":
                cmd += ' -profile='
                cmd += inst['profile']
　
                logger.error('---->HERE BP:' +cmd)
        except Exception as e:
            logger.error('---->HERE BPF:' +str(e))
    return cmd
　
　
#@shared_task
#def register_action(app_json, host_json, users_json, osusers_json, requser_json, type_json, level_json):
#    logger.error("Register Action1 Called")
#    return register_action(app_json, host_json, None, users_json, osusers_json, requser_json, type_json, level_json)
　
def check_ssh(host, user):
　
    cmd = chk_commandgen(host, user)
　
    logger.error("Executing command:")
    logger.error(cmd)
　
    result = 0
    out = ""
    err = ""
    msg = ""
    res = ""
    try:
　
        logger.error("Testing...")
        result, out, err = time_processor(settings.RUNAS, cmd)
        logger.error("Testing Complete.")
　
        if "Success" in out:
            logger.error("Check SSH Success: " + user + "@" + host) # + "--" + out + " -- " + err)
            return 0
        else:
            logger.error("Check SSH Fail: " + user + "@" + host + "--" + out + " -- " + err)
            return 2
　
    except:
        logger.error("Check SSH Exception: " + user + "@" + host)
        #logger.error(str(exc_type) + fname + str(exc_tb.tb_lineno))
        return 2
　
　
@shared_task
def register_action(app_json, host_json, users_json, osusers_json, requser_json, type_json, level_json, inst_json=None):
    logger.error("Register Action2 Called")
    app = json.loads(app_json)
    host = json.loads(host_json)
    try:
        inst = json.loads(inst_json)
        if inst == "":
            inst = None
    except:
        inst = None
　
    users = json.loads(users_json)
    osusers = json.loads(osusers_json)
    requser = json.loads(requser_json)
    type = json.loads(type_json)
    level = json.loads(level_json)
　
    issue = False
    issue_text = ""
　
    a = AuditObject()
    a.recordAction(type + " Register: " + app, None, None, None, None, requser, None)
　
    server_found = Server.objects.filter(name=host)
　
    if requser != "bulk" and server_found.exists():
　
        logger.error("---->" + type + " Register attempt to register existing env which is forbidden.  Host: " + host)
        return HttpResponseForbidden('<h1>Forbidden</h1>')
    else:
     #   keyresult = accept_server(host)
        keyresult = 0
        badkeys = [3]
　
        retry_limit = 1
        retry_count = 0
        retry_flag = True
　
        logger.error("JG_-----:>>>>" + str(keyresult))
　
        if keyresult in badkeys:
            while retry_flag:
                logger.error("---->Retrying " + type + " Keys Acceptance...")
                keyresult = accept_server(host)
                if keyresult in badkeys:
                    logger.error("---->Failed" + str(keyresult) + " " + str(retry_count))
                    retry_count = retry_count + 1
                else:
                    logger.error("---->" + type + " Keys Accepted.")
                    retry_flag = False
　
                if retry_count > retry_limit:
                    logger.error("---->Retry Limit Exceeded.  Tries: " + str(retry_count))
                    retry_flag = False
                    issue = True
                    issue_text = "Problem with Keys"
　
        else:
            logger.error("---->" + type + " Keys Accepted.")
　
        success = False
        app_name = ""
　
        for thisosuser in osusers:
            logger.error("---->Testing SSH " + host + "-" + thisosuser)
            check_val = check_ssh(host, thisosuser)
            logger.error("---->Testing result: " + str(check_val))
            #check_val = 2
            #if check_val == 2 or (requser != "bulk" and check_val == 1):
            if check_val == 0:
                logger.error("---->KEY CHECK: Check was successful for " + thisosuser + "@" + host)
                logger.error("---->" + type + " Env Scan:" + host + ":" + thisosuser)
　
                out = []
                logger.error("---->STARTING THREAD for " + thisosuser + "@" + host)
                try:
               #     inarg = [host, type, thisosuser, "webentry"]
               #     t = threading.Thread(None, envScanFunction, None, (host, type, thisosuser, "webentry",), out)
               #     t.start()
　
               #     t.join(120)
　
                    logger.error("---->1STARTING THREAD for " + thisosuser + "@" + host)
                    t = envScanWrapper(host, type, thisosuser)
                    logger.error("---->2STARTING THREAD for " + thisosuser + "@" + host)
                    t.join(440)
                    out = []
                    logger.error("---->3STARTING THREAD for " + thisosuser + "@" + host)
                    if t.isAlive():
                        logger.error("---->THREAD Hung for " + thisosuser + "@" + host)
　
                    else:
                        logger.error("1---->THREAD completed for " + thisosuser + "@" + host)
                        out = t.result_queue.get()
                        logger.error("2---->THREAD completed for " + thisosuser + "@" + host)
                    #serv, output, showmessage, showmsg = t.result_queue.get()
                    logger.error("3---->THREAD completed for " + thisosuser + "@" + host)
                    logger.error("---->4STARTING THREAD for " + thisosuser + "@" + host)
　
                    #for thisout in out:
                        #print "out---->" + thisout + "\n"
　
                    serv = None
　
                    if out is not None:
                        serv = out[0]
                        output = out[1]
                        showmessage = out[2]
                        showmsg = out[3]
　
                except:
                    print(traceback.format_exc())
　
                    logger.error("---->Thread Exception.")
                    pass
　
                #serv, output, showmessage, showmsg = envScanFunction(host, type, thisosuser, "webentry")
                try:
                    logger.error("---->" + type + " Env Scan:" + serv.name + ":\n")
                    logger.error("---->" + type + " Env Scan output:" + showmsg + ":\n")
                except:
                    logger.error("---->" + type + " Env Scan Print Exception.")
                    pass
　
                if serv is not None:
                    success = True
                else:
                    issue_text = issue_text + "Issue Scanning Server: " + output + " " + showmessage + " " + showmsg
                    logger.error("---->scan fail: " + issue_text)
            else:
                if check_val == 1:
                    logger.error("---->KEY CHECK: Check was NOT successful (passwd) for " + thisosuser + "@" + host + "--" + str(success))
                elif check_val == 3:
                    logger.error("---->KEY CHECK: Check was NOT successful (timeout) for " + thisosuser + "@" + host + "--" + str(success))
                else:
                    logger.error("---->KEY CHECK: Check was NOT successful (inconclusive) for " + thisosuser + "@" + host + "--" + str(success))
　
　
        if success:
            app_db = ""
            app_exists = False
　
            try:
                app = app.replace(" ", "-")
                app_name = app + "-" + type
                app_found = Application.objects.filter(appcode=app_name)
                if app_found.exists():
                    app_exists = True
                    app_db = app_found[0]
            except:
                issue = True
                issue_text = "Problem with app in DB"
                pass
　
            if not app_exists:
                app_db = Application(appcode=app_name, alternatename=app_name + " (registered)", description="N/A", email="N/A", created_by="webentry")
                app_db.save()
            logger.error("---->App Creation" + app_name + "--" )
　
            rolecode_in = "APC"
　
            for thisuser in users:
                logger.error("----> User:" + thisuser)
                user = User.objects.get_or_create(username=thisuser)[0]
                user.save()
　
                role = Roles.objects.filter(code=rolecode_in)[0]
　
                if role is not None and user is not None and app_db is not None:
                    approle = ApplicationRoles.objects.filter(application=app_db).filter(role=role).filter(user=user)
　
                if not approle:
                    newrole = ApplicationRoles(application=app_db, user=user, role=role, created_by="webentry")
                    newrole.save()
　
                grpname = app_db.appcode
                grpname += '_appgroup'
                group = Group.objects.get_or_create(name=grpname)[0]
                group.save()
                logger.error("----> group created:" + grpname)
　
                group.user_set.add(user)
                group.save()
                assign_perm('Application.appdev', group, app_db)
                assign_perm('Application.appcontact', user, app_db)
                logger.error("----> perms assignedi. ")
　
　
            env_exists = False
            env_db = ""
            env_name = ""
            try:
                env_name = app + "_" + level + "_" + type
                logger.error("---->Env Name:" + env_name + ":<--")
                env_found = Environment.objects.filter(name=env_name.strip())
                if env_found.exists():
                    env_exists = True
                    env_db = env_found[0]
            except:
                issue = True
                issue_text = "Problem with env in DB"
                pass
　
            logger.error("---->Env Creation" + env_name + "--" + str(issue))
            if not env_exists:
                dc_cld = Datacenter.objects.get(datacenter=type)
                env_db = Environment(application=app_db, type=level.strip(), name=env_name.strip(), delivered=timezone.now(), datacenter=dc_cld, gsdqueue="N/A", created_by="webentry")
                env_db.save()
            else:
                env_db.type = level.strip();
                env_db.save();
　
            logger.error("---->Env Creation completed: " + env_name + "--" + str(issue))
            insts = ""
　
            if inst is not None and inst is not "":
                logger.error("----------INST FILTER INST>>>>> " + inst)
                insts = Instance.objects.filter(server__name=host).filter(name__contains=inst)
            else:
                logger.error("----------NO INST FILTER INST>>>>> ")
                insts = Instance.objects.filter(server__name=host)
　
            for thisinst in insts:
                logger.error("---->Env adding inst " + thisinst.name + "--")
                env_db.instances.add(thisinst)
                env_db.save()
            logger.error("---->Env Creation complete " + env_name + "--")
        else:
            issue = True
            issue_text = issue_text + "Problem with server in DB"
　
        return host, app_name, issue, issue_text
　
　
def accept_server(server):
    SSH_NEWKEY = 'to continue connecting'
　
    logger.error("---->!!Checking for Key Acceptance on " + server)
    logger.error("---->Checking hosts file for: " + server)
　
    ip = ""
    hostsfile = open(settings.HOST_FILE, "r")
    logger.error("---->Hosts File Opened")
    server_search = server + " "
    for thisline in hostsfile:
        if server_search in thisline:
            logger.error("---->Entry in Hosts File found: " + thisline)
            ip = thisline.split()[1]
            logger.error("---->using IP: " + ip)
　
    if ip != "":
        server = ip
　
    cmd = '/usr/bin/ssh wasadm@' + server + ' uname -a'
    logger.error("---->Command being used: " + cmd)
    ssh = pexpect.spawn(cmd)
    time.sleep(1)
    retval = ssh.expect([SSH_NEWKEY, '[Pp]assword:', pexpect.EOF, pexpect.TIMEOUT], timeout=7)
    logger.error("---->XTDG before key: " + ssh.before + "\n")
    time.sleep(1)
　
    if retval == 0:
        logger.error("---->Key Accepting: " + ssh.before + "\n")
        ssh.sendline('yes')
        time.sleep(1)
        ssh.expect(['[Pp]assword: ', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        logger.error("---->Key Accepted: " + ssh.before + "\n")
    elif retval == 1:
        logger.error("---->Key Check - Password Prompt: " + ssh.before + "\n")
    elif retval == 2:
        logger.error("---->Key Check - EOF during SSH: " + ssh.before + "\n")
        time.sleep(2)
        logger.error("---->attempting to accept key anyway: " + ssh.before + "\n")
        ssh.sendline('yes')
        time.sleep(2)
        ssh.expect(['[Pp]assword: ', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
    elif retval == 3:
        logger.error("---->Key Check - Timeout executing command: " + ssh.before + "\n")
    else:
        logger.error("---->Key Check - Key Already Accepted: " + ssh.before + "\n")
　
    ssh.close(force=True)
    return retval
　
　
def chk_key(user, server):
    if "auto" in user:
        return 3
　
    SSH_NEWKEY = 'continue connecting'
　
    logger.error("---->Checking for Key Acceptance on " + server)
　
    logger.error("---->Checking hosts file for: " + server)
　
    ip = ""
    hostsfile = open(settings.HOST_FILE, "r")
    server_search = server + " "
    for thisline in hostsfile:
        if server_search in thisline:
            logger.error("---->Entry in Hosts File found: " + thisline)
            ip = thisline.split()[1]
            logger.error("---->using IP: " + ip)
　
    if ip != "":
        server = ip
　
    cmd = '/usr/bin/ssh -q -t -t -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + user + '@' + server + ' "ls -l"'
    logger.error("---->Command being used: " + cmd)
    ssh = pexpect.spawn(cmd)
    logger.error("---->spawned: " + cmd)
    retval = ssh.expect([SSH_NEWKEY, '[Pp]assword:', pexpect.EOF, pexpect.TIMEOUT], 'total', timeout=30)
    logger.error("---->XTDG before key: " + ssh.before + "\n")
    time.sleep(1)
　
    if retval == 0:
        logger.error("---->Key Accepting: " + ssh.before + "\n")
        ssh.sendline('yes')
        time.sleep(1)
        newret = ssh.expect(['[Pp]assword: ', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        logger.error("---->Key Accepted: " + ssh.before + "\n")
        ssh.close(force=True)
        return newret
    elif retval == 1:
        logger.error("---->Key Check - Password Prompt: " + ssh.before + "\n")
    elif retval == 2:
        logger.error("---->Key Check - EOF during SSH: " + ssh.before + "\n")
    elif retval == 3:
        logger.error("---->Key Check - Timeout executing command: " + ssh.before + "\n")
    elif retval == 4:
        logger.error("---->Key Check - Connected " + ssh.before + "\n")
        retval = 1
    else:
        logger.error("---->Key Check - Key Already Accepted: " + ssh.before + "\n")
　
    ssh.close(force=True)
    return retval
　
　
def threaded(f):
    import Queue
　
    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)
　
    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''
　
        q = Queue.Queue()
　
        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.start()
        t.result_queue = q
        return t
　
    return wrap
　
　
@threaded
def envScanWrapper(host, type, thisosuser):
    ret = []
    ret = envScanFunction(host, type, thisosuser, "webentry")
    return ret
　
