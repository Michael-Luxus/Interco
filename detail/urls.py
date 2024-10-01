from django.urls import path
from .views import detail, detail_Individuel, export_popup_to_xls


app_name = 'detail'
urlpatterns = [
   path('detail/', detail, name='detail'),
   path('individuel/', detail_Individuel, name='detail_Individuel'),
    path('export_popup_to_xls/', export_popup_to_xls, name='export_popup_to_xls')

]

