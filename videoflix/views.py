from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from videoflix_backend import settings
from django.http import HttpResponseRedirect
from .tokens import generate_token
from django.shortcuts import redirect





class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '').lower()
        password = request.data.get('password', '')
        
        try:
            user = User.objects.get(username=username)
            
            if not user.is_active:
               return Response({'detail': 'Account is not activated. Please check your email.'}, status=status.HTTP_403_FORBIDDEN) 
        except User.DoesNotExist:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        username = request.data.get("username").lower()
        email = request.data.get("email")
        password = request.data.get("password")
        
        errors = self._validate_user(username, email)
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self._create_user(username, email, password)
        self._send_confirmation_email(request, user)
        
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address and activate your account.")
        
        return Response(
            {
                'user_id': user.pk,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )
    
    def _validate_user(self, username, email):
        """Überprüft, ob der Benutzername oder die E-Mail bereits existiert."""
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username ist bereits vergeben"
        if User.objects.filter(email=email).exists():
            errors['email'] = "E-Mail ist bereits vergeben"
        return errors
    
    def _create_user(self, username, email, password):
        """Erstellt einen neuen Benutzer mit den angegebenen Daten und setzt is_active auf False."""
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        return user
    
    def _send_confirmation_email(self, request, user):
        """Sendet eine Bestätigungs-E-Mail und eine Willkommensnachricht an den neuen Benutzer."""
        # Willkommensnachricht
        subject = "Welcome to Our Django User Registration System"
        message = (
            "Hello!\n\nThank you for registering on our website. "
            "Please confirm your email address to activate your account.\n\n"
            "Regards,\nThe Django Team"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        # Bestätigungs-E-Mail
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address"
        message2 = render_to_string('email_confirmation.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        send_mail(email_subject, message2, from_email, to_list, fail_silently=False)
        
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
            return HttpResponseRedirect('https://www.videoflix.janborcholt.de/register-succes')
        else:
            messages.error(request, "Activation link is invalid!")
            return render(request, 'activation_failed.html')

class ResetPwView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Email address not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            myuser = User.objects.get(email=email)
            
            current_site = get_current_site(request)
            email_subject = "Reset Your Password"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            message2 = render_to_string('email_reset_password.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
            })
      
            send_mail(email_subject, message2, from_email, to_list, fail_silently=False)
            return Response({"success": "Password reset email sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
def activatepw(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
            
        if myuser is not None and generate_token.check_token(myuser, token):
            mail =  myuser.email
            return redirect(f'https://www.videoflix.janborcholt.de/reset-password/{uidb64}/{mail}')
        else:
            messages.error(request, "Activation link is invalid!")
            return render(request, 'activation_failed.html')
        
        
class SetNewPw(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        newPw = request.data.get("pw")
        
        try:
            myuser = User.objects.get(email=email)
            myuser.set_password(newPw)
            myuser.save()
            return Response({"message": "Password updated successfully"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
           
