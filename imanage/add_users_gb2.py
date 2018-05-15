from django.contrib.auth.models import User, Group
　
import logging
　
　
print "Initializing Group...\n"
　
region = 'GB'
grpname = region
grpname += '_engineers'
　
group = Group.objects.get_or_create(name=grpname)[0]
group.save()
　
print grpname + " initialized.\n"
　
user_list = ['user1', 'user2', 'user3', 'user4', 'user5']
　
for thisuser in user_list:
    print "Creating user: " + thisuser + "\n"
    user = User.objects.get_or_create(username=thisuser)[0]
    user.save()
    print "User " + thisuser + " created\n"
    group.user_set.add(user)
    group.save()
    print "User " + thisuser + " added to group\n"
