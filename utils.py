import kavenegar
import ghasedakpack
import random

class SMSSendingException(Exception):
    pass

def send_otp_code_1(phone):
    random_code = random.randint(1000, 9999)
    sms = ghasedakpack.Ghasedak("d7a5f32de92343c89568ae579d150d9438e14d1e0dae538b96065d1fc7221166")
    sms.send({'message':random_code, 'receptor' : phone, 'linenumber': '300002525'})
    print(sms.status({'id': 'messageId', 'type': '1'}))
    return random_code

def send_otp_code_2(phone):
    random_code = random.randint(1000, 9999)
    #api = KavenegarAPI('****')
    #params = {'sender': '1000596446', 'receptor': phone, 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
    #response = api.sms_send(params)
    raise SMSSendingException('Fialed to send code using Kavenegar')
    return random_code

def send_otp_code_3(phone):
    random_code = random.randint(1000, 9999)
    #api = KavenegarAPI('****')
    #params = {'sender': '1000596446', 'receptor': phone, 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
    #response = api.sms_send(params)
    return random_code

