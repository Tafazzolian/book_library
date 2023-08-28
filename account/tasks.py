from celery import shared_task
from account.models import CustomUser as User

@shared_task
def handle():
    users = User.objects.values('id','membership','wallet')
    for i in users:
        user_id = i['id']
        membership = i['membership']
        wallet = i['wallet']
        if membership=='N':
            user = User.objects.get(id=user_id)
            try:
                user.wallet = wallet - 1
                user.save()
            except:
                continue