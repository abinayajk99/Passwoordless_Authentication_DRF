from email.message import Message
from multiprocessing import context
from django.conf import settings
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics, status, permissions
from urllib.parse import urljoin
from django.contrib.auth.models import User 
# Create your views here.
from .serializers import (
    UserSignupSerializer,
    UserSignInSerializer
)
from rest_framework.response import Response
from .models import (EmailRegister)
from Passworless_Authentication.response import GenericResponse
import requests,json
from drfpasswordless.models import CallbackToken
from django.core.mail import send_mail, EmailMessage
from Passworless_Authentication.settings  import EMAIL_HOST_USER
from django.template.loader import render_to_string, get_template
from django.template import Context
class SignupView(GenericAPIView):
    serializer_class = UserSignupSerializer
    template_name = "Message.html"
    # permission_classes = [
    #     IsAuthenticated,
    # ]

    # def get(self,request):
    #     user = User.objects.get(email=request.user.email)
    #     serializer = UserSignupSerializer(user)
    #     print(serializer.data)
    #     return GenericResponse(serializer.data)

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url = 'http://'+request.get_host()+'/auth/email/'
            request_obj = request.data
            data_dict = {'email':request_obj['email']}
            aa = requests.post(url,data=data_dict)
            Token = CallbackToken.objects.get(to_alias=request_obj['email'],is_active=True)
            user = User.objects.get(email=request_obj['email'])
            subject = 'This is form GST'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            link = 'http://'+request.get_host()+'/api/signin'+'?email='+user.email+'&token='+Token.key
            magic_link =  f"http://localhost:3000/magiclink/{Token.key}/{user.email}"
            Context = {'name':user.username,'link':link,"token":Token.key,"magic_link":magic_link}
            html_content = get_template(self.template_name).render(Context)
            try: 
                msg = EmailMessage(subject, html_content, email_from, recipient_list)
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send(fail_silently=True)
            except :
                return GenericResponse(
                success_msg="we are not able to send Email. please, verify",
                status=status.HTTP_200_OK,)

            return GenericResponse(
                success_msg="We have send a code to you email",
                status=status.HTTP_200_OK,
            )
        return GenericResponse(
            error_msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class SigninView(GenericAPIView):

    serializer_class = UserSignInSerializer

    def get(self,request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        print("----------->data",email,token)
        return GenericResponse(
            success_msg="We have fetched data successfully", status=status.HTTP_400_BAD_REQUEST
        )


    # def post(self,request,email,token):
    #     print(request.data)
    #     serializer = UserSignInSerializer(data=request.data)
    #     if serializer.is_valid():
    #         url = 'http://'+request.get_host()+'/auth/token/'
    #         data_dict = {'email':email,'token':token}
    #         aa = requests.post(url,data=data_dict)
    #         print("--------------------->aa",json.loads(aa.text))
    #         return GenericResponse(
    #         success_msg=json.loads(aa.text),
    #         status=status.HTTP_200_OK)

    #     return GenericResponse(
    #         error_msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )
    def post(self,request):
        print("REQUEST.DATA------------------------>",request.data)
        email = request.data.get('email')
        token = request.data.get('token')
        serializer = UserSignInSerializer(data=request.data)
        if serializer.is_valid():
            url = 'http://'+request.get_host()+'/auth/token/'
            data_dict = {'email':email,'token':token}
            aa = requests.post(url,data=data_dict)
            print("--------------------->aa",json.loads(aa.text))
            return GenericResponse(
            success_msg=json.loads(aa.text),
            status=status.HTTP_200_OK)

        return GenericResponse(
            error_msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


