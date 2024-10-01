from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from .redirec import rederect_to_login, myRederectAdminLogoutFunction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', myRederectAdminLogoutFunction, name='logout'),
    path('accounts/', include('authentification.urls')),
    path('', rederect_to_login),

    path('', include('home.urls')),
    path('', include('detail.urls')),
    path('', include('recap.urls')),
    path('', include('grandlivre.urls')),
    path('', include('tiers.urls')),
    path('', include('gap.urls')),



    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
