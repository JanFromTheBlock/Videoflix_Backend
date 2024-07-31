"""
URL configuration for videoflix_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from videoflix.views import LoginView, RegisterView, ResetPwView, SetNewPw, activate, activatepw


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('activatepw/<uidb64>/<token>', activatepw, name='activatepw'),
    path('reset_pw/', ResetPwView.as_view()),
    path('set_new_pw/', SetNewPw.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
