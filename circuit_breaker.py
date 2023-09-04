import random
from datetime import datetime
from datetime import timedelta
from utils import send_otp_code_1, send_otp_code_2, send_otp_code_3

def otp_generator(cd):
    try:
        customer_number = cd['phone']
    except:
        customer_number = cd['user_name']
    otp_test = [send_otp_code_1, send_otp_code_2, send_otp_code_3]
    random.shuffle(otp_test)
    error_list = []
    block_time = datetime.now()
    code = None
    while code is None:
        for j in otp_test:
            count = error_list.count(j)
            if count > 3 and datetime.now()-block_time <= timedelta(minutes=30):
                otp_test = otp_test.remove(j)
                block_time = datetime.now()
            elif count > 3 and datetime.now()-block_time >= timedelta(minutes=30):
                otp_test = otp_test.append(j)
                block_time = datetime.now()
            
        for i in otp_test:
            try:
                code = i(customer_number)
                break
            except:
                error_list.append(i)
                continue
    return code