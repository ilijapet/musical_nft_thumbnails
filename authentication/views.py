from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.models import User



class HomeView(TemplateView):
    template_name="home.html"
    # template_name="navbar.html"
       
    def post(self, request):
        # check to see if loggin in
        if request.method == "POST":
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
        else:
            return render(request, "home.html", {})
        



class LogoutUser(TemplateView):
    
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out!")
        return redirect("home")  
