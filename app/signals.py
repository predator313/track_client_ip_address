from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
@receiver(user_logged_in,User)
def login_success(sender,request,user,**kwargs):
    ip=request.Meta.get('REMOTE_ADDR')
    request.session['ip']=ip