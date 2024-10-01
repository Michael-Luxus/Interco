from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import grandlivre, grandLivreSociete, download_grand_livre


app_name = 'grandlivre'
urlpatterns = [

    path('grandlivre/', grandlivre, name='grandlivre'),
    path('grandLivre/Societe/', grandLivreSociete, name='grandLivreSociete'),
    path('download/', download_grand_livre, name='download_grand_livre'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
