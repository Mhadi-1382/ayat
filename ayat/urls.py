"""
URL configuration for ayat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('manage/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('core.urls')),
    path('panel/', include('panel.urls')),
    path('', include('ai.urls')),
    path('api/v1/', include('api.urls')),
    path('api/private/v1/', include('api_private.urls')),
    path('froala/', include('froala_editor.urls')),

    path('service-worker.js', serve, {'path': 'js/service-worker.js', 'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
