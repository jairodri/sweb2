from django.urls import path

from core.sweb.views.dashboard.views import DashboardView

app_name = 'homepage'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='index'),
]