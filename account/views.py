from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,VerifyCodeForm, LoginForm, VerifyCodeForm2
import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib import messages
from datetime import timedelta, datetime
import pytz
from django.contrib.auth import authenticate, get_user_model , login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import requests

User = get_user_model()
utc = pytz.UTC

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000,9999)
            send_otp_code(cd['phone'],random_code)
            otp_created = datetime.now().isoformat()
            request.session['user_register_info'] = {
                'phone': cd['phone'],
                'email':cd['email'],
                'full_name':cd['full_name'],
                'password':cd['password'],
                'otp':random_code,
                'otp_time':otp_created,
            }
            messages.success(request,'we sent you a code','success')
            return redirect('account:verify_code')
        return render(request, self.template_name ,{'form':form})



class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'account/verify.html'
    #utc = pytz.UTC

    def get(self,request):
        form = self.form_class
        user_session = request.session['user_register_info']
        code = user_session['otp']
        return render(request,self.template_name,{'form':form,'code':code})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = request.session['user_register_info']
        code = user_session['otp']
        otp_sent_time_raw = user_session['otp_time']
        otp_sent_time = datetime.fromisoformat(otp_sent_time_raw)
        otp_expire_time = (otp_sent_time + timedelta(minutes=1))#.replace(tzinfo=utc)
        now = datetime.now()#.replace(tzinfo=utc)
        
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code and otp_expire_time > now :
                User.objects.create_user(user_session['phone'],
                                         user_session['email'],
                                         user_session['full_name'],
                                         user_session['password'])
                user = authenticate(request, phone=user_session['phone'], password=user_session['password'])
                if isinstance(user, User):
                    login(request, user)
                    messages.success(request,'registration success','success')
                    return redirect('library:home')
            else:
                messages.error(request,'Expired or wrong code! - pls find UserRegisterverify View and add or remove utc = pytz.UTC','danger')
                return redirect('account:verify_code')
        return redirect('library:home')


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request,'already logged in')
            return redirect('library:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone=cd['user_name'], password = cd['password'])
            if user:
                random_code = random.randint(1000, 9999)
                otp_created = datetime.now().isoformat()
                send_otp_code(cd['user_name'], random_code)
                request.session['user_login_info']= {
                    'username':cd['user_name'],
                    'password':cd['password'],
                    'otp':random_code,
                    'otp_time':otp_created,
                }
                return redirect('account:verify_code_login')
            elif User.objects.filter(phone=cd['user_name']).exists():
                messages.error(request, 'Wrong Pass', 'warning')
                return redirect('account:User_Login')
            messages.error(request, 'User not found!', 'warning')
            return redirect('account:User_Login')
        messages.error(request, 'invalid form info!')
        return redirect('account:User_Login')



class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm2
    template_name = 'account/loginverify.html'
    #utc = pytz.UTC

    def get(self,request):
        code = request.session['user_login_info']
        form = self.form_class
        return render(request,self.template_name,{'form':form,'code':code['otp']})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = request.session['user_login_info']
        otp_sent_time_raw = user_session['otp_time']
        otp_sent_time = datetime.fromisoformat(otp_sent_time_raw)
        otp_expire_time = (otp_sent_time + timedelta(minutes=1)).replace(tzinfo=utc)
        now = datetime.now().replace(tzinfo=utc)
        user = authenticate(request, phone=user_session['username'], password=user_session['password'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == user_session['otp'] and otp_expire_time > now:
                login(request, user)
                messages.success(request, 'welcome!','success')
                return redirect('library:home')
            else:
                messages.error(request,'Expired or wrong code! pls find UserLoginverify View and add or remove utc = pytz.UTC','danger')
                return redirect('account:verify_code_login')
        return redirect('library:home')


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.info(request,'Bye!')
        return redirect('library:home')

class LoginApiView(APIView):

    def get(self,request):
        return Response('This is the login API - Dont import anythin for POST - Data = {phone:1507, password:admin,otp:otp} - Just press POST')

    def post(self, request, *args, **kwargs):
        otp = random.randint(1000, 9999)
        data = {'phone':1507, 'password':'admin','otp':otp}
        send_otp_code(data['phone'], otp)
        if data['otp'] == otp:
            print(otp,'OTP verified')
        user = User.objects.get(phone= data['phone'])
        if user:
            refresh = RefreshToken.for_user(user)
            link = 'http://127.0.0.1:8000'
            login(request, user)
            return Response({
                'message': 'JWT token created',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'Go back to site':link,
            })
        else:
            return Response('Invalid OTP', status=400)