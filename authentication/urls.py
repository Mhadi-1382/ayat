
from django.urls import path
from authentication import views

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('signin/', view=views.signin, name='signin'),
    path('signout/', view=views.signout, name='signout'),
    path('profile/edit/info/', view=views.profile_edit_info, name='profile_edit_info'),
    path('profile/edit/password/', view=views.profile_edit_password, name='profile_edit_password'),
]
