from django.urls import path
from .views import *
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
    path('get-slots/', get_available_slots, name='get_available_slots'),
    path('services/<str:service_name>/', service_detail, name='service_detail'),
    path('i18n/setlang/', set_language, name='set_language'),
]
