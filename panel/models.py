from django.db import models
from froala_editor.fields import FroalaField
from authentication.models import CustomeUser
from persiantools.jdatetime import JalaliDateTime

class Notifications(models.Model):
    USER_TYPE_SENDING = [
        ('admin', 'admin'),
        ('cultural_admin', 'cultural_admin'),
    ]
    SEND_TYPE = [
        ('system', 'system'),
        ('notification', 'notification'),
        ('combined', 'combined'),
        ('system_admin', 'system_admin'),
        ('system_user', 'system_user'),
    ]

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, verbose_name='user id')
    title = models.CharField(max_length=500, verbose_name='title')
    body = models.TextField(verbose_name='body')
    url_action = models.URLField(verbose_name='url action')
    user_type_sending = models.CharField(max_length=50, choices=USER_TYPE_SENDING, verbose_name='user type sending')
    send_type = models.CharField(max_length=50, choices=SEND_TYPE, verbose_name='send type')
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')

    def __str__(self):
        return self.title

class CulturalManagerRequests(models.Model):
    STATUS = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ]

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, verbose_name='user id')
    university_name = models.CharField(max_length=200, verbose_name='university name', unique=True)
    city = models.CharField(max_length=50, verbose_name='city')
    university_icon = models.ImageField(upload_to='universities/university_icons/', verbose_name='university icon')
    document_file = models.FileField(upload_to='universities/document_files/', verbose_name='document file')
    description = models.TextField(verbose_name='description')
    phone_cultural_admin = models.CharField(max_length=11, verbose_name='phone cultural admin')
    phone_university = models.CharField(max_length=11, verbose_name='phone university')
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0], verbose_name='status')
    admin_note = models.TextField(verbose_name='admin note')
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')
    reviewed_at = models.CharField(max_length=50, verbose_name='reviewed at')

    def __str__(self):
        return f'{self.id} ({self.user_id} - {self.university_name} - {self.city})'
class Universities(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    university_name = models.ForeignKey(CulturalManagerRequests, on_delete=models.CASCADE, verbose_name='university name')
    is_verified = models.BooleanField(default=True, verbose_name='is verified')
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')
    
    def __str__(self):
        return f'{self.id} - {self.university_name}'

class CulturalEvents(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    university_id = models.ForeignKey(Universities, on_delete=models.CASCADE, verbose_name='university id')
    title = models.CharField(max_length=500, verbose_name='title')
    description = FroalaField(verbose_name='description')
    event_date = models.CharField(max_length=50, verbose_name='event date')
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')
    
    def __str__(self):
        return f'{self.id} - {self.title} - ({self.university_id.university_name.university_name})'

class UserPoints(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, verbose_name='user id', null=True, blank=True)
    point = models.BigIntegerField(verbose_name='point', default=0)
    level = models.CharField(max_length=100, verbose_name='level', default=1, null=True, blank=True)
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')
