from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomeUser

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            tel = request.POST.get('tel')
            password = request.POST.get('password')

            if CustomeUser.objects.filter(phone=tel).exists():
                messages.error(request, 'این شماره تماس قبلاً استفاده شده است.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                create_user = CustomeUser.objects.create_user(username=username, password=password, phone=tel, role='student')
                create_user.save()

                login(request, create_user)
                messages.info(request, '{0} عزیز سلام، به پلتفرم هوشمند انس با قرآن آیت خوش اومدی 🎉'.format(username))
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            tel = request.POST.get('tel')
            password = request.POST.get('password')

            try:
                user_check = CustomeUser.objects.get(phone=tel)
                if user_check.is_active:
                    if user_check.check_password(password):
                        if user_check.role == 'admin':
                            login(request, user_check)
                            messages.success(request, 'مدیر عزیز سلام، به پنل مدیریت خوش اومدی 🎉')
                            return redirect('/panel/')
                        elif user_check.role == 'cultural_admin':
                            login(request, user_check)
                            messages.success(request, f'{request.user.username} عزیز سلام، به پنل مدیریت خوش اومدی 🎉')
                            messages.info(request, f'{request.user.username} عزیز سلام، به پنل مدیریت خوش اومدی 🎉')
                            return redirect('/panel/')
                        else:
                            login(request, user_check)
                            messages.success(request, '{0} عزیز سلام، به پلتفرم هوشمند انس با قرآن آیت خوش اومدی 🎉'.format(request.user.username))
                            messages.info(request, '{0} عزیز سلام، به پلتفرم هوشمند انس با قرآن آیت خوش اومدی 🎉'.format(request.user.username))
                            return redirect(request.META.get('HTTP_REFERER', '/'))
                    else:
                        messages.error(request, 'رمز عبور شما اشتباه می باشد.')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.warning(request, 'اکانت شما غیرفعال است. لطفاً با پشتیبانی تماس بگیرید.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            except CustomeUser.DoesNotExist:
                messages.error(request, "کاربری با این شماره وجود ندارد.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

def profile_edit_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fullname = request.POST.get('username')
            email = request.POST.get('email')
            national_code = request.POST.get('national_code')
            student_code = request.POST.get('student_code')
            field_student = request.POST.get('field_student')
            educational_level = request.POST.get('educational_level')
            university_id = request.POST.get('university_id')

            user = CustomeUser.objects.filter(id=request.user.id)
            if user.exists():
                if CustomeUser.objects.filter(email=email).exclude(id=request.user.id).exists():
                    messages.error(request, 'این ایمیل قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                elif CustomeUser.objects.filter(national_code=national_code).exclude(id=request.user.id).exists():
                    messages.error(request, 'این کدملی قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                elif CustomeUser.objects.filter(student_code=student_code).exclude(id=request.user.id).exists():
                    messages.error(request, 'این شماره دانشجویی قبلاً استفاده شده است.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    user.update(username=fullname, email=email, national_code=national_code, student_code=student_code, field_student=field_student, educational_level=educational_level, university_id=university_id)

                    messages.success(request, 'ویرایش اطلاعات با موفقیت انجام شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, 'ویرایش اطلاعات با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def profile_edit_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password_current = request.POST.get('password_current')
            password_new = request.POST.get('password_new')

            try:
                user_check = CustomeUser.objects.get(id=request.user.id)
            except CustomeUser.DoesNotExist:
                messages.error(request, 'تغییر رمز عبور با مشکل مواجه شد.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                if not user_check.check_password(password_current):
                    messages.error(request, 'رمز عبور فعلی وارد شده با رمز عبور قبلیتان مطابقت ندارد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    user_check.set_password(password_new)
                    user_check.save()

                    messages.success(request, 'تغییر رمز عبور با موفقیت انجام شد.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
