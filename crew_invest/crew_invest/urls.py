"""crew_invest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from app import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment, name='payment'),
    path('pay/', views.pay, name='pay'),
    
    path('login/',views.auth_login, name='auth_login'),
    path('signup/',views.signup, name='signup'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('profile/edit/',views.edit,name='edit'),
    path('', views.main, name='main'),
    path('stockpage/<str>/', views.stockpage, name='stockpage'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
