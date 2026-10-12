from django.http.response import JsonResponse
from core.models import Ayahs, Hadiths, LifestyleQuran
from secrets import choice
from persiantools.jdatetime import JalaliDateTime

hour = JalaliDateTime.now().hour
if 5 <= hour < 12:
    time_greeting = "صبح بخیر"
elif 12 <= hour < 17:
    time_greeting = "ظهر بخیر"
elif 17 <= hour < 21:
    time_greeting = "عصر بخیر"
else:
    time_greeting = "شب بخیر"


def ai(request, prompt: str, secret_key: str):
    data = []

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

    if secret_key == 'pIuZuvCoaDWWqyuBmSyUG9hrCVhDLpWEWsnTvGdNioRHOPLanfGysWIYttr8we46khk71gaTGpkF3IeJvS_dIqS3lbfHedX7Q2ksYi2eWDif5kn3UbinKQcbizomTaeAu6Zu0t0ZDN0GEJEQ03fEt-PU8025m_5PQuXXDZJNpETX9wtB5ighGEktqZyX9lR0-2dcyfsgWB4ZRv5YVu3fddIGIIjFBvGrEA9dH9s6mK6AUY-QeXW81fzsvajIpTOYhTJAV-bVpVgTpbLgTOTWhkJiLWMbgu6NC8DXTNLsE1yjZkV4ixfJaV2mCPmg7iW8XwEYoxhWIjzHIC0kKePNhFnwLt5GMzV2qYDThTz-c76igWCQ8E5K74Yp6M2Nxy2qp77x6b3caxvrEvhuZ5Xz3_TW0mpD05sKAtEE-z-KXFiYkwrON4ND--gKPm0NhLdwPifGUNTuTIS-cHuTiBrcKwiHjJ5yWuqrrjfHbhT-RPiLVlSw5fYhxbfB-bgVnz0ecQVZRjEAS8zYQY6LSsC0P5DRLtYdWb9ERn8XSCPSQRowdaYbPhK2-k9NHIebVLGFmMbr97w1BMVxddfZmo-iZrIavyxSsae68BI3q9Nf5PUfbHk_1FSffx82FhcTrA_XkSPn5Fe4xVK4KP33iVnZwNOq9Iw':
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([{'error': 'secret key invalid.'}], safe=False)
