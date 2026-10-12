from django.db import models
from froala_editor.fields import FroalaField

class CategoriesContent(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.CharField(max_length=300, verbose_name='description', null=True, blank=True)

    def __str__(self):
        return f'Categories Content: {self.title}'

class Surahs(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name_ar = models.CharField(max_length=100, verbose_name='name arabic')
    name_fa = models.CharField(max_length=100, verbose_name='name farsi')
    total_ayah = models.BigIntegerField(verbose_name='total ayah')
    reciter_name = models.CharField(max_length=200, verbose_name='reciter name', null=True, blank=True)
    audio_url = models.URLField(verbose_name='audio url', null=True, blank=True, unique=True)

    def __str__(self):
        return f'Surah: {self.id}'
class Ayahs(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    surah_id = models.ForeignKey(Surahs, on_delete=models.CASCADE, verbose_name='surah id')
    ayah_number = models.BigIntegerField(verbose_name='ayah number')
    text_ar = FroalaField(verbose_name='text arabic')
    text_fa = FroalaField(verbose_name='text farsi')
    category_content_id = models.ForeignKey(CategoriesContent, on_delete=models.CASCADE, verbose_name='category content id', null=True, blank=True)

    def __str__(self):
        return f'Ayah: {self.id}'

class Duas(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200, verbose_name='title')
    text_full = FroalaField(verbose_name='text full')
    reciter_name = models.CharField(max_length=200, verbose_name='reciter name', null=True, blank=True)
    audio_url = models.URLField(verbose_name='audio url', null=True, blank=True, unique=True)
    category_content_id = models.ForeignKey(CategoriesContent, on_delete=models.CASCADE, verbose_name='category content id', null=True, blank=True)

    def __str__(self):
        return f'Dua: {self.title}'

class Hadiths(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text_ar = models.TextField(verbose_name='text arabic')
    text_fa = models.TextField(verbose_name='text farsi')
    source = models.CharField(max_length=200, verbose_name='source')
    category_content_id = models.ForeignKey(CategoriesContent, on_delete=models.CASCADE, verbose_name='category content id', null=True, blank=True)

    def __str__(self):
        return f'Hadith: {self.id}'

class LifestyleQuran(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.TextField(verbose_name='title')
    arabic = models.TextField(verbose_name='arabic')
    translation = models.TextField(verbose_name='translation')
    source = models.CharField(max_length=200, verbose_name='source')
    analysis = models.TextField(verbose_name='analysis')
    challenge_action = models.TextField(verbose_name='challenge_action')
    category_content_id = models.ForeignKey(CategoriesContent, on_delete=models.CASCADE, verbose_name='category content id', null=True, blank=True)

    def __str__(self):
        return f'Lifestyle Quran: {self.id} - {self.title}'

class CategoriesAhkam(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.CharField(max_length=300, verbose_name='description', null=True, blank=True)

    def __str__(self):
        return f'Categories Content: {self.title}'
class Ahkam(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.TextField(verbose_name='question')
    answer = FroalaField(verbose_name='answer')
    source = models.CharField(max_length=200, verbose_name='source')
    category_ahkam_id = models.ForeignKey(CategoriesAhkam, on_delete=models.CASCADE, verbose_name='category ahkam id', null=True, blank=True)

    def __str__(self):
        return f'Ahkam: {self.id}'
