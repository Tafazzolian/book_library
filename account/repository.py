from .models import CustomUser as User

class Session:
    @staticmethod
    def Raw_Session(request):
        raw_session = request.session
        return raw_session
    
    @staticmethod
    def Register_Session(request,cd, code, otp_created, count, ban):
        request.session['user_register_info']= {
        'phone':cd['phone'],
        'full_name':cd['full_name'],
        'password':cd['password'],
        'email':cd['email'],
        'otp':code,
        'otp_time':otp_created,
        'count':count,
        'ban':ban,
        }
        request.session.save()

    @staticmethod
    def Login_Session(request,cd, code, otp_created, count, ban):
        request.session['user_login_info']= {
        'username':cd['user_name'],
        'password':cd['password'],
        'otp':code,
        'otp_time':otp_created,
        'count':count,
        'ban':ban,
        }
        request.session.save()

class CreateUser:
    @staticmethod
    def User_Create(user_session):
        User.objects.create_user(user_session['phone'],
        user_session['email'],
        user_session['full_name'],
        user_session['password'])
        return User
