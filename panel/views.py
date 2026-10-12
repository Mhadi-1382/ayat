from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import CustomeUser
from .models import Notifications, CulturalManagerRequests, Universities, CulturalEvents, UserPoints
from core.models import Surahs, Ayahs, Duas, Hadiths, CategoriesContent, LifestyleQuran, Ahkam, CategoriesAhkam
from django.contrib import messages
from .notification import config_notification
from persiantools.jdatetime import JalaliDateTime
from django.http.response import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from .email import send_mail as s_mail, settings
from .bale import send_bale_message

def panel(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return render(request, template_name='pages/panel/index.html', context={'users': CustomeUser.objects.all(), 'notifications': Notifications.objects.all(), 'cultural_manager_requests': CulturalManagerRequests.objects.all(), 'universities': Universities.objects.all(), 'categories_content': CategoriesContent.objects.all(), 'surahs': Surahs.objects.all(), 'duas': Duas.objects.all(), 'hadiths': Hadiths.objects.all(), 'lifestyle_quran': LifestyleQuran.objects.all(), 'categories_ahkam': CategoriesAhkam.objects.all(), 'ahkam': Ahkam.objects.all()})
        elif request.user.role == 'cultural_admin':
            return render(request, template_name='pages/panel/index.html', context={'univercity': Universities.objects.filter(university_name=request.user.university_id.university_name).first(), 'count_users_joined': int(len(CustomeUser.objects.filter(university_id=Universities.objects.filter(university_name=request.user.university_id.university_name).get())) - 1), 'notifications': Notifications.objects.filter(user_id=request.user, send_type='system').all(), 'cultural_event': CulturalEvents.objects.filter(university_id=request.user.university_id).all(), 'time': JalaliDateTime.now().strftime('%Y-%m-%d %H:%M'), 'users': CustomeUser.objects.filter(university_id=request.user.university_id).all()})
        else:
            if not request.user.university_id:
                return render(request, template_name='pages/panel/index.html', context={})
            else:
                data = []
                for item in Notifications.objects.all():
                    if item.user_id.university_id == request.user.university_id:
                        data.append(item,)
                return render(request, template_name='pages/panel/index.html', context={'univercity': Universities.objects.filter(university_name=request.user.university_id.university_name).first(), 'university_notifications': data, 'cultural_event': CulturalEvents.objects.filter(university_id=request.user.university_id).all()})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_admin_user_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                username = request.POST.get('username')
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                role = request.POST.get('role')
                email = request.POST.get('email')
                national_code = request.POST.get('national_code')
                student_code = request.POST.get('student_code')
                field_student = request.POST.get('field_student')
                educational_level = request.POST.get('educational_level')
                university_id = request.POST.get('university_id')

                if CustomeUser.objects.filter(phone=phone).exists():
                    messages.error(request, 'این شماره تماس قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                elif CustomeUser.objects.filter(email=email).exists():
                    messages.error(request, 'این ایمیل قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                elif CustomeUser.objects.filter(national_code=national_code).exists():
                    messages.error(request, 'این کدملی قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                elif CustomeUser.objects.filter(student_code=student_code).exists():
                    messages.error(request, 'این شماره دانشجویی قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    create_user = CustomeUser.objects.create_user(username=username, phone=phone, password=password, role=role, email=email, national_code=national_code, student_code=student_code, field_student=field_student, educational_level=educational_level, university_id=university_id)
                    create_user.save()

                    messages.success(request, f'ایجاد حساب با نام کاربری ({username}) با موفقیت انجام شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_admin_user_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if CustomeUser.objects.filter(id=id).delete():
                    messages.success(request, f'حساب با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف حساب با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_admin_user_disable(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if CustomeUser.objects.filter(id=id).update(is_active=False):
                    messages.success(request, f'حساب با شناسه ({id}) با موفقیت غیرفعال شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'غیرفعال سازی حساب با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_admin_user_enable(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if CustomeUser.objects.filter(id=id).update(is_active=True):
                    messages.success(request, f'حساب با شناسه ({id}) با موفقیت فعال شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'فعال سازی حساب با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_notifications_create(request, send_type: str):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            body = request.POST.get('body')
            url_action = request.POST.get('url_action')

            if request.user.role == 'admin':
                if send_type == 'system':
                    try:
                        Notifications.objects.create(user_id=request.user, title=title, body=body, url_action=url_action, user_type_sending='admin', send_type='system').save()
                        messages.success(request, 'ارسال اعلان (سیستمی) با موفقیت انجام شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    except:
                        messages.error(request, 'ارسال اعلان (سیستمی) با مشکل مواجه شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                elif send_type == 'notification':
                    try:
                        config_notification(title=title, content=body, link=url_action)
                        messages.success(request, 'ارسال (اعلان) با موفقیت انجام شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    except:
                        messages.error(request, 'ارسال (اعلان) با مشکل مواجه شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                elif send_type == 'combined':
                    try:
                        config_notification(title=title, content=body, link=url_action)
                        Notifications.objects.create(user_id=request.user, title=title, body=body, url_action=url_action, user_type_sending='admin', send_type='combined').save()
                        messages.success(request, 'ارسال اعلان (ترکیبی) با موفقیت انجام شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    except:
                        messages.error(request, 'ارسال اعلان (ترکیبی) با مشکل مواجه شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
            elif request.user.role == 'cultural_admin':
                if send_type == 'system':
                    try:
                        Notifications.objects.create(user_id=request.user, title=title, body=body, url_action=url_action, user_type_sending='cultural_admin', send_type='system').save()
                        messages.success(request, 'ارسال اعلان (سیستمی) با موفقیت انجام شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    except:
                        messages.error(request, 'ارسال اعلان (سیستمی) با مشکل مواجه شده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_notifications_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin' or request.user.role == 'cultural_admin':
                if Notifications.objects.filter(id=id).delete():
                    messages.success(request, f'اعلان با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف اعلان با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_cultural_manager_request(request):
    if request.user.is_authenticated and request.user.role == 'student':
        if request.method == 'POST':
            university_name = request.POST.get('university_name')
            city = request.POST.get('city')
            university_icon = request.FILES.get('university_icon')
            document_file = request.FILES.get('document_file')
            phone_cultural_admin = request.POST.get('phone_cultural_admin')
            phone_university = request.POST.get('phone_university')
            description = request.POST.get('description')

            try:
                try:
                    CMR = CulturalManagerRequests.objects.create(user_id=request.user, university_name=university_name, city=city, university_icon=university_icon, document_file=document_file, phone_cultural_admin=phone_cultural_admin, phone_university=phone_university, description=description, status='pending')
                    messages.success(request, 'درخواست شما با موفقیت ثبت شد.')
                    body_admin = f'''
                    <p>مدیر عزیز سلام،</p>
                    <p>درخواست ارتقا حساب (مسئول امور فرهنگی) با عنوان: <br> <strong>{university_name} - {request.user.username}</strong></p>
                    '''
                    Notifications.objects.create(user_id=request.user, title='1 درخواست جدید ارتقا حساب', body=body_admin, url_action='', user_type_sending='admin', send_type='system_admin')
                    body_user = f'''
                    <p>{request.user.username} عزیز سلام،</p>
                    <p>درخواست شما با موفقیت ثبت شد. طی 72 ساعت آینده بررسی و در صورت لزوم کارشناسان ما با شما تماس خواهند گرفت، همچنین جهت پیگیری وضعیت درخواست خود می‌توانید در بخش اعلانات آنرا مشاهده کنید.</p>
                    <p style="font-weight: bold;">وضعیت درخواست شما: {'درحال بررسی' if CMR.status == 'pending' else ''}</p>
                    <h4>با تشکر،<br>آیت پلتفرم هوشمند انس با قرآن
                    '''
                    Notifications.objects.create(user_id=request.user, title='درخواست ارتقا حساب (مسئول امور فرهنگی)', body=body_user, url_action='', user_type_sending='admin', send_type='system_user')
                except:
                    pass

                if request.user.email:
                    context = f'''
                    <div style='direction: rtl;'>
                        <div style="padding-bottom: 50px;">
                            <p>{request.user.username} عزیز سلام،</p>
                            <p>درخواست شما با موفقیت ثبت شد. طی 72 ساعت آینده بررسی و در صورت لزوم کارشناسان ما با شما تماس خواهند گرفت، همچنین جهت پیگیری وضعیت درخواست خود می‌توانید در بخش اعلانات آنرا مشاهده کنید.</p>
                        </div>
                        <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                    </div>
                    '''
                    context_admin = f'''
                    <div style='direction: rtl;'>
                        <div style="padding-bottom: 50px;">
                            <p>مدیر عزیز سلام،</p>
                            <p>درخواست ارتقا حساب (مسئول امور فرهنگی) با عنوان: <br> <strong>{university_name} - {request.user.username}</strong></p>
                        </div>
                        <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                    </div>
                    '''
                    s_mail(subject='درخواست ارتقا حساب (مسئول امور فرهنگی)', body='', html_context=context, to=[request.user.email])
                    s_mail(subject='1 درخواست جدید ارتقا حساب', body='', html_context=context_admin, to=[settings.DEFAULT_FROM_EMAIL])
                else:
                    pass

                if request.user.bale_chat_id:
                    context = f'''
                    {request.user.username} عزیز سلام،\n
                    درخواست ارتقا حساب (مسئول امور فرهنگی) شما با موفقیت ثبت شد. طی 72 ساعت آینده بررسی و در صورت لزوم کارشناسان ما با شما تماس خواهند گرفت، همچنین جهت پیگیری وضعیت درخواست خود می‌توانید در بخش اعلانات آنرا مشاهده کنید.\n
                    با تشکر، \nآیت پلتفرم هوشمند انس با قرآن
                    '''
                    send_bale_message(chat_id=int(request.user.bale_chat_id), text=context)
                else:
                    pass

                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, 'درخواست شما با مشکل مواجه شده است.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_cultural_admin_request_approved(request, id, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                admin_note = request.POST.get('admin_note')
                
                req = CulturalManagerRequests.objects.filter(id=id)
                req_university_name = CulturalManagerRequests.objects.get(id=id)
                if req.update(status='approved', admin_note=admin_note, reviewed_at=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M')):
                    try:
                        uni = Universities.objects.create(university_name=req_university_name)
                    except:
                        messages.error(request, f'مشکلی در ایجاد دانشگاه (واحد) بوجود آماده است.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    else:
                        CustomeUser.objects.filter(id=user_id).update(role='cultural_admin', university_id=uni.id)
                        u = CustomeUser.objects.only('username', 'email').get(id=user_id)
                        
                        try:
                            notify_user = f'''
                            <p>{u.username} عزیز سلام،</p>
                            <p>درخواست با شناسه ({id}) با موفقیت تایید شد.</p>
                            <p style="font-weight: bold;">وضعیت درخواست شما: {'تاییدشده' if req_university_name.status == 'approved' else ''}</p>
                            <h4>با تشکر،<br>آیت پلتفرم هوشمند انس با قرآن
                            '''
                            Notifications.objects.create(user_id=u, title='تایید درخواست', body=notify_user, url_action='', user_type_sending='admin', send_type='system_user')
                        except:
                            pass

                        if u.email:
                            context = f'''
                            <div style='direction: rtl;'>
                                <div style="padding-bottom: 50px;">
                                    <p>{u.username} عزیز سلام،</p>
                                    <p>درخواست با شناسه ({id}) با موفقیت تایید شد.</p>
                                    <p>{admin_note}</p>
                                </div>
                                <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                            </div>
                            '''
                            s_mail(subject='تایید درخواست', body='', html_context=context, to=[u.email])
                        else:
                            pass

                        if request.user.bale_chat_id:
                            context = f'''
                            {u.username} عزیز سلام،\n
                            درخواست با شناسه ({id}) با موفقیت تایید شد.\n
                            {admin_note}\n
                            با تشکر، \nآیت پلتفرم هوشمند انس با قرآن
                            '''
                            send_bale_message(chat_id=int(request.user.bale_chat_id), text=context)
                        else:
                            pass

                        messages.success(request, f'درخواست با شناسه ({id}) با موفقیت تایید شد.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'تایید درخواست با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_cultural_admin_request_rejected(request, id, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                admin_note = request.POST.get('admin_note')
                
                req = CulturalManagerRequests.objects.filter(id=id)
                req_university_name = CulturalManagerRequests.objects.get(id=id)
                if req.update(status='rejected', admin_note=admin_note, reviewed_at=JalaliDateTime.now().strftime('%Y-%m-%d %H:%M')):
                    u = CustomeUser.objects.only('username', 'email').get(id=user_id)

                    try:
                        notify_user = f'''
                        <p>{u.username} عزیز سلام،</p>
                        <p>درخواست با شناسه ({id}) رد شد.</p>
                        <p style="font-weight: bold;">وضعیت درخواست شما: {'ردشده' if req_university_name.status == 'rejected' else ''}</p>
                        <h4>با تشکر،<br>آیت پلتفرم هوشمند انس با قرآن
                        '''
                        Notifications.objects.create(user_id=u, title='رد درخواست', body=notify_user, url_action='', user_type_sending='admin', send_type='system_user')
                    except:
                        pass
                    
                    if u.email:
                        context = f'''
                        <div style='direction: rtl;'>
                            <div style="padding-bottom: 50px;">
                                <p>{u.username} عزیز سلام،</p>
                                <p>درخواست با شناسه ({id}) رد شد.</p>
                                <p>{admin_note}</p>
                            </div>
                            <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                        </div>
                        '''
                        s_mail(subject='رد درخواست', body='', html_context=context, to=[u.email])
                    else:
                        pass
                    if request.user.bale_chat_id:
                        context = f'''
                        {u.username} عزیز سلام،\n
                        درخواست با شناسه ({id}) رد شد.\n
                        {admin_note}\n
                        با تشکر، \nآیت پلتفرم هوشمند انس با قرآن
                        '''
                        send_bale_message(chat_id=int(request.user.bale_chat_id), text=context)
                    else:
                        pass

                    messages.success(request, f'درخواست با شناسه ({id}) با موفقیت رد شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'رد درخواست با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_cultural_admin_request_delete(request, id, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if CulturalManagerRequests.objects.filter(id=id).delete():
                    CustomeUser.objects.filter(id=user_id).update(role='student')
                    messages.success(request, f'درخواست با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف درخواست با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_university_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Universities.objects.filter(id=id).delete():
                    messages.success(request, f'دانشگاه با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف دانشگاه با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_university_disable(request, id, id_uni, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                admin_note = request.POST.get('admin_note')
                
                if Universities.objects.filter(id=id).update(is_verified=False) and CulturalManagerRequests.objects.filter(id=id_uni).update(admin_note=admin_note):
                    u = CustomeUser.objects.only('username', 'email').get(id=user_id)

                    try:
                        notify_user = f'''
                        <p>{u.username} عزیز سلام،</p>
                        <p>دانشگاه با شناسه ({id_uni}) غیرفعال شد.</p>
                        <h4>با تشکر،<br>آیت پلتفرم هوشمند انس با قرآن
                        '''
                        Notifications.objects.create(user_id=u, title='غیرفعالسازی دانشگاه', body=notify_user, url_action='', user_type_sending='admin', send_type='system_user')
                    except:
                        pass

                    if u.email:
                        context = f'''
                        <div style='direction: rtl;'>
                            <div style="padding-bottom: 50px;">
                                <p>{u.username} عزیز سلام،</p>
                                <p>دانشگاه با شناسه ({id_uni}) غیرفعال شد.</p>
                                <p>{admin_note}</p>
                            </div>
                            <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                        </div>
                        '''
                        s_mail(subject='غیرفعالسازی دانشگاه', body='', html_context=context, to=[u.email])
                    else:
                        pass

                    if request.user.bale_chat_id:
                        context = f'''
                        {u.username} عزیز سلام،\n
                        دانشگاه با شناسه ({id_uni}) غیرفعال شد.\n
                        {admin_note}\n
                        با تشکر، \nآیت پلتفرم هوشمند انس با قرآن
                        '''
                        send_bale_message(chat_id=int(request.user.bale_chat_id), text=context)
                    else:
                        pass

                    messages.success(request, f'دانشگاه با شناسه ({id}) با موفقیت غیرفعال شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'غیرفعال سازی دانشگاه با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_university_enable(request, id, id_uni, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                admin_note = request.POST.get('admin_note')
                
                if Universities.objects.filter(id=id).update(is_verified=True) and CulturalManagerRequests.objects.filter(id=id_uni).update(admin_note=admin_note):
                    u = CustomeUser.objects.only('username', 'email').get(id=user_id)

                    try:
                        notify_user = f'''
                        <p>{u.username} عزیز سلام،</p>
                        <p>دانشگاه با شناسه ({id_uni}) فعال شد.</p>
                        <h4>با تشکر،<br>آیت پلتفرم هوشمند انس با قرآن
                        '''
                        Notifications.objects.create(user_id=u, title='فعالسازی دانشگاه', body=notify_user, url_action='', user_type_sending='admin', send_type='system_user')
                    except:
                        pass

                    if u.email:
                        context = f'''
                        <div style='direction: rtl;'>
                            <div style="padding-bottom: 50px;">
                                <p>{u.username} عزیز سلام،</p>
                                <p>دانشگاه با شناسه ({id_uni}) فعال شد.</p>
                                <p>{admin_note}</p>
                            </div>
                            <h4>با تشکر، <br> <a href='https://ayat.chbkn.run/'>آیت پلتفرم هوشمند انس با قرآن</a>
                        </div>
                        '''
                        s_mail(subject='فعالسازی دانشگاه', body='', html_context=context, to=[u.email])
                    else:
                        pass

                    if request.user.bale_chat_id:
                        context = f'''
                        {u.username} عزیز سلام،\n
                        دانشگاه با شناسه ({id_uni}) فعال شد.\n
                        {admin_note}\n
                        با تشکر، \nآیت پلتفرم هوشمند انس با قرآن
                        '''
                        send_bale_message(chat_id=int(request.user.bale_chat_id), text=context)
                    else:
                        pass

                    messages.success(request, f'دانشگاه با شناسه ({id}) با موفقیت فعال شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'فعال سازی دانشگاه با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_categories_content_create(request):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            try:
                CategoriesContent.objects.create(title=title, description=description).save()
                messages.success(request, f'دسته بندی با عنوان ({title}) با موفقیت ایجاد شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ایجاد دسته بندی با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_categories_content_edit(request, id):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            try:
                CategoriesContent.objects.filter(id=id).update(title=title, description=description)
                messages.success(request, f'دسته بندی با عنوان ({title}) با موفقیت ویرایش شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ویرایش دسته بندی با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_categories_content_delete(request, id):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            if CategoriesContent.objects.filter(id=id).delete():
                messages.success(request, f'دسته بندی با شناسه ({id}) با موفقیت حذف شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, f'حذف دسته بندی با شناسه ({id}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_quran(request, id):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            if get_object_or_404(Surahs, id=id):
                return render(request, template_name='pages/panel/core/admin/quran/index.html', context={'surah': Surahs.objects.filter(id=id).first(), 'ayahs': Ayahs.objects.filter(surah_id=id).all(), 'categories_content': CategoriesContent.objects.all()})
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_surah_edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                name_ar = request.POST.get('name_ar')
                name_fa = request.POST.get('name_fa')
                total_ayah = request.POST.get('total_ayah')
                reciter_name = request.POST.get('reciter_name')
                audio_url = request.POST.get('audio_url')
                
                if Surahs.objects.filter(id=id).update(name_ar=name_ar, name_fa=name_fa, total_ayah=total_ayah, reciter_name=reciter_name, audio_url=audio_url):
                    messages.success(request, f'سوره با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش سوره با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ayah_edit(request, surah_id, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                ayah_number = request.POST.get('ayah_number')
                text_ar = request.POST.get('text_ar')
                text_fa = request.POST.get('text_fa')
                category_content_id = request.POST.get('category_content_id')
                
                if Ayahs.objects.filter(surah_id=surah_id, ayah_number=id).update(ayah_number=ayah_number, text_ar=text_ar, text_fa=text_fa, category_content_id=category_content_id):
                    messages.success(request, f'آیه با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش آیه با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_surah_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Surahs.objects.filter(id=id).delete():
                    messages.success(request, f'سوره با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف سوره با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ayah_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Ayahs.objects.filter(ayah_number=id).delete():
                    messages.success(request, f'آیه با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'حذف آیه با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_dua(request, id):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            if get_object_or_404(Duas, id=id):
                return render(request, template_name='pages/panel/core/admin/duas/index.html', context={'dua': Duas.objects.filter(id=id).first(), 'categories_content': CategoriesContent.objects.defer('id', 'title').all()})
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_dua_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                text_full = request.POST.get('text_full')
                title = request.POST.get('title')
                reciter_name = request.POST.get('reciter_name')
                audio_url = request.POST.get('audio_url')
                
                try:
                    Duas.objects.create(text_full=text_full, title=title, reciter_name=reciter_name, audio_url=audio_url)
                    messages.success(request, f'دعا با موفقیت ثبت شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                except:
                    messages.error(request, f'ثبت دعا با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_dua_edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                text_full = request.POST.get('text_full')
                title = request.POST.get('title')
                reciter_name = request.POST.get('reciter_name')
                audio_url = request.POST.get('audio_url')
                category_content_id = request.POST.get('category_content_id')
                
                if Duas.objects.filter(id=id).update(text_full=text_full, title=title, reciter_name=reciter_name, audio_url=audio_url, category_content_id=category_content_id):
                    messages.success(request, f'دعا با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش دعا با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_dua_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Duas.objects.filter(id=id).delete():
                    messages.success(request, f'دعا با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect('/panel')
                else:
                    messages.error(request, f'حذف دعا با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_hadith(request, id):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            if get_object_or_404(Hadiths, id=id):
                return render(request, template_name='pages/panel/core/admin/hadiths/index.html', context={'hadith': Hadiths.objects.filter(id=id).first(), 'categories_content': CategoriesContent.objects.defer('id', 'title').all()})
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_hadith_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                text_ar = request.POST.get('text_ar')
                text_fa = request.POST.get('text_fa')
                source = request.POST.get('source')

                try:
                    Hadiths.objects.create(text_ar=text_ar, text_fa=text_fa, source=source)
                    messages.success(request, f'حدیث با موفقیت ثبت شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                except Exception as e:
                    print(e)
                    messages.error(request, f'ثبت حدیث با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_hadith_edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                text_ar = request.POST.get('text_ar')
                text_fa = request.POST.get('text_fa')
                source = request.POST.get('source')
                category_content_id = request.POST.get('category_content_id')
                
                if Hadiths.objects.filter(id=id).update(text_ar=text_ar, text_fa=text_fa, source=source, category_content_id=category_content_id):
                    messages.success(request, f'حدیث با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش حدیث با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_hadith_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Hadiths.objects.filter(id=id).delete():
                    messages.success(request, f'حدیث با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect('/panel')
                else:
                    messages.error(request, f'حذف حدیث با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_cultural_event_create(request):
    if request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'cultural_admin'):
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            event_date = request.POST.get('event_date')

            try:
                CulturalEvents.objects.create(title=title, description=description, event_date=event_date, university_id=request.user.university_id).save()
                messages.success(request, f'رویداد با عنوان ({title}) با موفقیت ایجاد شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ایجاد رویداد با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_cultural_event_edit(request, id):
    if request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'cultural_admin'):
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            event_date = request.POST.get('event_date')

            try:
                CulturalEvents.objects.filter(id=id).update(title=title, description=description, event_date=event_date)
                messages.success(request, f'رویداد با عنوان ({title}) با موفقیت ویرایش شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ویرایش رویداد با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_cultural_event_delete(request, id):
    if request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'cultural_admin'):
        if request.method == 'POST':
            if CulturalEvents.objects.filter(id=id).delete():
                messages.success(request, f'رویداد با شناسه ({id}) با موفقیت حذف شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, f'حذف رویداد با شناسه ({id}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_lifestyle_quran(request, id):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            if get_object_or_404(LifestyleQuran, id=id):
                return render(request, template_name='pages/panel/core/admin/lifestyle-quran/index.html', context={'lifestyle_quran': LifestyleQuran.objects.filter(id=id).first(), 'categories_content': CategoriesContent.objects.defer('id', 'title').all()})
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_lifestyle_quran_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                title = request.POST.get('title')
                arabic = request.POST.get('arabic')
                translation = request.POST.get('translation')
                analysis = request.POST.get('analysis')
                challenge_action = request.POST.get('challenge_action')
                source = request.POST.get('source')

                try:
                    LifestyleQuran.objects.create(title=title, arabic=arabic, translation=translation, analysis=analysis, challenge_action=challenge_action, source=source)
                    messages.success(request, f'محتوای سبک زندگی با موفقیت ثبت شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                except Exception as e:
                    print(e)
                    messages.error(request, f'ثبت محتوای سبک زندگی با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_lifestyle_quran_edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                title = request.POST.get('title')
                arabic = request.POST.get('arabic')
                translation = request.POST.get('translation')
                analysis = request.POST.get('analysis')
                challenge_action = request.POST.get('challenge_action')
                source = request.POST.get('source')
                category_content_id = request.POST.get('category_content_id')
                
                if LifestyleQuran.objects.filter(id=id).update(title=title, arabic=arabic, translation=translation, analysis=analysis, challenge_action=challenge_action, source=source, category_content_id=category_content_id):
                    messages.success(request, f'محتوای سبک زندگی با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش محتوای سبک زندگی با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_lifestyle_quran_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if LifestyleQuran.objects.filter(id=id).delete():
                    messages.success(request, f'محتوای سبک زندگی با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect('/panel')
                else:
                    messages.error(request, f'حذف محتوای سبک زندگی با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def panel_categories_ahkam_create(request):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            try:
                CategoriesAhkam.objects.create(title=title, description=description).save()
                messages.success(request, f'دسته بندی با عنوان ({title}) با موفقیت ایجاد شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ایجاد دسته بندی با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_categories_ahkam_edit(request, id):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            try:
                CategoriesAhkam.objects.filter(id=id).update(title=title, description=description)
                messages.success(request, f'دسته بندی با عنوان ({title}) با موفقیت ویرایش شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except:
                messages.error(request, f'ویرایش دسته بندی با عنوان ({title}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_categories_ahkam_delete(request, id):
    if request.user.is_authenticated and request.user.role == 'admin':
        if request.method == 'POST':
            if CategoriesAhkam.objects.filter(id=id).delete():
                messages.success(request, f'دسته بندی با شناسه ({id}) با موفقیت حذف شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, f'حذف دسته بندی با شناسه ({id}) با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ahkam(request, id):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            if get_object_or_404(Ahkam, id=id):
                return render(request, template_name='pages/panel/core/admin/ahkam/index.html', context={'ahkam': Ahkam.objects.filter(id=id).first(), 'categories_ahkam': CategoriesAhkam.objects.defer('id', 'title').all()})
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ahkam_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                question = request.POST.get('question')
                answer = request.POST.get('answer')
                source = request.POST.get('source')

                try:
                    Ahkam.objects.create(question=question, answer=answer, source=source)
                    messages.success(request, f'احکام با موفقیت ثبت شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                except Exception as e:
                    print(e)
                    messages.error(request, f'ثبت احکام با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ahkam_edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                question = request.POST.get('question')
                answer = request.POST.get('answer')
                source = request.POST.get('source')
                category_ahkam_id = request.POST.get('category_ahkam_id')
                
                if Ahkam.objects.filter(id=id).update(question=question, answer=answer, source=source, category_ahkam_id=category_ahkam_id):
                    messages.success(request, f'احکام با شناسه ({id}) با موفقیت ویرایش شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, f'ویرایش احکام با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
def panel_ahkam_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.role == 'admin':
                if Ahkam.objects.filter(id=id).delete():
                    messages.success(request, f'احکام با شناسه ({id}) با موفقیت حذف شد.')
                    return redirect('/panel')
                else:
                    messages.error(request, f'حذف احکام با شناسه ({id}) با مشکل مواجه شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_main(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=1)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_surah(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=10)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_dua(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=10)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_zekar_counter_step_1(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=10)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_zekar_counter_step_2(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=50)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@ratelimit(key='ip', rate='1/d', block=True)
def update_user_point_zekar_counter_step_3(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student' and request.method == 'POST':
        try:
            UserPoints.objects.create(user_id=request.user, point=100)
            
            return JsonResponse(data=[{'status': True}], safe=False)
        except:
            return JsonResponse(data=[{'status': False}], safe=False)
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
