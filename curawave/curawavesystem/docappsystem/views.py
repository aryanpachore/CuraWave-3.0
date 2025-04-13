from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()

def BASE(request):
    return render(request,'base.html')

def LOGIN(request):
    return render(request,'login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password')
            return redirect('login')
            
        try:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_type = user.user_type
                    
                    if user_type == '1':
                        return redirect('admin_home')
                    elif user_type == '2':
                        return redirect('doctor_home')
                    elif user_type == '3':
                        return redirect('user_home')
                    else:
                        messages.error(request, 'Invalid user type')
                        return redirect('login')
                else:
                    messages.error(request, 'Your account is not active')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
                
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('login')
            
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request,'profile.html',context)

@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #username = request.POST.get('username')
        email = request.POST.get('email')
        #password = request.POST.get('password')
        print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            #customuser.username = username
            
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            
            customuser.save()
            messages.success(request,'Your Profile Updated Successfully!')
            return redirect('profile')
        except:
            messages.error(request,'Failed to Update Your Profile')

    return render(request,'profile.html')

def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id = request.user.id)
     
    if len(ch) > 0:
        data = User.objects.get(id = request.user.id)
        context["data"] = data            
    if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request,'Password Changed Successfully!')
            user = User.objects.get(username=un)
            login(request,user)
        else:
            messages.error(request,'Current Password is incorrect!')
            return redirect("change_password")
    return render(request,'change-password.html', context)
