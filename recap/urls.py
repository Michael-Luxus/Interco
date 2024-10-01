from django.urls import path
from .views import recap
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recap'
urlpatterns = [
    
    path('recap/', recap, name='recap'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
