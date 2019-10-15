from django.test import TestCase
import ldap
from functools import wraps
from xpinyin import Pinyin
# Create your tests here.
def user_required():
    @wraps()
    def user(*arg,**kwargs):
        if email == "guest":
            return

#loginuser.objects.filter(username="admin").update(password=make_password("Bys123456"))

#ldapconn = ldap.initialize('ldap://auth.hpicorp.net:389')
#print(ldapconn.simple_bind_s('cn=renjie.wang@hp.com,OU=CN,OU=Asiapacific,OU=Users,OU=Accounts,DC=auth,DC=hpicorp,DC=net', "$4Rfv%5Tgb^6Yhn"))

