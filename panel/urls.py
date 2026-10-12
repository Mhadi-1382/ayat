
from django.urls import path
from panel import views

urlpatterns = [
    path('', view=views.panel, name='panel'),
    path('admin/user/create/', view=views.panel_admin_user_create, name='panel_admin_user_create'),
    path('admin/user/delete/<int:id>/', view=views.panel_admin_user_delete, name='panel_admin_user_delete'),
    path('admin/user/disable/<int:id>/', view=views.panel_admin_user_disable, name='panel_admin_user_disable'),
    path('admin/user/enable/<int:id>/', view=views.panel_admin_user_enable, name='panel_admin_user_enable'),

    path('notifications/create/<str:send_type>/', view=views.panel_notifications_create, name='panel_notifications_create'),
    path('notifications/delete/<int:id>/', view=views.panel_notifications_delete, name='panel_notifications_delete'),

    path('cultural_manager/request/', view=views.panel_cultural_manager_request, name='panel_cultural_manager_request'),
    path('admin/request/approved/<int:id>/<int:user_id>/', view=views.panel_cultural_admin_request_approved, name='panel_cultural_admin_request_approved'),
    path('admin/request/rejected/<int:id>/<int:user_id>/', view=views.panel_cultural_admin_request_rejected, name='panel_cultural_admin_request_rejected'),
    path('admin/request/delete/<int:id>/<int:user_id>/', view=views.panel_cultural_admin_request_delete, name='panel_cultural_admin_request_delete'),
    
    path('admin/university/delete/<int:id>/', view=views.panel_university_delete, name='panel_university_delete'),
    path('admin/university/disable/<int:id>/<int:id_uni>/<int:user_id>/', view=views.panel_university_disable, name='panel_university_disable'),
    path('admin/university/enable/<int:id>/<int:id_uni>/<int:user_id>/', view=views.panel_university_enable, name='panel_university_enable'),

    path('admin/categories/create/', view=views.panel_categories_content_create, name='panel_categories_content_create'),
    path('admin/categories/edit/<int:id>/', view=views.panel_categories_content_edit, name='panel_categories_content_edit'),
    path('admin/categories/delete/<int:id>/', view=views.panel_categories_content_delete, name='panel_categories_content_delete'),

    path('admin/quran/<int:id>/', view=views.panel_quran, name='panel_quran'),
    path('admin/quran/surah/edit/<int:id>/', view=views.panel_surah_edit, name='panel_surah_edit'),
    path('admin/quran/surah/delete/<int:id>/', view=views.panel_surah_delete, name='panel_surah_delete'),
    path('admin/quran/ayah/edit/<int:surah_id>/<int:id>/', view=views.panel_ayah_edit, name='panel_ayah_edit'),
    path('admin/quran/ayah/delete/<int:surah_id>/<int:id>/', view=views.panel_ayah_delete, name='panel_ayah_delete'),

    path('admin/duas/<int:id>/', view=views.panel_dua, name='panel_dua'),
    path('admin/duas/create/', view=views.panel_dua_create, name='panel_dua_create'),
    path('admin/duas/edit/<int:id>/', view=views.panel_dua_edit, name='panel_dua_edit'),
    path('admin/duas/delete/<int:id>/', view=views.panel_dua_delete, name='panel_dua_delete'),

    path('admin/hadiths/<int:id>/', view=views.panel_hadith, name='panel_hadith'),
    path('admin/hadiths/create/', view=views.panel_hadith_create, name='panel_hadith_create'),
    path('admin/hadiths/edit/<int:id>/', view=views.panel_hadith_edit, name='panel_hadith_edit'),
    path('admin/hadiths/delete/<int:id>/', view=views.panel_hadith_delete, name='panel_hadith_delete'),

    path('cultural_event/create/', view=views.panel_cultural_event_create, name='panel_cultural_event_create'),
    path('cultural_event/edit/<int:id>/', view=views.panel_cultural_event_edit, name='panel_cultural_event_edit'),
    path('cultural_event/delete/<int:id>/', view=views.panel_cultural_event_delete, name='panel_cultural_event_delete'),
    
    path('admin/lifestyle_quran/<int:id>/', view=views.panel_lifestyle_quran, name='panel_lifestyle_quran'),
    path('admin/lifestyle_quran/create/', view=views.panel_lifestyle_quran_create, name='panel_lifestyle_quran_create'),
    path('admin/lifestyle_quran/edit/<int:id>/', view=views.panel_lifestyle_quran_edit, name='panel_lifestyle_quran_edit'),
    path('admin/lifestyle_quran/delete/<int:id>/', view=views.panel_lifestyle_quran_delete, name='panel_lifestyle_quran_delete'),

    path('admin/categories_ahkam/create/', view=views.panel_categories_ahkam_create, name='panel_categories_ahkam_create'),
    path('admin/categories_ahkam/edit/<int:id>/', view=views.panel_categories_ahkam_edit, name='panel_categories_ahkam_edit'),
    path('admin/categories_ahkam/delete/<int:id>/', view=views.panel_categories_ahkam_delete, name='panel_categories_ahkam_delete'),
    path('admin/ahkam/<int:id>/', view=views.panel_ahkam, name='panel_ahkam'),
    path('admin/ahkam/create/', view=views.panel_ahkam_create, name='panel_ahkam_create'),
    path('admin/ahkam/edit/<int:id>/', view=views.panel_ahkam_edit, name='panel_ahkam_edit'),
    path('admin/ahkam/delete/<int:id>/', view=views.panel_ahkam_delete, name='panel_ahkam_delete'),

    path('user_point/update/main/', view=views.update_user_point_main, name='update_user_point_main'),
    path('user_point/update/surah/', view=views.update_user_point_surah, name='update_user_point_surah'),
    path('user_point/update/dua/', view=views.update_user_point_dua, name='update_user_point_dua'),
    path('user_point/update/zekar_counter/step/1/', view=views.update_user_point_zekar_counter_step_1, name='update_user_point_zekar_counter_step_1'),
    path('user_point/update/zekar_counter/step/2/', view=views.update_user_point_zekar_counter_step_2, name='update_user_point_zekar_counter_step_2'),
    path('user_point/update/zekar_counter/step/3/', view=views.update_user_point_zekar_counter_step_3, name='update_user_point_zekar_counter_step_3'),
]
