from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Customer



class HomeView(TemplateView):
    template_name="home.html"

    def post(self, request):
            # check to see if loggin in
            user_name = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect("home")    
            else:
                messages.success(request, "There was An Error login in, please try again")
                return redirect("home")  
        
    def get(self, request):
        if str(request.user) == "AnonymousUser":
            return render(request, "home.html", {})
        name = str(request.user)
        customer = Customer.objects.get(username=name)
        return render(request, "home.html", {"customer": customer})

class LogoutUser(TemplateView):    
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out!")
        return redirect("home")  
    

class RegisterUser(TemplateView):
    # template_name="register.html"
    
    def post(self, request): 
        # Everything what user send pass to our SignUpForm
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate use and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            Customer.objects.create(username=user, email=user.email, first_name=user.first_name, last_name=user.last_name)
            messages.success(request,  "You have been sucesfuly logged in ")
            return redirect("home")
        return render(request, "register.html", {"form": form}) 

    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form}) 
