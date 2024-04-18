from django.contrib import admin
from django.urls import path
from .views import landing_page,Company_list,Alllocations,dashboard,about

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('landing_page/', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('Company_list/', Company_list, name='Company_list'),
    path('Alllocations/<str:company_name>/',Alllocations, name='Alllocations'),
    
]
