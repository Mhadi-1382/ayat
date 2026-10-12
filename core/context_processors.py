from panel.models import Universities, Notifications, UserPoints
from authentication.models import CustomeUser
from django.db.models import Sum
    
def app_version(request):
    return {'APP_VERSION': '1.0.1'}

def university_list(request):
    if request.user.is_authenticated:
        data = Universities.objects.defer('id', 'university_name', 'is_verified').all()
        return {'university_list': data}
    else:
        return {'university_list': []}

def notifications_list(request):
    if request.user.is_authenticated:
        data_uni = []
        data_system = []
        data_system_admin = []
        data_system_user = []
        for item in Notifications.objects.defer('user_id', 'title', 'body', 'url_action', 'user_type_sending', 'created_at').all():
            if item.user_id.role == 'cultural_admin' and item.user_id.university_id == request.user.university_id:
                data_uni.append(item,)
            elif item.user_id.role == 'admin' and (item.send_type == 'system' or item.send_type == 'combined'):
                data_system.append(item,)
            elif item.user_id == request.user and item.user_type_sending == 'admin' and item.send_type == 'system_user':
                data_system_user.append(item,)
        if request.user.role == 'admin':
            for item in Notifications.objects.defer('title', 'body', 'url_action', 'user_type_sending', 'send_type', 'created_at').all():
                if item.send_type == 'system_admin' and item.user_type_sending == 'admin':
                    data_system_admin.append(item,)
        return {'notifications_list_uni': data_uni, 'notifications_list_system': data_system, 'notifications_list_system_user': data_system_user, 'notifications_list_system_admin': data_system_admin}
    else:
        return {'notifications_list': []}

def user_total_points(request):
    if request.user.is_authenticated:
        if request.user.role == 'cultural_admin' or request.user.role == 'student':
            sum_total_points_uni = UserPoints.objects.filter(user_id__university_id=request.user.university_id).defer('point').aggregate(Sum('point'))['point__sum'] or 0
            
            return {'total_points_uni': sum_total_points_uni}
        else:
            if request.user.university_id:
                sum_total_points = UserPoints.objects.filter(user_id=request.user).aggregate(Sum('point'))['point__sum'] or 0
                CustomeUser.objects.filter(id=request.user.id).update(total_points=sum_total_points)

            return {'total_points_user': []}
    else:
        return {'user_total_points': []}
