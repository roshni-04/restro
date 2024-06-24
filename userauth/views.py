import os
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
# ------ for authentication -----------
from django.contrib.auth import authenticate, login, logout

# ------ for menu forms -------------
from .forms import MenuForm

# ------ for custom user forms -------------
from .forms import CuisineForm
from .models import MenuItem

# ------ models ----
from .models import *
from home.models import Feedback

# =====================================================================================
#               AUTHENTICATION
# =====================================================================================

def signup_page(request):

    if request.method == "POST":
        uname = request.POST['txtUname']
        fname = request.POST['txtFname']
        lname = request.POST['txtLname']
        umail= request.POST['txtEmail']
        upass = request.POST['txtPass']
        uconfpass = request.POST['txtConfPass']


        myuser=User.objects.create_user(uname,umail,upass)
        myuser.first_name=fname
        myuser.last_name=lname


        myuser.save()

        messages.success(request, 'User Registered successfully')

    return render(request,'authentication/signup.html')

# Create your views here.


def login_user(request):
    
    if request.method == "POST":   # view function called by submitting a form
        uname = request.POST['txtUname']
        upass = request.POST['txtPass']

        myuser = authenticate(username = uname, password = upass)

        if myuser is None:  # authentication failed
            messages.warning(request, 'Incorrect credential. Please try again')
            return redirect('login')
        else:   # successful
            login(request, myuser)   # login
            messages.success(request, 'Login successfull')
            if myuser.is_staff:
                #return render(request, 'authentication/dashboard.html')

                return redirect('dashboard') # calls the view function responsible for rendering dashboard page after gathering required data 
            else:
                return redirect('show-reservation')


    return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'Logout successful')
    return redirect('home')

def dashboard_page(request):
    if request.user.is_authenticated:

        return redirect('show-reservation')
        """
        if request.user.is_staff:
            allfb=Feedback.objects.all()
            context={"feedbacks":allfb}
        return render(request, 'authentication/dashboard.html', context)
        """
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('home')
    
def changepass_user(request):

    if request.method == "POST":
        oldpass = request.POST['txtOPass']
        newpass = request.POST['txtNPass']
        confpass = request.POST['txtConfPass']
        uname = request.user.username # grab username of logged in user from session

        myuser = authenticate(username = uname, password = oldpass) # authenticate with current password
        
        if myuser is not None:  # authenticated
            
            myuser.set_password(newpass)
            myuser.save()

            messages.success(request, 'Password changed successfully')
            return redirect('dashboard')

    return render(request, 'authentication/change_pass.html')



# =====================================================================================
#               MENU
# =====================================================================================

def add_menu(request):

    if request.method == "POST":
        myform = MenuForm(request.POST)  # construct form object with passed data
        # myform = MenuForm(request.POST) --> for text only data 
        if myform.is_valid():
            myform.save()
            messages.info(request, 'Menu added successfully')
            return redirect('/restroapp/addmenu')
    else:
        myform = MenuForm()  # create a blank form
        ctx = {'my_form': myform}
        return render(request, 'menu/addmenu.html', ctx)
    

def show_menu(request):
    menu_list = MenuItem.objects.all()
    return render(request, 'menu/showmenu.html', {'menu' : menu_list})
    
    
# =====================================================================================
#               CUISINES
# =====================================================================================

def add_cuisines(request):

    if request.method == "POST":
        myform = CuisineForm(request.POST, request.FILES)  # construct form object with passed data
        # myform = CuisineForm(request.POST) --> for text only data 
        if myform.is_valid():
            myform.save()
            messages.info(request, 'Cuisine added successfully')
            return redirect('/restroapp/addcuisine')
    else:
        myform = CuisineForm()  # create a blank form
        ctx = {'my_form': myform}
        return render(request, 'cuisines/addcuisines.html', ctx)
    

def show_cuisines(request):
    cuisine_list = Cuisine.objects.all()
    return render(request, 'cuisines/showcuisines.html', {'cuisines' : cuisine_list})

def edit_cuisines(request, cid):
    # Grab the object details which is under process
    selected_cuisine = Cuisine.objects.get(id = cid) # ****** where id = 1
    myform = CuisineForm(request.POST or None, request.FILES or None, instance=selected_cuisine)

    if request.method == "POST":
        if myform.is_valid():
            myform.save()
            messages.info(request, 'Cuisine editted successfully')
            return redirect('show-cuisine')
    # present a form with data filled up
    return render(request, 'cuisines/editcuisine.html', {'my_form': myform})

def delete_cuisines(request, cid):
    # Grab the object details which is under process
    selected_cuisine = Cuisine.objects.get(id = cid) # ****** where id = 1
    selected_cuisine.delete()
    
    # delete the image from disk
    os.remove(selected_cuisine.img.path)  # give path while deletion

    messages.info(request, 'Cuisine deleted successfully')
    return redirect('show-cuisine')



def edit_menu(request, mid):
    # Grab the object details which is under process
    selected_menu = MenuItem.objects.get(menu_id = mid) # ****** where id = 1
    myform = MenuForm(request.POST or None, instance=selected_menu)

    if request.method == "POST":
        if myform.is_valid():
            myform.save()
            messages.info(request, 'Menu editted successfully')
            return redirect('show-menu')
    # present a form with data filled up
    return render(request, 'menu/editmenu.html', {'my_form': myform})

def delete_menu(request, mid):
    # Grab the object details which is under process
    selected_menu = MenuItem.objects.get(menu_id = mid) # ****** where id = 1
    selected_menu.delete()
    
    

    messages.info(request, 'Menu item deleted successfully')
    return redirect('show-menu')


def menubycat(request,cid):
    select_menu=MenuItem.objects.filter(cuisine_cat=cid) #get all the menu items for the selected cuisine
    select_cuisine=Cuisine.objects.get(id=cid)#get the selected cuisine details
    return render(request,'menu/showmenubycat.html',{ 'menulist':select_menu, 'cuisine':select_cuisine})

def search_results(request):
    query = request.GET.get('q')

    if query:
        results = MenuItem.objects.filter(name__icontains=query)
        
    else:
        results = []

    return render(request, 'menu/search_results.html', {'results': results, 'query': query})



