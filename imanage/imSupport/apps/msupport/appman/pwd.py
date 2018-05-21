import pwrecord
　
　
def getpwnam(user):
    if user == 'wasadm':
        pwrecord.pw_name = 'wasadm'
        pwrecord.pw_dir = '/home/wasadm/'
        pwrecord.pw_uid = '601'
        pwrecord.pw_gid = '601'
　
    return pwrecord
