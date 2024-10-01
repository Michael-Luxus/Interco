from django.urls import path
from .views import tiers, listTiers, modif_Tiers

app_name = 'tiers'
urlpatterns = [
   path('tiers/', tiers, name='tiers'),

   path('tiers/listtiers/', listTiers, name='listTiers'),
   path('tiers/modif_Tiers/', modif_Tiers, name='modif_Tiers'),
]

