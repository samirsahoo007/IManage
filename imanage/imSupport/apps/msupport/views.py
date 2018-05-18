from django.conf import settings
from django.http import HttpResponse
from django.template import loader, RequestContext
from imSupport.apps.msupport.models import Application, Environment, Instance
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
import os.path
import logging
　
@login_required
def home(request):
    logger = logging.getLogger('django.request')
　
    request.session.set_expiry(1800)
　
    motd = ""
　
    outdata = {}
    eng_region = []
    is_engineer = False
　
    try:
        if os.path.isfile(settings.MOTD_FILE):
            f = open(settings.MOTD_FILE,"r")
            motd = f.read()
            f.close()
    except:
        logger.error("here---->" + settings.MOTD_FILE)
        pass
    for g in request.user.groups.all():
        if "_engineers" in g.name:
            is_engineer = True
            eng_region.append(g.name.split("_")[0])
　
    if is_engineer:
        for thisreg in eng_region:
            instlist = Instance.objects.filter(e2active="ACT").filter(region__region=thisreg)[:50]
            insts = list(instlist)
            envs = Environment.objects.filter(instances__in=insts).distinct()
　
            for thisenv in envs:
                env_good = False
                thisinstlist = thisenv.instances.all()[:30]
                for thisinst in thisinstlist:
                    if thisinst.region.region == thisreg:
                        env_good = True
                if env_good:
　
                    thisapp = Application.objects.filter(appcode=thisenv.application.appcode)[0]
                    if envs.count():
                        outdata.setdefault(thisapp.appcode, []).append(thisenv)
    else:
        apps = get_objects_for_user(request.user, 'appdev', Application)[:50]
　
        for thisapp in apps:
            envs = Environment.objects.distinct().filter(instances__e2active="ACT").filter(application__appcode=thisapp.appcode)[:50]
            envs = envs.select_related()
            for thisenv in envs:
                thisapp = Application.objects.filter(appcode=thisenv.application.appcode)[0]
                if envs.count():
                    outdata.setdefault(thisapp.appcode, []).append(thisenv)
    template = loader.get_template('msupport/index.html')
　
    context = RequestContext(request, {
        'mye2': "true",
        'data': outdata,
        'motd': motd,
        })
　
    return HttpResponse(template.render(context))
　
def tester(request):
    logger = logging.getLogger('django.request')
    logger.error("Tester Called")
　
    instlist = Instance.objects.filter(name="DNATEST")
    template = loader.get_template('msupport/tester.html')
    logger.error("Tester Succes" + str(len(instlist)))
　
    context = RequestContext(request, {
        'mye2': "true",
        'data': instlist,
        })
　
    return HttpResponse(template.render(context))
　
