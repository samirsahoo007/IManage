from django.core import management
from django.contrib.auth.models import User, Group
from django.conf import settings
　
import logging
import threading
import sys
　
　
logger = logging.getLogger('django.request')
threading._DummyThread._Thread__stop = lambda x: 42
logger.error("Threading Fix Applied")
　
setadminflag = False
for thisarg in sys.argv:
    if thisarg == "runserver" or thisarg == "runfcgi":
        setadminflag = True
　
if setadminflag:
    grpname = "e2admins"
    group = Group.objects.get_or_create(name=grpname)[0]
    group.save()
　
    logger.error("Setting e2admins group...")
　
    for acct in settings.ADMIN_ACCOUNTS:
        if User.objects.filter(username=acct).count():
            logger.error("User already exists in DB: " + acct)
            user = User.objects.get(username=acct)
            logger.error("Obtaining user")
            if not user.is_superuser:
                logger.error("Recreating User")
                user.delete()
                em = acct + "@abcd.com"
                management.call_command('createsuperuser', interactive=False, username=acct, email=em)
                user = User.objects.get(username=acct)
                user.save()
                logger.error("Saved as admin")
                group.user_set.add(user)
                group.save()
                logger.error("Added user to group. ")
        else:
            try:
                logger.error("Adding admin acounts: " + acct)
                em = acct + "@abcd.com"
                management.call_command('createsuperuser', interactive=False, username=acct, email=em)
                logger.error("Added: " + acct)
                user = User.objects.get(username=acct)
                user.save()
                group.user_set.add(user)
                group.save()
                logger.error("Added user to group. ")
            except Exception as e:
                logger.error("Admin account already exists. " + str(e))
