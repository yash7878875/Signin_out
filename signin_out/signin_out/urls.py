"""
URL configuration for signin_out project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from register.views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenBlacklistView

# TokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('otp-verify/', verify_otp.as_view(), name='OTP Verify'),
    path('login/', LoginView.as_view(), name='Login'),
    path('ChangePasswordAPI/', ChangePasswordAPI.as_view(), name='Change Password'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
