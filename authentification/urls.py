from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auths'
urlpatterns = [
    path('login/', views.LoginLDAP.as_view(), name='login'),
    path('logout/', views.logout_ldap, name='logout'),
   # path('profile/', views.profile, name='profile'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
