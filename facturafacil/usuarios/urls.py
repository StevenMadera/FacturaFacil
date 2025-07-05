from django.urls import path
from .views import registro_view, login_view, logout_view, perfil_view, HomeView

app_name = 'usuarios'

urlpatterns = [
    path('', HomeView.as_view(), name='inicio'),
    path('registro/', registro_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
]