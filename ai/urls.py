
from django.urls import path
from ai import views

urlpatterns = [
    path('ai/<str:prompt>/<str:secret_key>/', view=views.ai, name='ai'),
]
