
from django.urls import path
from api_private import views

urlpatterns = [
    path('bale/webhook/', view=views.bale_webhook, name='bale_webhook'),
]
