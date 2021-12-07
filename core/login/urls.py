from django.urls import path

from core.login.views import *

app_name = 'login'

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]