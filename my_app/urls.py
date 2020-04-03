from django.urls import path
from my_app import views
# app_name='my_app'
urlpatterns=[
   path('',views.home,name='home'),
   path('new_search/',views.new_search,name='new_search'),
]
