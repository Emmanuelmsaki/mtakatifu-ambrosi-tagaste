from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Masomo
from .models import Announcement,AnnouncementDocument
from .models import Event,EventDocument
from .models import Blog,BlogDocument
from .models import Sermon
from .models import Article
from .models import Podcast
from .models import Give
from .models import Message
from .models import Mubashara
from .models import Library,Picture
from .models import History
from .models import Faith
from .models import Policy
from .models import Rule
from .models import Mapadri
from .models import Viongozi_wa_kanisani
from .models import Viongozi_wa_Jumuiya
from .models import Ubatizo,UbatizoDocument
from .models import Ndoa,NdoaDocument
from .models import Ekaristi,EkaristiDocument
from .models import Kipaimara,KipaimaraDocument
from .models import Toba
from .models import Upako_wa_Wagonjwa
from .models import Viwawa,ViwawaDocument
from .models import Wawata,WawataDocument
from .models import Uwaka,UwakaDocument
from .models import Muda_wa_ibada
from .models import Ratiba_za_ofisini
from .models import Muda_wa_Maungamo
from .models import Jumuiya,Jumuiya_page,JumuiyaDocument
from .models import Vyama, Vyama_page,VyamaDocument
from .models import MakalaQuotation
from .models import CarouselPodikasiti
from .models import Resetpassword,CarourselRatiba,CarourselMaktaba,Carourselkanda
from .models import CarourselMatangazo,CarourselMatukio,CarourselMahubiri,CarourselBlogu
from .models import CarourselJumuiya,CarourselUwaka,CarourselWawata,CarourselViwawa,CarourselVyama
from .models import Kanda,Kanda_page,KandaDocument,CarourselUongozi
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'phone', 'amount', 'status', 'provider', 'transaction_id', 'created_at')
    list_filter = ('status', 'provider', 'created_at')
    search_fields = ('phone', 'external_id', 'transaction_id')

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    # Modify fieldsets without duplicates
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    
class Vyama_pageInline(admin.TabularInline):
     model = Vyama_page  
     extra = 1  

class VyamaDocumentInline(admin.TabularInline):
    model = VyamaDocument
    extra = 1

class VyamaAdmin(admin.ModelAdmin):
       list_display = ('Jina_la_chama',)  
       search_fields = ('Jina_la_chama',)  

class Vyama_pageAdmin(admin.ModelAdmin):
    inlines = [VyamaDocumentInline]
    list_display = ('vyama','created_at')  
    list_filter = ('vyama',) 
    search_fields = ('vyama__Jina_la_chama',) 

class Kanda_pageInline(admin.TabularInline):
     model = Kanda_page  
     extra = 1  

class KandaDocumentInline(admin.TabularInline):
    model = KandaDocument
    extra = 1

class KandaAdmin(admin.ModelAdmin):
       list_display = ('Jina_la_kanda',)  
       search_fields = ('Jina_la_kanda',)  

class Kanda_pageAdmin(admin.ModelAdmin):
    inlines = [KandaDocumentInline]
    list_display = ('kanda','created_at')  
    list_filter = ('kanda',) 
    search_fields = ('kanda__Jina_la_kanda',) 

class BlogDocumentInline(admin.TabularInline):
    model = BlogDocument
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogDocumentInline]

class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1  

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('created_at','title',  'location')  
    search_fields = ('title',)  
    inlines = [PictureInline]  

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',  'author') 
    search_fields = ('title',)  

class EventDocumentInline(admin.TabularInline):
    model = EventDocument
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [EventDocumentInline]
    list_display=('created_at','title')
    search_fields = ('title',)

class Viongozi_wa_JumuiyaAdmin(admin.ModelAdmin):
    list_display = ('jina', 'Jina_la_jumuiya') 
    search_fields = ('Jina_la_jumuiya',)  

class Viongozi_wa_kanisaniAdmin(admin.ModelAdmin):
    list_display = ('jina', 'chama') 
    search_fields = ('chama',) 


class UbatizoDocumentInline(admin.TabularInline):
    model =UbatizoDocument
    extra =1

class UbatizoAdmin(admin.ModelAdmin):
    inlines = [UbatizoDocumentInline]

class AnnouncementDocumentInline(admin.TabularInline):
    model = AnnouncementDocument
    extra = 1

class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [AnnouncementDocumentInline]

class NdoaDocumentInline(admin.TabularInline):
    model =NdoaDocument
    extra = 1

class NdoaAdmin(admin.ModelAdmin):
    inlines =[NdoaDocumentInline]

class EkaristiDocumentInline(admin.TabularInline):
    model = EkaristiDocument
    extra = 1

class EkaristiAdmin(admin.ModelAdmin):
    inlines = [EkaristiDocumentInline]

class KipaimaraDocumentInline(admin.TabularInline):
    model = KipaimaraDocument
    extra = 1

class KipaimaraAdmin(admin.ModelAdmin):
    inlines =[KipaimaraDocumentInline]

class UwakaDocumentInline(admin.TabularInline):
    model = UwakaDocument
    extra = 1

class UwakaAdmin(admin.ModelAdmin):
    inlines =[UwakaDocumentInline]

class WawataDocumentInline(admin.TabularInline):
    model = WawataDocument
    extra = 1

class WawataAdmin(admin.ModelAdmin):
    inlines =[WawataDocumentInline]

class ViwawaDocumentInline(admin.TabularInline):
    model = ViwawaDocument
    extra = 1

class ViwawaAdmin(admin.ModelAdmin):
    inlines =[ViwawaDocumentInline]
    

class Jumuiya_pageInline(admin.TabularInline):
     model = Jumuiya_page  
     extra = 1  

class JumuiyaDocumentInline(admin.TabularInline):
    model = JumuiyaDocument
    extra = 1

class JumuiyaAdmin(admin.ModelAdmin):
       list_display = ('Jina_la_jumuiya',) 
       search_fields = ('Jina_la_jumuiya',) 

class Jumuiya_pageAdmin(admin.ModelAdmin):
    inlines =[JumuiyaDocumentInline]
    list_display = ('jumuiya','created_at')  
    list_filter = ('jumuiya',)  
    search_fields = ('jumuiya__Jina_la_jumuiya',)  


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Carourselkanda)
admin.site.register(CarourselUongozi)
admin.site.register(CarourselBlogu)
admin.site.register(CarourselVyama)
admin.site.register(CarourselViwawa)
admin.site.register(CarourselWawata)
admin.site.register(CarourselUwaka)
admin.site.register(CarourselJumuiya)
admin.site.register(CarourselMaktaba)
admin.site.register(CarourselRatiba)
admin.site.register(CarourselMahubiri)
admin.site.register(CarourselMatukio)
admin.site.register(CarourselMatangazo)
admin.site.register(Jumuiya, JumuiyaAdmin)
admin.site.register(Jumuiya_page,Jumuiya_pageAdmin)
admin.site.register(Masomo)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Sermon)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Podcast)
admin.site.register(Give)
admin.site.register(Message)
admin.site.register(Mubashara)
admin.site.register(Library, LibraryAdmin)
admin.site.register(History)
admin.site.register(Faith)
admin.site.register(Policy)
admin.site.register(Rule)
admin.site.register(Mapadri)
admin.site.register(Viongozi_wa_kanisani,Viongozi_wa_kanisaniAdmin)
admin.site.register(Viongozi_wa_Jumuiya,Viongozi_wa_JumuiyaAdmin)
admin.site.register(Ubatizo, UbatizoAdmin)
admin.site.register(Ndoa,NdoaAdmin)
admin.site.register(Ekaristi,EkaristiAdmin)
admin.site.register(Kipaimara,KipaimaraAdmin)
admin.site.register(Toba)
admin.site.register(Upako_wa_Wagonjwa)
admin.site.register(Viwawa,ViwawaAdmin)
admin.site.register(Wawata,WawataAdmin)
admin.site.register(Uwaka,UwakaAdmin)
admin.site.register(Muda_wa_ibada)
admin.site.register(Ratiba_za_ofisini)
admin.site.register(Muda_wa_Maungamo)
admin.site.register(MakalaQuotation)
admin.site.register(CarouselPodikasiti)
admin.site.register(Kanda, KandaAdmin)
admin.site.register(Kanda_page,Kanda_pageAdmin)
admin.site.register(Vyama, VyamaAdmin)
admin.site.register(Vyama_page, Vyama_pageAdmin)
admin.site.register(Resetpassword)