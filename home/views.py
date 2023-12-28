from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import (Hotel,Amenities,Cities,HotelBooking)
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def check_booking(request,checkin,checkout,uid, room_count):
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
    qs = HotelBooking.objects.filter(
        start_date__lte = checkin,
        end_date__gte = checkout,
        hotel__uid = uid
    )
    if len(qs) >= room_count:
        return False
    else:
        return True
    
def check_dates(request):
    pass

def hotel(request):
    
    # Fetching data from models
    amenities_objs = Amenities.objects.all()
    hotel_objs = Hotel.objects.all()  
    city_objs = Cities.objects.all()
    
    # storing user search, sort data into a sortiable 
    sort = request.GET.get('sort')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    
    checkin = request.POST.get('checkin')
    checkout = request.POST.get('checkout')
        
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
        
    # Paginator Code
    page = request.GET.get('page', 1)
    paginator = Paginator(hotel_objs, 3)
    
    try:
        queryset = paginator.get_page(page)
        print(queryset)
    except PageNotAnInteger:
        queryset = paginator.get_page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    # print(paginator.count)    # tell total items
    # print(paginator.num_pages)  # tell total number of pages
                 
    context = {
        
        'amenities_objs':amenities_objs,
        'sort':sort, 
        'search': search,
        'amenities':amenities,
        'city_objs':city_objs,
        'queryset':queryset
        
        }
    
    return render(request, 'index.html',context)

def hotel_details(request, uid):
    hotel_obj = Hotel.objects.get(uid=uid)

    if request.method == "POST":
        checkin = request.POST.get("checkin")
        checkout = request.POST.get('checkout')
        hotel = Hotel.objects.get(uid=uid)
        room_count = hotel.room_count  # Fetch room_count from the hotel object
        
        if not check_booking(request, checkin, checkout, uid, room_count):  # Pass room_count here
            messages.warning(request, "Hotel is booked in these days")
        else:
            HotelBooking.objects.create(
                hotel=hotel,
                user=request.user,
                start_date=checkin,
                end_date=checkout,
                booking_type='pre paid'
            )
            messages.info(request, "Your Hotel has been Booked successfully")

    context = {'hotel_obj': hotel_obj}
    return render(request, "hotel_details.html", context)





def login_page(request):  # sourcery skip: assign-if-exp, use-named-expression
    
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
    
    
    # This code checks if there's a 'next' parameter in the URL. If it exists:
    # It redirects the user to the URL specified in the 'next' parameter after a successful login.
    # If 'next' is not set, it redirects the user to the default page (/hotel/).
    
    redirect_url = request.GET.get('next') 
    if redirect_url:
        return redirect(redirect_url)
    else:
        return redirect('/hotel/')  

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

def log_out(request):
    
    logout(request)
    return redirect('hotel')
    