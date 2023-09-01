from celery import shared_task
from account.models import CustomUser as User
from library.models import Transaction
from datetime import date, timedelta
from django.db.models import Sum

#membership daily cost
@shared_task
def cost():
    users = User.objects.values('id','membership','wallet')
    membership_cost = 10
    for i in users:
        user_id = i['id']
        membership = i['membership']
        wallet = i['wallet']
        if membership=='N':
            user = User.objects.get(id=user_id)
            last_month = date.today()-timedelta(days=30)
            last_2month = date.today()-timedelta(days=60)
            transaction_count = Transaction.objects.filter(user = user_id, date__range=(last_month,date.today())).count()
            spent_amount_sum  = Transaction.objects.filter(user = user_id, date__range=(last_2month,date.today())).aggregate(Sum('spent_amount'))['spent_amount__sum']
            if spent_amount_sum and spent_amount_sum>300:
                membership_cost = 0
                continue
            if transaction_count > 3:
                discount = membership_cost - (30/100)*membership_cost
                try:
                    user.wallet = wallet - discount
                    user.save()
                    continue
                except:
                    continue
            try:
                user.wallet = wallet - membership_cost
                user.save()
                continue
            except:
                continue

#membership expiration check
@shared_task
def membership():
    users = User.objects.filter(membership='V')
    for user in users:
        if user.expiration_date <= date.today():
            user.membership = 'N'
            user.save()