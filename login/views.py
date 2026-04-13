from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout as auth_logout
import requests
from django.conf import settings
from .forms import UserForm, CarForm
from .models import User, cars
from django.contrib import messages
import random
from django.views.decorators.csrf import csrf_exempt
def _send_otp_email(to_email, otp):
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        },
        json={
            "sender": {
                "name": settings.BREVO_SENDER_NAME,
                "email": settings.BREVO_SENDER_EMAIL
            },
            "to": [{"email": to_email}],
            "subject": "Your Fairy Club Verification Code",
            "textContent": f"Your OTP is: {otp}\n\nThis code expires in 5 minutes.",
        }
    )
    print("Brevo response:", response.status_code, response.text)





def members(request):
    form = UserForm()
    return render(request, 'signup.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone_number')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'signup.html', {'form': form})

            if phone and User.objects.filter(phone_number=phone).exists():
                messages.error(request, 'Phone number already exists.')
                return render(request, 'signup.html', {'form': form})

            otp = str(random.randint(100000, 999999))

            # Store registration data in session — do NOT save to DB yet
            request.session['pending_user'] = {
                'username': form.cleaned_data.get('username'),
                'email': email,
                'password': form.cleaned_data['password'],
                'otp': otp,
            }
            request.session['verify_email'] = email

            print(f"\n[DEV] OTP for {email}: {otp}\n")
            _send_otp_email(email, otp)
            return redirect('verify_otp')

    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})

def home(request):
    featured_cars = cars.objects.filter(is_approved=True).order_by('-created_at')[:6]
    makes = cars.objects.filter(is_approved=True).values_list('make', flat=True).distinct()
    years = cars.objects.filter(is_approved=True).values_list('year', flat=True).distinct().order_by('-year')
    total_listings = cars.objects.filter(is_approved=True).count()
    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'makes': makes,
        'years': years,
        'total_listings': total_listings,
    })

def listings(request):
    return render(request, 'listings.html')

def sell(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to sell a car.')
            return redirect('login')

        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user

            images = request.FILES.getlist('images')
            if images:
                try:
                    main_index = int(request.POST.get('main_image_index', 0))
                except (ValueError, TypeError):
                    main_index = 0
                if main_index >= len(images):
                    main_index = 0
                car.image = images[main_index]

            car.save()
            messages.success(request, 'Car listed successfully!')
            return redirect('dashboard')
        return render(request, 'sell.html', {'form': form})

    form = CarForm()
    return render(request, 'sell.html', {'form': form})

def financing(request):
    return render(request, 'financing.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    user_cars = cars.objects.filter(owner=request.user) if request.user.is_authenticated else []
    return render(request, 'dashboard.html', {'user_cars': user_cars})

def edit_car(request, pk):
    car = cars.objects.get(pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            updated = form.save(commit=False)

            images = request.FILES.getlist('images')
            if images:
                try:
                    main_index = int(request.POST.get('main_image_index', 0))
                except (ValueError, TypeError):
                    main_index = 0
                if main_index >= len(images):
                    main_index = 0
                updated.image = images[main_index]

            updated.save()
            messages.success(request, 'Car updated successfully!')
            return redirect('dashboard')
        return render(request, 'sell.html', {'form': form})

    form = CarForm(instance=car)
    return render(request, 'sell.html', {'form': form})

def delete_car(request, pk):
    car = cars.objects.get(pk=pk, owner=request.user)
    car.delete()
    messages.success(request, 'Car deleted successfully.')
    return redirect('dashboard')

def update_profile(request):
    return render(request, 'update_profile.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
          
        user = User.objects.filter(email=email).first()
        
        if not user:
            print(f"[DEV] Login failed: no user found with email={email}")
            messages.error(request, 'Invalid email or password.')
        elif not user.check_password(password):
            print(f"[DEV] Login failed: wrong password for email={email}")
            messages.error(request, 'Invalid email or password.')
        elif user.user_type == 1:
                login(request, user)
                return redirect('/admin/')
        elif not user.is_verified:
            print(f"[DEV] Login failed: user not verified email={email}")
            messages.error(request, 'Account verification has been removed contact admin.')
        else:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
  
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('home')

def search(request):
    return render(request, 'search.html')

def car_detail(request, pk):
    car = cars.objects.filter(pk=pk, is_approved=True).first() 
    similar_cars = cars.objects.filter(make=car.make, is_approved=True).exclude(pk=pk)[:4]
    return render(request, 'car_detail.html', {'pk': pk, 'car': car, 'similar_cars': similar_cars})

def compare(request):
    return render(request, 'compare.html')

def careers(request):
    return render(request, 'careers.html')

def press(request):
    return render(request, 'press.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def refund(request):
    return render(request, 'refund.html')

@csrf_exempt
def resend_otp(request):
    if request.method == 'POST':
        email = request.session.get('verify_email')
        pending = request.session.get('pending_user')
        if not email or not pending:
            messages.error(request, 'Session expired. Please signup again.')

        new_otp = str(random.randint(100000, 999999))
        pending['otp'] = new_otp
        request.session['pending_user'] = pending  

        _send_otp_email(email, new_otp)
        messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('verify_otp')

@csrf_exempt
def verify_otp(request):
    email = request.session.get('verify_email')
    pending = request.session.get('pending_user')

    if not email or not pending:
        messages.error(request, 'Session expired. Please signup again.')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == pending['otp']:
           
            user = User(
                username=pending.get('username'),
                email=pending['email'],
                is_verified=True,
            )
            user.set_password(pending['password'])
            user.save()

            del request.session['pending_user']
            del request.session['verify_email']

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid OTP.')

    return render(request, 'verify_otp.html')