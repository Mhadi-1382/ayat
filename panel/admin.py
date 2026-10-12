from django.contrib import admin
from .models import Notifications, CulturalManagerRequests, Universities, CulturalEvents, UserPoints

admin.site.register(Notifications)
admin.site.register(CulturalManagerRequests)
admin.site.register(Universities)
admin.site.register(CulturalEvents)
admin.site.register(UserPoints)
