from django.db import models
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
import uuid 
import datetime
import locale
from .mixins import SwahiliDateMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class Masomo(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    somo_la = models.CharField(max_length=20,verbose_name='SOMO')
    limetoka = models.CharField(max_length=20,verbose_name='LIMETOKA')
     
    def __str__(self):
        return self.somo_la.upper()  # Displays the name of the lesson
    
    class Meta:
        verbose_name="MASOMO YA LEO"
        verbose_name_plural = "MASOMO YA LEO"
    
class Announcement(SwahiliDateMixin,models.Model):
    weekday = models.CharField(max_length=20,verbose_name='SIKU YA JUMA', blank=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    matangazo = models.TextField(verbose_name='TANGAZO')

    def save(self):
        days = {
            "Monday": "Jumatatu",
            "Tuesday": "Jumanne",
            "Wednesday": "Jumatano",
            "Thursday": "Alhamisi",
            "Friday": "Ijumaa",
            "Saturday": "Jumamosi",
            "Sunday": "Jumapili"
        }
        today_weekday = datetime.datetime.today().strftime("%A")
        self.weekday = days[today_weekday] 

        super().save()

    def __str__(self):
        return self.get_swahili_date() 
    
    class Meta:
        verbose_name="MATANGAZO"
        verbose_name_plural = "MATANGAZO"

class AnnouncementDocument(models.Model):
     matangazo = models.ForeignKey(Announcement,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()
    
class Viwawa(SwahiliDateMixin,models.Model):
    created_at = models.DateField(auto_now_add=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
        return self.get_swahili_date()

    class Meta:
        verbose_name="VIWAWA (MATANGAZO)"
        verbose_name_plural = "VIWAWA (MATANGAZO)" 

class ViwawaDocument(models.Model):
     matangazo = models.ForeignKey(Viwawa,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()
    
class Wawata(SwahiliDateMixin,models.Model):
    created_at = models.DateField(auto_now_add=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
        return self.get_swahili_date()
    
    class Meta:
        verbose_name="WAWATA (MATANGAZO)"
        verbose_name_plural = "WAWATA (MATANGAZO)"

class WawataDocument(models.Model):
     matangazo = models.ForeignKey(Wawata,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)
     
     def __str__(self):
         return self.title.upper()
    
class Uwaka(SwahiliDateMixin,models.Model):
    created_at = models.DateField(auto_now_add=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
        return self.get_swahili_date()
    
    class Meta:
        verbose_name="UWAKA (MATANGAZO)"
        verbose_name_plural = "UWAKA (MATANGAZO)"

class UwakaDocument(models.Model):
     matangazo = models.ForeignKey(Uwaka,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()
    
class Event(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    mwezi = models.CharField(max_length=3,verbose_name='MWEZI')
    siku = models.CharField(max_length=2,verbose_name='SIKU')
    title = models.CharField(max_length=255,verbose_name='TITLE')
    created_at = models.DateField(verbose_name='TAREHE YA TUKIO')
    location = models.CharField(max_length=255,verbose_name='SEHEMU YA TUKIO')
    muda = models.CharField(max_length=255,verbose_name='MUDA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return self.title.upper()  # Displays the name of the lesson
    
    class Meta:
        verbose_name="MATUKIO"
        verbose_name_plural = "MATUKIO"

class EventDocument(models.Model):
     matangazo = models.ForeignKey(Event,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()
    
class Blog(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255,verbose_name='TITLE')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return self.title.upper()  # Displays the name of the lesson
    
    class Meta:
        verbose_name="BLOGU"
        verbose_name_plural = "BLOGU"

class BlogDocument(models.Model):
     matangazo = models.ForeignKey(Blog,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)
    
     def __str__(self):
         return self.title.upper()


class Sermon(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    weekday = models.CharField(max_length=255,verbose_name='SIKU YA JUMA', blank=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    somo_la_kwanza = models.CharField(max_length=255,verbose_name='SOMO LA KWANZA')
    somo_la_pili = models.CharField(max_length=255,verbose_name='SOMO LA PILI')
    injili = models.CharField(max_length=255,verbose_name='INJILI')
    tafakari = models.TextField(verbose_name='TAFAKARI')

    def save(self):
        days = {
            "Monday": "Jumatatu",
            "Tuesday": "Jumanne",
            "Wednesday": "Jumatano",
            "Thursday": "Alhamisi",
            "Friday": "Ijumaa",
            "Saturday": "Jumamosi",
            "Sunday": "Jumapili"
        }
        today_weekday = datetime.datetime.today().strftime("%A")
        self.weekday = days[today_weekday]

        super().save()

    def __str__(self):
        return self.get_swahili_date()

    class Meta:
        verbose_name="MAHUBIRI"
        verbose_name_plural = "MAHUBIRI"
    
class Article(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255,verbose_name='TITLE')
    author = models.CharField(max_length=255,verbose_name='MWANDISHI')
    maelezo = models.TextField(verbose_name='UJUMBE')
    
    def __str__(self):
        return self.title.upper()  # Displays the name of the lesson
    
    class Meta:
        verbose_name="MAKALA"
        verbose_name_plural = "MAKALA"

class MakalaQuotation(models.Model):
    nukuu = models.TextField(max_length=255,verbose_name='NUKUU')
    msemaji = models.CharField(max_length=50,verbose_name='MSEMAJI')
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')

    def __str__(self):
        return self.msemaji.upper()
    
    class Meta:
        verbose_name="NUKUU YA MAKALA"
        verbose_name_plural = "NUKUU YA MAKALA"


class CarourselMatangazo(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA MATANGAZO"

    class Meta:
        verbose_name="PICHA YA MATANGAZO"
        verbose_name_plural = "PICHA YA MATANGAZO"

class CarourselMatukio(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA MATUKIO"

    class Meta:
        verbose_name="PICHA YA MATUKIO"
        verbose_name_plural = "PICHA YA MATUKIO"

class CarourselRatiba(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA RATIBA"

    class Meta:
        verbose_name="PICHA YA RATIBA"
        verbose_name_plural = "PICHA YA RATIBA"

class CarourselBlogu(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA BLOGU"

    class Meta:
        verbose_name="PICHA YA BLOGU"
        verbose_name_plural = "PICHA YA BLOGU"

class CarourselMahubiri(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA MAHUBIRI"

    class Meta:
        verbose_name="PICHA YA MAHUBIRI"
        verbose_name_plural = "PICHA YA MAHUBIRI"


class CarourselMaktaba(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA MAKTABA"

    class Meta:
        verbose_name="PICHA YA MAKTABA"
        verbose_name_plural = "PICHA YA MAKTABA"


class CarourselJumuiya(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA JUMUIYA ZETU"

    class Meta:
        verbose_name="PICHA YA JUMUIYA ZETU"
        verbose_name_plural = "PICHA YA JUMUIYA ZETU"


class CarourselUwaka(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA UWAKA"

    class Meta:
        verbose_name="PICHA YA UWAKA"
        verbose_name_plural = "PICHA YA UWAKA"


class CarourselWawata(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA WAWATA"

    class Meta:
        verbose_name="PICHA YA WAWATA"
        verbose_name_plural = "PICHA YA WAWATA"


class CarourselViwawa(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA VIWAWA"

    class Meta:
        verbose_name="PICHA YA VIWAWA"
        verbose_name_plural = "PICHA YA VIWAWA"


class CarourselVyama(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA VYAMA VYETU"

    class Meta:
        verbose_name="PICHA ZA VYAMA VYETU"
        verbose_name_plural = "PICHA ZA VYAMA VYETU"

class Carourselkanda(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA KANDA ZETU"

    class Meta:
        verbose_name="PICHA YA KANDA ZETU"
        verbose_name_plural = "PICHA YA KANDA ZETU"

class CarourselUongozi(models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')

    def __str__(self):
        return "PICHA YA UONGOZI"

    class Meta:
        verbose_name="PICHA YA UONGOZI"
        verbose_name_plural = "PICHA YA UONGOZI"


class CarouselPodikasiti(models.Model):
    picha = models.ImageField(upload_to='pics',null=True,verbose_name='PICHA')

    def __str__(self):
        return "PODIKASITI PICHA"
    
    class Meta:
        verbose_name="PICHA YA PODIKASITI"
        verbose_name_plural = "PICHA YA PODIKASITI" \
        ""


    
class Podcast(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50,verbose_name='TITLE')
    video_url = models.URLField(verbose_name='YOUTUBE LINK')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return self.title.upper()  # Displays the name of the lesson
    
    class Meta:
        verbose_name="PODIKASITI"
        verbose_name_plural = "PODIKASITI"
    
class Give(models.Model):
    taarifa = models.TextField(verbose_name='UJUMBE')
    kwa_simu = models.TextField(verbose_name='KWA SIMU')
    kwa_benki = models.TextField(verbose_name='KWA BENKI')

    def __str__(self):
        return "CHANGIA"
    
    class Meta:
        verbose_name="CHANGIA"
        verbose_name_plural = "CHANGIA"

class Message(models.Model):
    taarifa = models.TextField(verbose_name='UJUMBE')
    phone_number = models.CharField(max_length=30,verbose_name='NAMBA YA SIMU')

    def __str__(self):
        return "TUMA UJUMBE"
    
    class Meta:
        verbose_name="TUMA UJUMBE"
        verbose_name_plural = "TUMA UJUMBE"
    
class Mubashara(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    taarifa = models.TextField(verbose_name='UJUMBE')
    created_at = models.DateField(null=True, blank=True,verbose_name='TAREHE')
    weekday = models.CharField(blank=True,max_length=255,default="Hamna",verbose_name='SIKU YA JUMA')
    muda = models.CharField( blank=True,max_length=255,default="Hamna",verbose_name='MUDA')
    link_url = models.URLField( null=True, blank=True,verbose_name='YOUTUBE LINK')

    def __str__(self):
        return "LIVE MATANGAZO"
    
    class Meta:
        verbose_name="LIVE MATANGAZO"
        verbose_name_plural = "LIVE MATANGAZO"
    
class Library(SwahiliDateMixin,models.Model):
    created_at = models.DateField(verbose_name='TAREHE YA TUKIO')
    title = models.CharField(max_length=255,verbose_name='TITLE')
    location = models.CharField(max_length=255,verbose_name='SEHEMU YA TUKIO')
     
    def __str__(self):
        return self.title.upper()
    
    class Meta:
        verbose_name="MAKTABA YA PICHA"
        verbose_name_plural = "MAKTABA YA PICHA"
    
class Picture(models.Model):
    libray = models.ForeignKey(Library,related_name='images', on_delete=models.CASCADE)
    picha = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.libray.title.upper()

class History(models.Model):
    historia = models.TextField(verbose_name='HISTORIA YA KANISA')

    def __str__(self):
        return "HISTORIA YETU"

    class Meta:
        verbose_name="HISTORIA YETU"
        verbose_name_plural = "HISTORIA YETU" 
    
class Faith(models.Model):
    imani = models.TextField(verbose_name='IMANI YA KANISA')

    def __str__(self):
        return "IMANI YETU"
    
    class Meta:
        verbose_name="IMANI YETU"
        verbose_name_plural = "IMANI YETU"

class Policy(models.Model):
    sera = models.TextField(verbose_name='SERA YA KANISA')

    def __str__(self):
        return "SERA YA FARAGHA"
    
    class Meta:
        verbose_name="SERA YA FARAGHA"
        verbose_name_plural = "SERA YA FARAGHA"

class Rule(models.Model):
    masharti = models.TextField(verbose_name='SHERIA NA MASHARTI')

    def __str__(self):
        return "SHERIA NA MASHARTI"
    
    class Meta:
        verbose_name="SHERIA NA MASHARTI"
        verbose_name_plural = "SHERIA NA MASHARTI"
    
class Mapadri(models.Model):
     picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
     cheo = models.CharField(max_length=255,verbose_name='CHEO')
     jina = models.CharField(max_length=40,verbose_name='JINA LA PADRI')
     maelezo = models.CharField(max_length=50,verbose_name='MAELEZO')

     def __str__(self):
        return self.jina.upper()
     
     class Meta:
        verbose_name="MAPADRI"
        verbose_name_plural = "MAPADRI"

class Viongozi_wa_kanisani(models.Model):
     picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
     cheo = models.CharField(max_length=255,verbose_name='CHEO')
     jina = models.CharField(max_length=40,verbose_name='JINA LA KIONGOZI')
     chama = models.CharField(max_length=60,verbose_name='JINA LA CHAMA')

     def __str__(self):
        return self.jina.upper()
     
     class Meta:
        verbose_name="VIONGOZI WA KANISANI"
        verbose_name_plural = "VIONGOZI WA KANISANI"
     
class Viongozi_wa_Jumuiya(models.Model):
     picha = models.ImageField(upload_to='pics',verbose_name='PICHA')
     cheo = models.CharField(max_length=255,verbose_name='CHEO')
     jina = models.CharField(max_length=40,verbose_name='JINA LA KIONGOZI')
     Jina_la_jumuiya = models.CharField(max_length=60,verbose_name='JINA LA JUMUIYA')

     def __str__(self):
        return self.jina.upper()
     
     class Meta:
        verbose_name="VIONGOZI WA JUMUIYA"
        verbose_name_plural = "VIONGOZI WA JUMUIYA"
     
class Ubatizo(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')
   

    def __str__(self):
        return 'UBATIZO'
    
    class Meta:
        verbose_name="UBATIZO"
        verbose_name_plural = "UBATIZO"
    
class UbatizoDocument(models.Model):
     ubatizo = models.ForeignKey(Ubatizo,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents') 

     def __str__(self):
         return self.title.upper()

class Ndoa(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return "NDOA"
    
    class Meta:
        verbose_name="NDOA"
        verbose_name_plural = "NDOA"
    
class NdoaDocument(models.Model):
    ndoa = models.ForeignKey(Ndoa,on_delete=models.CASCADE,related_name='documents')
    title = models.CharField(max_length=255)
    upload_file = models.FileField(upload_to='documents')

    def __str__(self):
         return self.title.upper()

class Ekaristi(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return "EKARISTI TAKATIFU"
    
    class Meta:
        verbose_name="EKARISTI TAKATIFU"
        verbose_name_plural = "EKARISTI TAKATIFU"
    
class EkaristiDocument(models.Model):
    ekaristi = models.ForeignKey(Ekaristi,related_name='documents',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    upload_file = models.FileField(upload_to='documents')

    def __str__(self):
         return self.title.upper()
    
class Kipaimara(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return "KIPAIMARA"
    
    class Meta:
        verbose_name="KIPAIMARA"
        verbose_name_plural = "KIPAIMARA"
    
class KipaimaraDocument(models.Model):
    kipaimara = models.ForeignKey(Kipaimara,related_name='documents',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    upload_file = models.FileField(upload_to='documents')

    def __str__(self):
         return self.title.upper()

class Toba(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return "TOBA"
    
    class Meta:
        verbose_name="TOBA"
        verbose_name_plural = "TOBA"
    
class Upako_wa_Wagonjwa(models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    maelezo = models.TextField(verbose_name='UJUMBE')

    def __str__(self):
        return "UPAKO WA WAGONJWA"
    
    class Meta:
        verbose_name="UPAKO WA WAGONJWA"
        verbose_name_plural = "UPAKO WA WAGONJWA"
    
class Muda_wa_ibada(models.Model):
    siku_za_juma = models.CharField(max_length=255,verbose_name='SIKU ZA JUMA')
    misa_ya_kwanza = models.CharField(max_length=255,verbose_name='MISA YA KWANZA')
    misa_ya_pili = models.CharField(max_length=255,verbose_name='MISA YA PILI')
    misa_ya_watoto = models.CharField(max_length=255,verbose_name='MISA YA WATOTO')

    def __str__(self):
        return "MUDA WA IBADA"
    
    class Meta:
        verbose_name="MUDA WA IBADA"
        verbose_name_plural = "MUDA WA IBADA"
    
class Ratiba_za_ofisini(models.Model):
    siku_za_juma = models.CharField(max_length=255,verbose_name='SIKU ZA JUMA')
    jumapili = models.CharField(max_length=255,verbose_name='JUMAPILI')

    def __str__(self):
        return "RATIBA ZA OFISINI"
    
    class Meta:
        verbose_name="RATIBA ZA KANISANI"
        verbose_name_plural = "RATIBA ZA KANISANI"
    
class Muda_wa_Maungamo(models.Model):
    ijumaa = models.CharField(max_length=255)
    jumamosi = models.CharField(max_length=255)

    def __str__(self):
        return "MUDA WA MAUNGAMO"
    
    class Meta:
        verbose_name="MUDA WA MAUNGAMO"
        verbose_name_plural = "MUDA WA MAUNGAMO"

class Jumuiya(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    Jina_la_jumuiya = models.CharField(max_length=255,verbose_name='JINA LA JUMUIYA')
    created_at = models.DateField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.Jina_la_jumuiya.upper()
    
    class Meta:
        verbose_name="JUMUIYA ZETU"
        verbose_name_plural = "JUMUIYA ZETU"
    
class Jumuiya_page(SwahiliDateMixin,models.Model):
    jumuiya = models.ForeignKey(Jumuiya,related_name="pages",on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
        return f"{self.jumuiya.Jina_la_jumuiya.upper()} - {self.created_at.strftime('%d %B %Y').upper()}"
    
    class Meta:
        verbose_name="JUMUIYA (MATANGAZO)"
        verbose_name_plural = "JUMUIYA (MATANGAZO)"

class JumuiyaDocument(models.Model):
     matangazo = models.ForeignKey(Jumuiya_page,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()
    
    
class Vyama(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    Jina_la_chama = models.CharField(max_length=255,verbose_name='JINA LA CHAMA')
    created_at = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Jina_la_chama.upper()
    
    class Meta:
        verbose_name="VYAMA VYETU"
        verbose_name_plural = "VYAMA VYETU"
    
class Vyama_page(SwahiliDateMixin,models.Model):
    vyama = models.ForeignKey(Vyama,related_name='chama',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
         return F"{self.vyama.Jina_la_chama.upper()} - {self.created_at.strftime('%d %B %Y').upper()}"
    
    class Meta:
        verbose_name="VYAMA (MATANGAZO)"
        verbose_name_plural = "VYAMA (MATANGAZO)"

class VyamaDocument(models.Model):
     matangazo = models.ForeignKey(Vyama_page,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()


class Resetpassword(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable= False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PASSWORD RESET FOR {self.user.username} at {self.created_when}"
    
    class Meta:
        verbose_name="RESET PASSWORD"
        verbose_name_plural = "RESET PASSWORD"

class Kanda(SwahiliDateMixin,models.Model):
    picha = models.ImageField(upload_to='pics', null=True,verbose_name='PICHA')
    Jina_la_kanda = models.CharField(max_length=255,verbose_name='JINA LA KANDA')
    created_at = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Jina_la_kanda.upper()
    
    class Meta:
        verbose_name="KANDA ZETU"
        verbose_name_plural = "KANDA ZETU"
    
class Kanda_page(SwahiliDateMixin,models.Model):
    kanda = models.ForeignKey(Kanda,related_name='chama',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    maelezo = models.TextField(verbose_name='TANGAZO')

    def __str__(self):
         return F"{self.kanda.Jina_la_kanda.upper()} - {self.created_at.strftime('%d %B %Y').upper()}"
    
    class Meta:
        verbose_name="KANDA (MATANGAZO)"
        verbose_name_plural = "KANDA (MATANGAZO)"

class KandaDocument(models.Model):
     matangazo = models.ForeignKey(Kanda_page,related_name='documents',on_delete=models.CASCADE)
     title = models.CharField(max_length=255)
     upload_file = models.FileField(upload_to='documents',null=True)

     def __str__(self):
         return self.title.upper()

class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError("Barua pepe inahitajika")
        
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active",False)     # User inactive until verified
        user =self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active", True)  # Superuser should always be active

        return self.create_user(email,password,**extra_fields)
    
class CustomUser(AbstractUser):
    username = None  # Remove username
    email = models.EmailField(unique=True,verbose_name='BARUA PEPE')
    first_name = models.CharField(max_length=100,verbose_name='JINA LA KWANZA')
    last_name = models.CharField(max_length=100,verbose_name='JINA LA MWISHO')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name="USER MANAGEMENT"
        verbose_name_plural = "USER MANAGEMENT"



