
from django.urls import path
from api import views

urlpatterns = [
    path('surahs/', view=views.surahs, name='surahs'),
    path('surahs/details/<int:id>/', view=views.surah_details, name='surah_details'),
    path('duas/', view=views.duas, name='duas'),
    path('duas/details/<int:id>/', view=views.dua_details, name='dua_details'),
    path('hadiths/', view=views.hadiths, name='hadiths'),
    path('hadiths/details/<int:id>/', view=views.hadith_details, name='hadith_details'),
    path('lifestyle-quran/', view=views.lifestyle_quran, name='lifestyle_quran'),
    path('lifestyle-quran/details/<int:id>/', view=views.lifestyle_quran_details, name='lifestyle_quran_details'),
    path('ahkam/', view=views.ahkam, name='ahkam'),

    path('ai/<str:prompt>/', view=views.ai, name='ai'),
]
