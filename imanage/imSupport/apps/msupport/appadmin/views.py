from django.http import HttpResponse, HttpResponseRedirect
#from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from imSupport.apps.msupport.models import Application, ApplicationRoles
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from guardian.shortcuts import get_objects_for_user, get_users_with_perms
from imSupport.apps.msupport.audit import AuditObject
　
import grantForm
import logging
　
logger = logging.getLogger('django.request')
　
@login_required
def home(request):
　
    request.session.set_expiry(1800)
    template = loader.get_template('msupport/appadmin.html')
　
    apps = ApplicationRoles.objects.filter(user=request.user).filter(role__code="APC")
    apps.select_related()
    userperms = {}
　
    for app in apps:
        thisapp = app.application
        userwp = get_users_with_perms(thisapp, attach_perms=True)
        userperms[app.application] = userwp
　
    context = RequestContext(request, {
        'apc': request.user,
        'appadmin': "true",
        'userperms': userperms,
        })
　
    return HttpResponse(template.render(context))
　
　
@login_required
def grant_view(request):
    request.session.set_expiry(1800)
    app = request.GET['Application']
    form = grantForm.grantForm(initial={'userName': ''})
　
    template = loader.get_template('msupport/appadmin_grant.html')
　
    context = RequestContext(request, {
        'appadmin': "true",
        'Application': app,
        'form': form,
        })
    return HttpResponse(template.render(context))
　
　
@login_required
def grant_action(request):
    request.session.set_expiry(1800)
    thisapp = request.POST['Application']
    uid = request.POST['userName']
    logger.error("------>UID GRANT: " + uid)
    err = 0
　
    if ',' in uid:
        uids = uid.split(',')
        for thisuid in uids:
            thiserr = 0
            thiserr = do_grant_action(thisapp, thisuid, request.user, request.user.username)
            if thiserr == 1:
                err = 1
    else:
        err = do_grant_action(thisapp, uid, request.user, request.user.username)
　
    return HttpResponseRedirect('/appadmin/')
　
　
def do_grant_action(thisapp, uid, requser, requsername):
　
    apps = ApplicationRoles.objects.filter(user=requser).filter(role__code="APC")
    apps.select_related()
　
    for app in apps:
        workingapp = app.application
        if workingapp.appcode == thisapp:
            grpname = workingapp.appcode
            grpname += '_appgroup'
            logger.error("------>UID GRANT: " + grpname)
            group = Group.objects.get_or_create(name=grpname)[0]
            group.save()
            user = User.objects.get_or_create(username=uid)[0]
            user.save()
            logger.error("------>UID GRANT: " + str(user))
　
            group.user_set.add(user)
            group.save()
            logger.error("------>UID GRANT: " + str(group))
            a = AuditObject()
            a.recordAction("AppAdmin Granted Access", None, None, workingapp, uid, requsername)
def grant_api(thisapp, uid, admin):
    logger.error("------>UID GRANT: " + uid + " " + thisapp)
　
#    apps = get_objects_for_user(request.user, 'appcontact', Application)
    apps = Application.objects.filter(appcode=thisapp)
　
    for app in apps:
        workingapp = app
        if workingapp.appcode == thisapp:
            grpname = workingapp.appcode
            grpname += '_appgroup'
            logger.error("------>UID GRANT: " + grpname)
            group = Group.objects.get_or_create(name=grpname)[0]
            group.save()
            user = User.objects.get_or_create(username=uid)[0]
            user.save()
            logger.error("------>UID GRANT: " + str(user))
　
            group.user_set.add(user)
            group.save()
            logger.error("------>UID GRANT: " + str(group))
            a = AuditObject()
            a.recordAction("AppAdmin Granted Access", None, None, workingapp, uid, admin)
            return True
    return False
　
　
　
@login_required
def revoke(request):
    request.session.set_expiry(1800)
    thisapp = request.GET['Application']
    uid = request.GET['uid']
　
    apps = get_objects_for_user(request.user, 'appcontact', Application)
    for app in apps:
        if app.appcode == thisapp:
            grpname = app.appcode
            grpname += '_appgroup'
            group = Group.objects.get_or_create(name=grpname)[0]
            group.save()
            user = User.objects.get_or_create(username=uid)[0]
            user.save()
　
            group.user_set.remove(user)
            group.save()
　
            a = AuditObject()
            a.recordAction("AppAdmin Revoked Access", None, None, app, uid, request.user.username)
　
    return HttpResponseRedirect('/appadmin/')
　
