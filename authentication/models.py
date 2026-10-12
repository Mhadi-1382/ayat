from django.db import models
from django.contrib.auth.models import AbstractUser
from persiantools.jdatetime import JalaliDateTime

class CustomeUser(AbstractUser):
    ROLE_USERS = [
        ('admin', 'admin'),
        ('cultural_admin', 'cultural_admin'),
        ('student', 'student')
    ]
    EDUCATIONAL_LEVELS = [
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکترا', 'دکترا'),
        ('سایر', 'سایر'),
    ]

    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    date_joined = None
    last_login = None

    username = models.CharField(max_length=200, verbose_name='username')
    phone = models.CharField(max_length=11, verbose_name='phone', unique=True, error_messages={'unique': 'یک کاربر با این شماره وجود دارد.'})
    national_code = models.CharField(max_length=10, verbose_name='national code', unique=True, error_messages={'unique': 'این کدملی قبلاً استفاده شده است.'}, null=True, blank=True)
    student_code = models.CharField(max_length=14, verbose_name='student code', unique=True, error_messages={'unique': 'این شماره دانشجویی قبلاً استفاده شده است.'}, null=True, blank=True)
    field_student = models.CharField(max_length=50, verbose_name='field student', null=True, blank=True)
    educational_level = models.CharField(max_length=50, choices=EDUCATIONAL_LEVELS, verbose_name='educational level', null=True, blank=True)
    university_id = models.ForeignKey('panel.Universities', on_delete=models.CASCADE, verbose_name='university id', null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_USERS, default=ROLE_USERS[2], verbose_name='role')
    total_points = models.BigIntegerField(verbose_name='total_points', default=0, null=True, blank=True)
    bale_chat_id = models.CharField(max_length=30, verbose_name='bale_chat_id', unique=True, blank=True, null=True)
    created_at = models.CharField(max_length=50, default=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), verbose_name='created at')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.username + ' ' + f'({self.phone})'
