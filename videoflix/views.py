from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from videoflix_backend import settings
from django.http import HttpResponseRedirect
from .tokens import generate_token



class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        myuser = User.objects.create_user(username = request.data.get("username"), 
                                        email= request.data.get("email"),
                                        password=request.data.get("password"))
        myuser.is_active = False
        myuser.save()
        
        subject = "Welcome to Our Django User Registration System"
        message = f"Hello !\n\nThank you for registering on our website. Please confirm your email address to activate your account.\n\nRegards,\nThe Django Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address"
        message2 = render_to_string('email_confirmation.html', {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': generate_token.make_token(myuser)
        })
      
        send_mail(email_subject, message2, from_email, to_list, fail_silently=False)
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address and activate your account.")
        
        
        return Response(
            {
            'user_id': myuser.pk,
            'email': myuser.email
            }
        )
        
def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
            
        if myuser is not None and generate_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            messages.success(request, "Your account has been activated")
            return HttpResponseRedirect('http://localhost:4200/login')
        else:
            messages.error(request, "Activation link is invalid!")
            return render(request, 'activation_failed.html')
        
