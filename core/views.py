from django.shortcuts import render, get_object_or_404, redirect
from .models import Surahs, Ayahs, Duas, Hadiths, LifestyleQuran, CategoriesContent, Ahkam, CategoriesAhkam
from panel.models import Universities, CulturalEvents
from authentication.models import CustomeUser
from secrets import choice

def main(request):
    try:
        hadiths_random = choice(Hadiths.objects.all())
    except:
        hadiths_random = ''
    return render(request, template_name='pages/index.html', context={'hadith': hadiths_random})

def surahs(request):
    return render(request, template_name='pages/content/surahs/index.html', context={'surahs': Surahs.objects.defer('id', 'name_ar', 'name_fa', 'total_ayah')})
def surah_details(request, slug):
    if get_object_or_404(Surahs, id=slug):
        return render(request, template_name='pages/content/surahs/details.html', context={'ayah_details': Ayahs.objects.filter(surah_id=slug).all(), 'surah_details': Surahs.objects.filter(id=slug).first()})

def duas(request):
    return render(request, template_name='pages/content/duas/index.html', context={'duas': Duas.objects.defer('id', 'title')})
def dua_details(request, slug):
    if get_object_or_404(Duas, id=slug):
        return render(request, template_name='pages/content/duas/details.html', context={'duas_details': Duas.objects.filter(id=slug).first()})

def hadiths(request):
    return render(request, template_name='pages/content/hadiths/index.html', context={'hadiths': Hadiths.objects.defer('id', 'text_ar', 'text_fa', 'source'), 'categories_content': CategoriesContent.objects.defer('id', 'title').all()})

def cultural_events(request):
    if request.user.is_authenticated and request.user.university_id:
        return render(request, template_name='pages/content/cultural-events/index.html', context={'univercity': Universities.objects.filter(university_name=request.user.university_id.university_name).first(), 'cultural_events': CulturalEvents.objects.filter(university_id=request.user.university_id).all()})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def lifestyle_quran(request):
    return render(request, template_name='pages/content/lifestyle-quran/index.html', context={'lifestyle_quran': LifestyleQuran.objects.all(), 'categories_content': CategoriesContent.objects.defer('id', 'title').all()})

def challenge(request):
    if request.user.is_authenticated and request.user.university_id and request.user.role == 'student':
        return render(request, template_name='pages/content/challenge/index.html', context={
            'university_rank': CustomeUser.objects.filter(
                university_id=request.user.university_id,
                role='student',
                total_points__gt=request.user.total_points
            ).count() + 1,
            'university_total': CustomeUser.objects.filter(
                university_id=request.user.university_id,
                role='student'
            ).count(),
            'overall_rank': CustomeUser.objects.filter(
                role='student',
                total_points__gt=request.user.total_points
            ).count() + 1,
            'overall_total': CustomeUser.objects.filter(role='student').count()})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

def ahkam(request):
    return render(request, template_name='pages/content/ahkam/index.html', context={'ahkam': Ahkam.objects.all(), 'categories_ahkam': CategoriesAhkam.objects.defer('id', 'title').all()})

def relax_room(request):
    return render(request, template_name='pages/single-pages/relax-room/index.html', context={})

def maktab_haj_qasem(request):
    return render(request, template_name='pages/single-pages/maktab-haj-qasem/index.html', context={})

def maktab_emam_khamenei(request):
    return render(request, template_name='pages/single-pages/maktab-emam-khamenei/index.html', context={})

def exam_yar(request):
    return render(request, template_name='pages/single-pages/exam-yar/index.html', context={})

def ramadhan_yar(request):
    return render(request, template_name='pages/single-pages/ramadhan-yar/index.html', context={})

def recitation_path(request):
    return render(request, template_name='pages/content/recitation-path/index.html', context={})

def cultural_challenges(request):
    return render(request, template_name='pages/content/cultural-challenges/index.html', context={})

def cultural_calender(request):
    return render(request, template_name='pages/content/cultural-calender/index.html', context={})

def dl(request):
    return render(request, template_name='pages/landing/dl.html', context={})
