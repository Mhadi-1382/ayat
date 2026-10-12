from core.models import Surahs, Ayahs, Duas, Hadiths, LifestyleQuran, Ahkam
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from persiantools.jdatetime import JalaliDateTime
from secrets import choice

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def surahs(request):
    try:
        data = []
        for item in Surahs.objects.all():
            data.append({'id': item.id, 'name_fa': item.name_fa, 'name_ar': item.name_ar, 'total_ayah': item.total_ayah, 'reciter_name': item.reciter_name, 'audio_url': item.audio_url})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def surah_details(request, id):
    try:
        data = []
        for item in Ayahs.objects.filter(surah_id__id=id):
            data.append({'id': item.id, 'surah_id': item.surah_id.id, 'surah_name': item.surah_id.name_fa, 'ayah_number': item.ayah_number, 'text_ar': item.text_ar, 'text_fa': item.text_fa})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def duas(request):
    try:
        data = []
        for item in Duas.objects.all():
            data.append({'id': item.id, 'title': item.title})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def dua_details(request, id):
    try:
        data = []
        for item in Duas.objects.filter(id=id):
            data.append({'id': item.id, 'title': item.title, 'text_full': item.text_full, 'reciter_name': item.reciter_name, 'audio_url': item.audio_url})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def hadiths(request):
    try:
        data = []
        for item in Hadiths.objects.all():
            data.append({'id': item.id, 'text_ar': item.text_ar, 'text_fa': item.text_fa, 'source': item.source})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def hadith_details(request, id):
    try:
        data = []
        for item in Hadiths.objects.filter(id=id):
            data.append({'id': item.id, 'text_ar': item.text_ar, 'text_fa': item.text_fa, 'source': item.source})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def lifestyle_quran(request):
    try:
        data = []
        for item in LifestyleQuran.objects.all():
            data.append({'id': item.id, 'title': item.title, 'arabic': item.arabic, 'translation': item.translation, 'source': item.source, 'analysis': item.analysis, 'challenge_action': item.challenge_action})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def lifestyle_quran_details(request, id):
    try:
        data = []
        for item in LifestyleQuran.objects.filter(id=id):
            data.append({'id': item.id, 'title': item.title, 'arabic': item.arabic, 'translation': item.translation, 'source': item.source, 'analysis': item.analysis, 'challenge_action': item.challenge_action})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)

@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def ahkam(request):
    try:
        data = []
        for item in Ahkam.objects.all():
            data.append({'id': item.id, 'question': item.question, 'answer': item.answer, 'source': item.source, 'category_ahkam': item.category_ahkam_id.title})
    
        return JsonResponse(data=data, safe=False)
    except Exception as e:
        return JsonResponse(data={'error': e}, safe=False)


@csrf_exempt
@ratelimit(key='ip', rate='20/m', block=True)
def ai(request, prompt: str):
    data = []
    hour = JalaliDateTime.now().hour
    if 5 <= hour < 12:
        time_greeting = "صبح بخیر"
    elif 12 <= hour < 17:
        time_greeting = "ظهر بخیر"
    elif 17 <= hour < 21:
        time_greeting = "عصر بخیر"
    else:
        time_greeting = "شب بخیر"

    try:
        if prompt == 'سلام' or prompt == 'دستیار آیت' or prompt == 'آیت سلام':
            if request.user.is_authenticated:
                data.append({
                    'response': choice([f'سلام حالت خوبه {request.user.username} عزیز! از دستورات زیر یکی رو انتخاب کن.', f'سلام {request.user.username} عزیز! حالت چطوره؟ 🌸', f'سلام {request.user.username} عزیز! خوشحالم که اینجایی 🌷', f'درود بر {request.user.username} عزیز! امروز چطور می‌تونم کمکت کنم؟ 💫', f'سلام {request.user.username} عزیز! بفرمایید 🌸', f'سلام {request.user.username} عزیز! چه استرسی داری امروز بگو کمکت کنم 😎', f'{time_greeting} {request.user.username} عزیز! 🌸']),
                })
            else:
                data.append({
                    'response': choice(['سلام حالت خوبه دوست عزیز! از دستورات زیر یکی رو انتخاب کن.', 'سلام دوست عزیز! حالت چطوره؟ چه کمکی از دستم برمیاد؟ 🌸', 'سلام دوست عزیز! خوشحالم که اینجایی 🌷', 'درود بر تو! امروز چطور می‌تونم کمکت کنم؟ 💫', 'سلام عزیز! بفرمایید 🌸', 'سلام! چه استرسی داری امروز بگو کمکت کنم 😎', f'{time_greeting} دوست عزیز! 🌸']),
                })
        elif prompt == 'خداحافظ' or prompt == 'خدانگهدار' or prompt == 'بای' or prompt == 'فعلا':
            if request.user.is_authenticated:
                data.append({
                    'response': choice([f'به امید دیدار {request.user.username} عزیز ✋', f'به امید دیدار دوباره {request.user.username} عزیز! خوش باشی ✋', f'به امید دیدار {request.user.username} عزیز! موفق باشی ✨', 'خدانگهدار عزیزم! یادت نره همیشه امید داشته باشی 🌸', f'باشه {request.user.username} عزیز! به امید یه روز خوب دیگه 🌟']),
                })
            else:
                data.append({
                    'response': choice(['به امید دیدار دوست عزیز ✋.', 'به امید دیدار دوباره! خوش باشی ✋', 'به امید دیدار! موفق باشی ✨', 'خدانگهدار عزیزم! یادت نره همیشه امید داشته باشی 🌸', 'باشه! به امید یه روز خوب دیگه 🌟']),
                })
        elif prompt == 'چطوری' or prompt == 'حالت چطوره' or prompt == 'چه خبر' or prompt == 'خوبی':
            if request.user.is_authenticated:
                data.append({
                    'response': choice([f'ممنون {request.user.username} عزیز! من که همیشه آماده کمکم. تو چطوری؟ 😊', f'عالیَم {request.user.username} عزیز! تو بگو چه خبر؟ 🌸', f'الحمدلله خوبم {request.user.username} عزیز! تو چراغی؟ 🤗', f'همین که تو اینجایی {request.user.username} عزیز، منم خوبم! 💫'])
                })
            else:
                data.append({
                    'response': choice(['ممنون! من که همیشه آماده کمکم. تو چطوری؟ 😊', 'عالیَم! تو بگو چه خبر؟ 🌸', 'الحمدلله خوبم! تو چراغی؟ 🤗', 'همین که تو اینجایی، منم خوبم! 💫'])
                })
        elif prompt == 'ممنون' or prompt == 'مرسی' or prompt == 'تشکر' or prompt == 'دمت گرم':
            if request.user.is_authenticated:
                data.append({
                    'response': choice([f'خواهش میکنم {request.user.username} عزیز! خوشحالم که تونستم کمک کنم 🤗', f'قابل نداره {request.user.username} عزیز! هر وقت نیاز بود من هستم 🌸', f'مرسی از لطفت {request.user.username} عزیز! این دلگرمی من برای بهتر کمک کردنه 💫', f'خواهش میکنم {request.user.username} عزیز! تو که همیشه خوشحالی من رو بیشتر میکنی 😊'])
                })
            else:
                data.append({
                    'response': choice(['خواهش میکنم عزیز! خوشحالم که تونستم کمک کنم 🤗', 'قابل نداره! هر وقت نیاز بود من هستم 🌸', 'مرسی از لطفت! این دلگرمی من برای بهتر کمک کردنه 💫', 'خواهش میکنم! تو که همیشه خوشحالی من رو بیشتر میکنی 😊'])
                })
        elif prompt == 'تو کی هستی' or prompt == 'چه کاری ازت بر میاد' or prompt == 'قابلیت ها':
            data.append({
                'response': choice(['من دستیار آیت هستم! می‌تونم بهت آیات قرآن، احادیث، جملات انگیزشی و راهکارهای سبک زندگی رو بگم 🤗', 'سلام! من آیت هستم، دستیار هوشمند قرآنی. می‌تونم بهت کمک کنم استرس کم کنی، انگیزه بگیری، یا یه آیه قشنگ بهت بگم 🌸', 'من یه ربات دوستانه هستم که برات از قرآن و نهج‌البلاغه و صحیفه سجادیه محتوای کاربردی میارم 💫'])
            })
        elif prompt == 'راهنما' or prompt == 'دستورات':
            data.append({
                'response': choice(['📋 دستورات موجود: <br />- دستیار آیت / سلام / آیت سلام<br />- چطوری / حالت چطوره / چه خبر / خوبی<br />- مرسی / تشکر / دمت گرم / ممنون<br />- خداحافظ / خدانگهدار / فعلا / بای<br />- چه کاری ازت بر میاد / قابلیت ها / تو کی هستی<br />- دستورات / راهنما<br />- درباره آیت / آیت / درباره اپلیکیشن<br /><br />🌸 هر سوالی که در زیر قرار داره رو میتونم جواب بدم!'])
            })
        elif prompt == 'درباره آیت' or prompt == 'آیت' or prompt == 'درباره اپلیکیشن':
            data.append({
                'response': choice(['<a href="javascript:modal('"'about'"');" draggable="false" class="flex w-fit"><button class="go-surah-btn py-2 px-4 bg-slate-100 cursor-pointer text-xs text-slate-600 rounded-full">برای کسب اطلاعات درباره آیت — ضربه بزن</button></a>'])
            })
        else:
            data_choice_random_ayah = choice(Ayahs.objects.filter(category_content_id__title=prompt))
            data_choice_random_hadith = choice(Hadiths.objects.filter(category_content_id__title=prompt))
            data_choice_random_lifestylequran = choice(LifestyleQuran.objects.filter(category_content_id__title=prompt))
            data.append({
                'suggestion_ayah': {'surah_id_id': data_choice_random_ayah.surah_id.id, 'surah_id_name_fa': data_choice_random_ayah.surah_id.name_fa, 'ayah_number': data_choice_random_ayah.ayah_number, 'text_ar': data_choice_random_ayah.text_ar, 'text_fa': data_choice_random_ayah.text_fa},
                'suggestion_hadith': {'text_ar': data_choice_random_hadith.text_ar, 'text_fa': data_choice_random_hadith.text_fa, 'source': data_choice_random_hadith.source},
                'suggestion_lifestylequran': {'title': data_choice_random_lifestylequran.title, 'arabic': data_choice_random_lifestylequran.arabic, 'translation': data_choice_random_lifestylequran.translation, 'source': data_choice_random_lifestylequran.source, 'analysis': data_choice_random_lifestylequran.analysis, 'challenge_action': data_choice_random_lifestylequran.challenge_action}
            })
    except:
        if request.user.is_authenticated:
            data.append({
                'error': choice([f'{request.user.username} عزیز! متأسفانه پاسخی برای این سوال ندارم. میتوانید سوال دیگری بپرسید؟ 🙏', f'{request.user.username} عزیز! هنوز جواب این یکی را یاد نگرفته‌ام. چیز دیگری بپرسم؟ 😊', f'{request.user.username} عزیز! فعلاً دانش من در این مورد کم است. سوال بعدی؟ 🚀', 'پیداش نکردم! شاید با عبارت دیگری بپرسید؟ 🔍', 'از عهده‌ی این سوال برنیامدم. دستم خالی است! 🌸']),
            })
        else:
            data.append({
                'error': choice(['متأسفانه پاسخی برای این سوال ندارم. میتوانید سوال دیگری بپرسید؟ 🙏', 'هنوز جواب این یکی را یاد نگرفته‌ام. چیز دیگری بپرسم؟ 😊', 'فعلاً دانش من در این مورد کم است. سوال بعدی؟ 🚀', 'پیداش نکردم! شاید با عبارت دیگری بپرسید؟ 🔍', 'از عهده‌ی این سوال برنیامدم. دستم خالی است! 🌸']),
            })

    return JsonResponse(data, safe=False)
