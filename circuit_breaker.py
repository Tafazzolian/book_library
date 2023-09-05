import random
import json
from django.core.cache import cache
from datetime import datetime
from datetime import timedelta
from utils import send_otp_code_1, send_otp_code_2, send_otp_code_3

otp_test_main  = [send_otp_code_1, send_otp_code_2, send_otp_code_3]

def otp_generator(cd):
    global otp_test_main
    otp_test  = otp_test_main

    for i in otp_test:
        instance = {'blocked_time' : datetime.now().isoformat(), 'ban_statuse' : False}
        cache.set(i.__name__, instance)
        cache.set(i.__name__+'count',0)
        print(f'{i.__name__} saved in cahe')
        
    try:
        customer_number = cd['phone']
    except:
        customer_number = cd['user_name']

    random.shuffle(otp_test)
    code = None

    for i in otp_test:
        f_name = i.__name__
        otp_status = cache.get(f_name)
        blocked_time = datetime.fromisoformat(otp_status['blocked_time'])
        error_list = cache.get(f_name+'count')
        print('1')
        
        if error_list > 3:
            instance = {'blocked_time' : datetime.now().isoformat(), 'ban_statuse' : True}
            cache.set(f_name,instance)
            cache.set(f_name + 'count',0)
            otp_test = otp_test.remove(i)
            print('2')
            continue
            
        if otp_status['ban_statuse'] == True and datetime.now() - blocked_time <= timedelta(minutes=30):
            otp_test = otp_test.remove(i)
            print('3')
            continue

        if otp_status['ban_statuse'] ==  True and datetime.now() - blocked_time >= timedelta(minutes=30):
            instance = {'blocked_time' : datetime.now().isoformat(), 'ban_statuse' : False}
            cache.set(f_name,instance)
            print('4')
            continue
            

    while code is None:   
        for i in otp_test:
            try:
                code = i(customer_number)
                print('5')
                break
            except:
                cache.incr(i.__name__+'count')
                print('6')
                continue
    return code