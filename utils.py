from kavenegar import *
import random

def send_otp_code(phone):
    random_code = random.randint(1000, 9999)
    #api = KavenegarAPI('****')
    #params = {'sender': '1000596446', 'receptor': phone_number, 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
    #response = api.sms_send(params)

    return random_code

def send_otp_code_2(phone, code):
    #api = KavenegarAPI('****')
    #params = {'sender': '1000596446', 'receptor': phone_number, 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
    #response = api.sms_send(params)
    pass