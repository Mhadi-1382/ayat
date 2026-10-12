
from django.urls import path
from core import views

urlpatterns = [
    path('', view=views.main, name='main'),
    path('surahs/', view=views.surahs, name='surahs'),
    path('surahs/<str:slug>/', view=views.surah_details, name='surah_details'),
    path('duas/', view=views.duas, name='duas'),
    path('duas/<str:slug>/', view=views.dua_details, name='dua_details'),
    path('hadiths/', view=views.hadiths, name='hadiths'),
    path('cultural-events/', view=views.cultural_events, name='cultural_events'),
    path('lifestyle-quran/', view=views.lifestyle_quran, name='lifestyle_quran'),
    path('challenge/', view=views.challenge, name='challenge'),
    path('ahkam/', view=views.ahkam, name='ahkam'),
    path('relax-room/', view=views.relax_room, name='relax_room'),
    path('maktab-haj-qasem/', view=views.maktab_haj_qasem, name='maktab_haj_qasem'),
    path('maktab-emam-khamenei/', view=views.maktab_emam_khamenei, name='maktab_emam_khamenei'),
    path('exam-yar/', view=views.exam_yar, name='exam_yar'),
    path('ramadhan-yar/', view=views.ramadhan_yar, name='ramadhan_yar'),
    path('recitation-path/', view=views.recitation_path, name='recitation_path'),
    path('cultural-challenges/', view=views.cultural_challenges, name='cultural_challenges'),
    path('cultural-calender/', view=views.cultural_calender, name='cultural_calender'),
    path('dl/', view=views.dl, name='dl'),
]
