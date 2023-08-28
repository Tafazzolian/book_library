from django.core.management.base import BaseCommand
from .models import CustomUser as User

class Command(BaseCommand):
    def task(self, *args, **options):
        users = User.objects.values('id','membership')
        for i in users:
            user_id = i['id']
            membership = i['membership']
            if membership=='N':
                user = User.objects.get(id=user_id)
                user.update_wallet(repeat = 365)
                print('done')