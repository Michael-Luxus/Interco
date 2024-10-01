from django.urls import path
from .views import gap

app_name = 'gap'
urlpatterns = [
   path('gap/', gap, name='gap'),
]