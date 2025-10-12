from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # Authentification : connexion / déconnexion
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # Application principale : gestion_rh
    path('', include('gestion_rh.urls')),
]
