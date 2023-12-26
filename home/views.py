from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Hotel,Amenities
from django.db.models import Q
from django.core.paginator import Paginator

def hotel(request):
    amenities_objs = Amenities.objects.all()
    hotel_objs = Hotel.objects.all()
    
    # storing user search, sort data into a sortiable 
    sort = request.GET.get('sort')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')

    # Sort Function
    if sort:
        if sort == "ASC":
            hotel_objs = hotel_objs.order_by('hotel_price')
        elif sort =="DSC":
            hotel_objs = hotel_objs.order_by('-hotel_price')
            
    # Search Function
    if search:
        hotel_objs = hotel_objs.filter (
            Q(hotel_name__icontains = search) | # using Q objects for multiple search
            Q(room_count__icontains = search) |
            Q(description__icontains = search)
        )
        
    # amenities Function
    if amenities:
        hotel_objs = hotel_objs.filter(amenity_name__amenity_name__in = amenities).distinct()
        
        
    # Paginator Function
    # paginator = Paginator(hotel_objs, 4)  # Assuming 3 items per page
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
                
    context = {
        
        'amenities_objs':amenities_objs,
        'hotel_objs':hotel_objs,
        'sort':sort, 
        'search': search,
        'amenities':amenities
        
        }
    return render(request, 'index.html',context)

def login_page(request):
    if request.method != "POST":
        return render(request, "login.html")

    username = request.POST.get("Username")
    password = request.POST.get("Password")

    if not User.objects.filter(username=username).exists():
        messages.warning(request, "Please Create an Account First")
        return redirect("register")  # Redirect to the register page if the user doesn't exist

    user = authenticate(username=username, password=password)
    
    if user is None:
        messages.error(request, "Wrong Password")
        return redirect('login')  # Redirect back to login if the password is incorrect

    login(request, user)
    return redirect("hotel")

def register_page(request):
    if request.method != "POST":
        return render(request, "register.html")
    
    first_name = request.POST.get("Firstname")
    last_name = request.POST.get("Lastname")
    username = request.POST.get("Username")
    password = request.POST.get("Password")

    if User.objects.filter(username=username).exists():
        messages.info(request, "User Already exists")
        return redirect("login")  # Redirect to login if the user already exists
    
    user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
    user.set_password(password)
    user.save()
    messages.success(request, "Account created successfully")
    return redirect("login")
