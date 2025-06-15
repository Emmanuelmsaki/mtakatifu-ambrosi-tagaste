from django.shortcuts import render, get_object_or_404,redirect
from smtplib import SMTPException
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import * 
import re
from datetime import date, timedelta
from .models import Masomo
from .models import Announcement
from .models import Event
from .models import Blog
from .models import Sermon
from .models import Article
from .models import Podcast
from .models import Give
from .models import Message
from .models import Mubashara
from .models import Library
from .models import History
from .models import Faith
from .models import Policy
from .models import Rule
from .models import Mapadri
from .models import Viongozi_wa_kanisani
from .models import Viongozi_wa_Jumuiya
from .models import Ubatizo
from .models import Ndoa
from .models import Ekaristi
from .models import Kipaimara
from .models import Toba
from .models import Upako_wa_Wagonjwa
from .models import Viwawa
from .models import Wawata
from .models import Uwaka
from .models import Muda_wa_ibada
from .models import Ratiba_za_ofisini
from .models import Muda_wa_Maungamo
from .models import Jumuiya,Jumuiya_page
from .models import Vyama,Vyama_page
from .models import MakalaQuotation
from .models import CarouselPodikasiti
from .models import Resetpassword,CarourselMaktaba
from .models import CarourselMatangazo,CarourselMatukio,CarourselRatiba,CarourselBlogu
from .models import CarourselJumuiya,CarourselUwaka,CarourselWawata,CarourselViwawa,CarourselVyama
from django.core.paginator import Paginator
from .models import Kanda,Kanda_page,KandaDocument
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid 
import time
from datetime import datetime
from .models import Give, PaymentTransaction  # Add PaymentTransaction model



User = get_user_model()

def email(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New message from {name}"
        full_message = f"Jina: {name}\nBarue Pepe: {email}\n\nUjumbe:\n{message}"

        try:
           email_message = EmailMessage(
                subject=subject,
                body=full_message,
                from_email=settings.EMAIL_HOST_USER,  # Must be your verified sender
                to=[settings.EMAIL_HOST_USER],  # You receive it
                reply_to=[email],  # So when you click "Reply", it replies to the user
            )
           email_message.send()
           messages.success(request, "Ujumbe umetumwa kwa mafanikio!")
        except:
            messages.error(request, "Imeshindikana kutuma ujumbe. Tafadhali jaribu tena.")
        return redirect('email')
    
    return render(request, 'email.html')

def index(request):
    Somos = Masomo.objects.order_by('id')
    next_event = Event.objects.filter(created_at__gte=date.today()).order_by('created_at').first()
    recent_blogs = Blog.objects.all().order_by('-created_at')[:4]  # Get the latest 4 blogs
    quote = MakalaQuotation.objects.first()
    latest_sermon = Sermon.objects.all().order_by('-created_at').first()  # Fetch the latest sermon in tafakari link index.html
    pic = CarourselRatiba.objects.first()
    pica = CarourselJumuiya.objects.first()
    pice = CarourselMahubiri.objects.first()
    pici = CarourselMatukio.objects.first()
    pico = CarouselPodikasiti.objects.first()

    return render(request,'index.html',{'Somos':Somos,'next_event': next_event,'recent_blogs':recent_blogs,'quote':quote,'pic':pic,'pica':pica,'pice':pice,'pici':pici,'pico':pico,'latest_sermon': latest_sermon})

def ingia(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            # Check if the user's account is active (i.e., email verified)
            if user.is_active:
                login(request, user)

                # Redirect superusers and staff to the admin page+
                if user.is_superuser or user.is_staff:
                    return redirect("/admin/")

                # Redirect to the home page or dashboard
                return redirect('index')

            else:
                # If user is registered but not verified, show the verification message
                messages.error(request, "Bonyeza link iliyotumwa kwenye barua pepe yako ili kuthibitisha akaunti yako.")
                return redirect('ingia')  # Stay on the login page
        
        else:
            messages.error(request,"Taarifa ulizoingiza sio sahihi.")
            
            return redirect('ingia')
    
    return render(request,'ingia.html')

def ondoka(request):
    logout(request)

    return redirect('index')

def jisajili(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        user_data_has_error = False

        if password != password2:
            user_data_has_error = True
            messages.error(request,"Neno la siri halifanani.")

        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request,"Barua pepe hii imeshatumika.")

        if len(password) < 5 or len(password2) <5 :
            user_data_has_error = True
            messages.error(request,"Neno la siri lazima angalau lianzie herufi 5.")

        if user_data_has_error:
             return redirect('jisajili')
        else:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password2
            )

            new_user.is_active = False  # Disable the user until email is verified
            new_user.save()

            #Send verification email
            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            token = default_token_generator.make_token(new_user)

            verification_link =f"http://{get_current_site(request).domain}/verify_email/{uid}/{token}"
            subject = "Thibitisha Barua pepe"
            message = f"Thibitisha Barua pepe yako kwa kutumia link hii: {verification_link}"

            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=f'Mtakatifu Ambrosi <{settings.EMAIL_HOST_USER}>',
                to=[email]
            )
            email_message.fail_silently = True

            # **Wrap email sending in try-except to handle SMTP errors**
            try:
                email_message.send()
                messages.success(request, "Bonyeza link iliyotumwa kwenye barua pepe yako ili kuthibitisha akaunti yako.")
                return redirect('ingia')
            except SMTPException:
                messages.error(request, "Imeshindikana kutuma barua pepe ya uthibitisho. Tafadhali jaribu tena baadaye.")
                return redirect('jisajili')  # Redirect user without breaking the app


    return render(request,'jisajili.html')

def verify_email(request, uidb64, token):
    try:
        #Decode the UID and get the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        #Check if the token is valid
        if default_token_generator.check_token(user,token):
            user.is_active =True #Activate the user
            user.save()
            messages.success(request,"Barua pepe imethibitishwa. Ingia Sasa.")
            return redirect('ingia')
        else:
            messages.error(request, "Link hii imeisha muda wake.")
            return redirect('resend_verification', user_id=user.id)  # Redirect to resend verification page
        
    except (User.DoesNotExist, ValueError, TypeError):
        messages.error(request,"Tatizo lilitokea wakati wa kuthibitisha barua pepe.")
        return redirect('index')

def resend_verification(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        
        # Ensure the user is not already active
        if user.is_active:
            messages.info(request, "Akaunti yako tayari imethibitishwa.")
            return redirect('index')

        # Generate a new UID and token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_link = f"http://{get_current_site(request).domain}/verify_email/{uid}/{token}"
        subject = "Thibitisha Barua pepe"
        message = f"Thibitisha Barua pepe yako kwa kutumia link hii: {verification_link}"

        # Send the email
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=f'Mtakatifu Ambrosi <{settings.EMAIL_HOST_USER}>',
            to=[user.email]
        )
        email_message.fail_silently = True
        email_message.send()

        messages.success(request, "Link mpya imetumwa kwenye barua pepe yako. Tafadhali angalia.")
        return redirect('ingia')

    except User.DoesNotExist:
        messages.error(request, "Tatizo lilitokea wakati wa kutuma barua pepe.")
        return redirect('index')

def forgetpassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = Resetpassword(user=user) #resetpassword name model
            new_password_reset.save()

            password_reset_url = reverse('resetpassword',kwargs={'reset_id':new_password_reset.reset_id}) #resetpassword name in urls

            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"  
            
            
            email_message = EmailMessage(
                 subject='Badilisha Neno la siri',
                 body=F'Badilisha Neno la Siri kwa kubonyeza link apa chini:\n\n\n\n{full_password_reset_url}', 
                 from_email=f'Mtakatifu Ambrosi <{settings.EMAIL_HOST_USER}>', 
                 to=[email] 
            )

            email_message.fail_silently =True
            email_message.send()

            return redirect ('resettext',reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request,F"Hakuna mtumiaji mwenye Barua pepe '{email}'")
            return redirect("forgetpassword")

    return render(request,'forgetpassword.html')

def resetpassword(request,reset_id):

    try:
        password_reset_id = Resetpassword.objects.get(reset_id=reset_id)

        if request.method=="POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
               passwords_have_error = True
               messages.error(request,"Neno la siri halifanani.")

            if len(password) < 5 or len(confirm_password) <5 :
                passwords_have_error = True
                messages.error(request,"Neno la siri lazima angalau lianzie herufi 5.")

            expiration_time =password_reset_id.created_when + timezone.timedelta(minutes=60)

            if timezone.now()> expiration_time:
                passwords_have_error = True
                messages.error(request,"link imekuwa batili.")
                password_reset_id.delete()
                return redirect('forgetpassword')

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                # Delete reset link after successful password change
                password_reset_id.delete()

                messages.success(request,'Neno la siri limebadilika. Sasa Ingia.')
                return redirect('ingia')
            
            else:
                return redirect('resetpassword',reset_id=reset_id)


    except Resetpassword.DoesNotExist:

        messages.error(request,'link sio sahihi au imeisha muda wake.')
        return redirect('forgetpassword')
    
    return render(request,'resetpassword.html')

def resettext(request,reset_id):
    if Resetpassword.objects.filter(reset_id=reset_id).exists():  
       return render(request,'resettext.html')
    
    else:
       messages.error(request,'link sio sahihi.')
       return redirect('forgetpassword')

def matangazo(request):
    announcements_list = Announcement.objects.all().order_by('-created_at')
    pic = CarourselMatangazo.objects.first()

    # Pagination: Show 10 announcements per page
    paginator = Paginator(announcements_list, 9)  
    page_number = request.GET.get('page')
    announcements = paginator.get_page(page_number)

    return render(request,'matangazo.html',{'announcements':announcements,'pic':pic})

def matangazo_page(request,pk):
    Announcements = Announcement.objects.get(id=pk)
    
    return render(request,'matangazo_page.html',{'Announcements':Announcements})

def matukio(request):
    today = date.today()
    Event.objects.filter(created_at__lte=today - timedelta(days=1)).delete()  # Delete old events
    pici = CarourselMatukio.objects.first()

    Events_list= Event.objects.all().order_by('created_at')

     # Pagination: Show 10 announcements per page
    paginator =Paginator(Events_list,10)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    
    return render(request,'matukio.html',{'events':events,'pici':pici})

def matukio_page(request,pk):
    Events = Event.objects.get(id=pk)
    return render(request,'matukio_page.html',{'Events':Events})

def blogu(request):
    Blogs_list = Blog.objects.all().order_by('-created_at')
    pic = CarourselBlogu.objects.first()

    paginator = Paginator(Blogs_list,10)
    page_number = request.GET.get('page')
    Blogs = paginator.get_page(page_number)

    return render(request,'blogu.html',{'Blogs':Blogs,'pic':pic})

def blogu_page(request,pk):
    Blogs = Blog.objects.get(id=pk)

    return render(request,'blogu_page.html',{'Blogs':Blogs})

def mahubiri(request):
    Sermons_list = Sermon.objects.all().order_by('-created_at') 
    pice = CarourselMahubiri.objects.first()

    paginator = Paginator(Sermons_list ,10)
    page_number = request.GET.get('page')
    Sermons = paginator.get_page(page_number)

    return render(request,'mahubiri.html',{'Sermons':Sermons,'pice':pice})

def mahubiri_page(request,pk):
    Sermons = Sermon.objects.get(id=pk)

    return render(request,'mahubiri_page.html',{'Sermons':Sermons})

def makala(request):
    Articles_list = Article.objects.all().order_by('-created_at')
    pic = MakalaQuotation.objects.first()

    paginator = Paginator(Articles_list ,10)
    page_number = request.GET.get('page')
    Articles = paginator.get_page(page_number)

    return render(request,'makala.html',{'Articles':Articles,'pic':pic})

def makala_page(request,pk):
    Articles = Article.objects.get(id=pk)

    return render(request,'makala_page.html',{'Articles':Articles})

def podikasiti(request):
    podcasts_list = Podcast.objects.all().order_by('-created_at')
    pic = CarouselPodikasiti.objects.first()

    paginator = Paginator(podcasts_list ,9)
    page_number = request.GET.get('page')
    podcasts = paginator.get_page(page_number)

    return render(request,'podikasiti.html',{'podcasts':podcasts,'pic':pic}) 

def podikasiti_page(request,id):
    podcast = get_object_or_404(Podcast, id=id)

     # Extract video ID from any YouTube URL
    match = re.search(r'(?:v=|be/|embed/|shorts/)([\w\-]{11})', podcast.video_url)
    video_id = match.group(1) if match else None
    embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else ""

    return render(request, 'podikasiti_page.html', {
        'podcast': podcast,
        'embed_url': embed_url
    })

def changia(request):
    gives = Give.objects.first()
    return render(request, 'changia.html', {'gives': gives})

AZAMPAY_ACCESS_TOKEN = None
AZAMPAY_TOKEN_EXPIRY = 0  

def get_azampay_token():
    global AZAMPAY_ACCESS_TOKEN, AZAMPAY_TOKEN_EXPIRY

    if AZAMPAY_ACCESS_TOKEN and AZAMPAY_TOKEN_EXPIRY > time.time() + 60:
        return AZAMPAY_ACCESS_TOKEN

    token_url = f"{settings.AZAMPAY_SANDBOX_AUTHENTICATOR_URL}/AppRegistration/GenerateToken"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "appName": settings.AZAMPAY_APP_NAME,
        "clientId": settings.AZAMPAY_CLIENT_ID,
        "clientSecret": settings.AZAMPAY_CLIENT_SECRET
    }

    try:
        response = requests.post(token_url, headers=headers, json=payload)
        response.raise_for_status()
        token_data = response.json()

        if token_data.get('success') and token_data['data'].get('accessToken'):
            AZAMPAY_ACCESS_TOKEN = token_data['data']['accessToken']
            expire_datetime_str = token_data['data']['expire']
            expire_dt_object = datetime.strptime(expire_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
            AZAMPAY_TOKEN_EXPIRY = expire_dt_object.timestamp()

            print(f"AzamPay token generated successfully. Expires at: {datetime.fromtimestamp(AZAMPAY_TOKEN_EXPIRY)}")
            return AZAMPAY_ACCESS_TOKEN
        else:
            print(f"Failed to get AzamPay token: {token_data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching AzamPay token: {e}")
        return None

PROVIDER_PREFIXES = {
    'Airtel_Money': ['+25578', '+25568'],
    'Mixx_by_Yas': ['+25565', '+25571'],
    'HaloPesa': ['+25562',],
    'Azampesa': ['+25573', '+25574']
}

def detect_provider(phone):
    for provider, prefixes in PROVIDER_PREFIXES.items():
        if any(phone.startswith(prefix) for prefix in prefixes):
            return provider
    return 'Azampesa'

def process_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        amount_str = request.POST.get('number')

        # Validate phone number format: +255 followed by exactly 9 digits
        phone_pattern = r'^\+255\d{9}$'
        if not phone_number or not re.match(phone_pattern, phone_number):
            error_message = 'Tafadhali ingiza namba ya simu sahihi'
            return render(request, 'payment_failed.html', {
                'error_message': error_message,
                'phone': phone_number,
                'number': amount_str
            })

        # Validate amount is a valid float and within limits
        try:
            amount = float(amount_str)
            if amount < 100:  # minimum amount e.g., 100 TZS
                raise ValueError("Kiasi ni kidogo sana.")
            if amount > 5000001:  # max amount e.g., 5,000,000 TZS
                raise ValueError("Kiasi ni kikubwa sana.")
        except (ValueError, TypeError) as e:
            error_message = f'Kiasi si sahihi: {str(e)}'
            return render(request, 'payment_failed.html', {
                'error_message': error_message,
                'phone': phone_number,
                'number': amount_str
            })

        access_token = get_azampay_token()
        if not access_token:
            return render(request, 'payment_failed.html', {
                'error_message': 'Imeshindikana kupata ruhusa ya malipo. Tafadhali jaribu tena.',
                'phone': phone_number,
                'number': amount_str
            })

        provider = detect_provider(phone_number)

        checkout_url = f"{settings.AZAMPAY_SANDBOX_CHECKOUT_URL}/azampay/mno/checkout"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        external_id = str(uuid.uuid4())

        payload = {
            "accountNumber": phone_number,
            "amount": amount,
            "currency": "TZS",
            "externalId": external_id,
            "provider": provider
        }

        print(f"Sending MNO Checkout request: {json.dumps(payload, indent=2)}")

        try:
            checkout_response = requests.post(checkout_url, headers=headers, json=payload)
            checkout_response.raise_for_status()
            response_data = checkout_response.json()

            if response_data.get('success'):
                transaction_id = response_data.get('transactionId')
                message = response_data.get('message', 'Malipo yameanzishwa. Tafadhali angalia simu yako.')

                # Save transaction in DB
                PaymentTransaction.objects.create(
                    external_id=external_id,
                    phone=phone_number,
                    amount=amount,
                    status='pending',
                    provider=provider,
                    transaction_id=transaction_id
                )

                return render(request, 'payment_success.html', {
                    'transaction_id': transaction_id,
                    'message': message,
                    'external_id': external_id
                })
            else:
                error_message = response_data.get('message', 'Malipo yameshindwa kuanzishwa.')
                print(f"AzamPay MNO Checkout failed: {error_message}")
                return render(request, 'payment_failed.html', {
                    'error_message': error_message,
                    'phone': phone_number,
                    'number': amount_str
                })
        except requests.exceptions.RequestException as e:
            print(f"Error initiating AzamPay MNO Checkout: {e}")
            return render(request, 'payment_failed.html', {
                'error_message': f'Hitilafu imejitokeza wakati wa kuwasiliana na AzamPay: {e}',
                'phone': phone_number,
                'number': amount_str
            })

    return redirect('changia')

def azampay_callback(request):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            print(f"Received AzamPay Callback: {json.dumps(callback_data, indent=2)}")

            transaction_status = callback_data.get('transactionstatus')
            reference_id = callback_data.get('reference')
            utility_ref = callback_data.get('utilityref')
            amount = callback_data.get('amount')
            msisdn = callback_data.get('msisdn')
            message = callback_data.get('message')
            operator = callback_data.get('operator')
            fsp_reference_id = callback_data.get('fspReferenceId')

            try:
                txn = PaymentTransaction.objects.get(external_id=utility_ref)
                txn.status = transaction_status
                txn.transaction_id = reference_id
                txn.save()
                print(f"Transaction {reference_id} updated in DB.")
            except PaymentTransaction.DoesNotExist:
                print(f"No matching transaction for external ID {utility_ref}")

            return JsonResponse({"message": "Callback received successfully"}, status=200)

        except json.JSONDecodeError:
            print("Invalid JSON in AzamPay callback request body.")
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            print(f"Error processing AzamPay callback: {e}")
            return JsonResponse({"message": "Internal Server Error"}, status=500)
    else:
        return JsonResponse({"message": "Method Not Allowed"}, status=405)

def ujumbe(request):
    messag = Message.objects.first()

    return render(request,'ujumbe.html',{'messag':messag})

def live_stream(request):
    mubashara = Mubashara.objects.first()

    return render(request,'live_stream.html',{'mubashara':mubashara})

def live_stream_page(request, id):
    mubashara = get_object_or_404(Mubashara, id=id)

    # Extract video ID from any YouTube URL
    match = re.search(r'(?:v=|be/|embed/|shorts/)([\w\-]{11})', mubashara.link_url)
    video_id = match.group(1) if match else None
    embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else ""

    return render(request, 'live_stream_page.html', {
        'mubashara': mubashara,
        'embed_url': embed_url
    })

def maktaba(request):
    # Fetch events with images (you can define this model with a ForeignKey to images)
    libraries_list = Library.objects.all().order_by('-created_at')
    pic = CarourselMaktaba.objects.first()

    paginator = Paginator(libraries_list ,9)
    page_number = request.GET.get('page')
    libraries = paginator.get_page(page_number)

    return render(request,'maktaba.html',{'libraries':libraries,'pic':pic})

def maktaba_page(request,pk):
     # Get the specific event based on its ID and related images
     library = get_object_or_404(Library,id=pk)
     library_images = library.images.all()

     return render(request,'maktaba_page.html',{'library':library,'library_images':library_images})

def historia(request):
    histori = History.objects.first()

    return render(request,'historia.html',{'histori':histori})

def imani(request):
    iman = Faith.objects.first()

    return render(request,'imani.html',{'iman':iman})

def sera(request):
    sera_yetu = Policy.objects.first()

    return render(request,'sera.html',{'sera_yetu':sera_yetu})

def masharti(request):
    sheria = Rule.objects.first()

    return render(request,'masharti.html',{'sheria':sheria})

def uongozi(request):
    mapadri = Mapadri.objects.all()
    kanisani = Viongozi_wa_kanisani.objects.all()
    jumuiya = Viongozi_wa_Jumuiya.objects.all()
    pic =CarourselUongozi.objects.first()

    return render(request,'uongozi.html',{'mapadri':mapadri,'kanisani':kanisani,'jumuiya':jumuiya,'pic':pic})

def ubatizo(request):
    ubatizo = Ubatizo.objects.first()

    return render(request,'ubatizo.html',{'ubatizo':ubatizo})

def ndoa(request):
     ndoa = Ndoa.objects.first()
     
     return render(request,'ndoa.html',{'ndoa':ndoa})

def ekaristi(request):
    ekaristi = Ekaristi.objects.first()
   
    return render(request,'ekaristi.html',{'ekaristi':ekaristi})

def kipaimara(request):
    kipaimara = Kipaimara.objects.first()

    return render(request,'kipaimara.html',{'kipaimara':kipaimara})

def toba(request):
    toba = Toba.objects.first()

    return render(request,'toba.html',{'toba':toba})

def wagonjwa(request):
    wagonjwa = Upako_wa_Wagonjwa.objects.first()

    return render(request,'wagonjwa.html', {'wagonjwa':wagonjwa})


def jumuiya(request):
    jumuiyas_list = Jumuiya.objects.all().order_by('-created_at')
    pica = CarourselJumuiya.objects.first()

    paginator = Paginator(jumuiyas_list ,9)
    page_number = request.GET.get('page')
    jumuiyas = paginator.get_page(page_number)

    return render(request,'jumuiya.html',{'jumuiyas':jumuiyas,'pica':pica})

def jumuiya_page1(request,jumuiya_id):

    jumuiya = get_object_or_404(Jumuiya,pk=jumuiya_id)
    pages_list = jumuiya.pages.all().order_by('-created_at')

    paginator = Paginator(pages_list ,9)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    return render(request,'jumuiya_page1.html',{'jumuiya':jumuiya,'pages':pages})

def jumuiya_page2(request,page_id):
    page = get_object_or_404(Jumuiya_page,pk=page_id)

    return render(request,'jumuiya_page2.html',{'jumuiya':page})


def vyama(request):
    vyamaz_list = Vyama.objects.all().order_by('-created_at')
    pic = CarourselVyama.objects.first()

    paginator = Paginator(vyamaz_list ,9)
    page_number = request.GET.get('page')
    vyamaz = paginator.get_page(page_number)

    return render(request,'vyama.html',{'vyamaz':vyamaz,'pic':pic})

def vyama_page1(request,vyapage):
    cham = get_object_or_404(Vyama,id=vyapage)
    pages_list = cham.chama.all().order_by('-created_at')

    paginator = Paginator(pages_list ,9)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    
    return render(request,'vyama_page1.html',{'cham':cham,'pages':pages})

def vyama_page(request,chapage):
    vyama = get_object_or_404(Vyama_page, id=chapage)

    return render(request,'vyama_page.html',{'cham':vyama})


def uwaka(request):
    uwaka_list =Uwaka.objects.all().order_by('-created_at')
    pic = CarourselUwaka.objects.first()

    paginator = Paginator(uwaka_list,9)
    page_number = request.GET.get('page')
    uwaka = paginator.get_page(page_number)

    return render(request,'uwaka.html',{'uwaka':uwaka,'pic':pic})

def uwaka_page(request,pk):
    uwaka = Uwaka.objects.get(id=pk)

    return render(request,'uwaka_page.html',{'uwaka':uwaka})


def wawata(request):
    wawata_list = Wawata.objects.all().order_by('-created_at')
    pic = CarourselWawata.objects.first()

    paginator = Paginator(wawata_list,9)
    page_number = request.GET.get('page')
    wawata = paginator.get_page(page_number)

    return render(request,'wawata.html',{'wawata':wawata,'pic':pic})

def wawata_page(request,pk):
    wawata = Wawata.objects.get(id=pk)

    return render(request,'wawata_page.html',{'wawata':wawata})


def viwawa(request):
    viwawa_list = Viwawa.objects.all().order_by('-created_at')
    pic = CarourselViwawa.objects.first()

    paginator = Paginator(viwawa_list ,9)
    page_number = request.GET.get('page')
    viwawa = paginator.get_page(page_number)

    return render(request,'viwawa.html',{'viwawa':viwawa,'pic':pic})

def ratiba(request):
    ratiba = Muda_wa_ibada.objects.first() 
    ofisini = Ratiba_za_ofisini.objects.first()
    maungamo = Muda_wa_Maungamo.objects.first()
    pic = CarourselRatiba.objects.first()

    return render(request,'ratiba.html',{'ratiba':ratiba,'ofisini':ofisini,'pic':pic,'maungamo':maungamo})

def viwawa_page(request,pk):

    viwawa = Viwawa.objects.get(id=pk)

    return render(request,'viwawa_page.html',{'viwawa':viwawa})

def kanda(request):
    kandaz_list = Kanda.objects.all().order_by('-created_at')
    pic = Carourselkanda.objects.first()

    paginator = Paginator(kandaz_list ,9)
    page_number = request.GET.get('page')
    kandaz = paginator.get_page(page_number)

    return render(request,'kanda.html',{'kandaz':kandaz,'pic':pic})

def kanda_page1(request,chape):
    kand = get_object_or_404(Kanda,id=chape)
    pages_list = kand.chama.all().order_by('-created_at')

    paginator = Paginator(pages_list ,9)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    
    return render(request,'kanda_page1.html',{'kand':kand,'pages':pages})

def kanda_page(request,chap):
    kanda = get_object_or_404(Kanda_page, id=chap)

    return render(request,'kanda_page.html',{'kand':kanda})
