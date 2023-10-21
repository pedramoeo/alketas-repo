from django.shortcuts import render, redirect

from .forms import *
from .models import  *

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from django.http import HttpResponse, JsonResponse
from django.views.generic import View, FormView


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator





from django.contrib.auth import get_user_model




User = get_user_model()







@method_decorator(csrf_exempt, name='dispatch')
class SignupView(FormView):
    form_class = SignUpForm
    template_name = "signup.html"

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
        else:
            return JsonResponse({"Message": "Invalid username or password."}, status=400)

    
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)





@method_decorator(csrf_exempt, name='dispatch')
class LoginView(FormView):
    form_class = LogInForm
    template_name = "login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('/home')
        else:
            return JsonResponse({"Message": "Invalid Username or Password"})
        
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)




def logout(request):
    """
    imported logout as auth_logout because it'd interfere 
    with the function name
    """
    auth_logout(request)
    return redirect('/login')








class ProfileView(View):
    def get(self, request):
        user = self.request.user
        form = ChangeEmailForm()
        form2 = ChangePasswordForm()
        form3 = DeleteAccountForm()

        context = {
            "username": user.username,
            "email": user.email,
            "form": form,
            "form2": form2,
            "form3": form3,
        }
        return render(request, "dashboard.html", context)


    def post(self, request, *args, **kwargs):
        user = self.request.user

        if "change_email" in request.POST:
            form = ChangeEmailForm(request.POST)
            if form.is_valid():
                new_email = form.cleaned_data.get('email')  # Fixed this line
                user.email = new_email
                user.save()
                return redirect('dashboard')
            else:
                context = {
                        "username": user.username,
                        "email": user.email,
                        "form": form,
                        "form2": ChangePasswordForm(),
                        "form3": DeleteAccountForm(),
                    }
                return render(request, "dashboard.html", context)

        elif "change_password" in request.POST:
            form2 = ChangePasswordForm(request.POST)
            if form2.is_valid():
                new_password = form2.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()
                return redirect('dashboard')
            else:
                context = {
                    "username": user.username,
                    "email": user.email,
                    "form": ChangeEmailForm(),
                    "form2": form2,
                    "form3": DeleteAccountForm(),
                }
                return render(request, "dashboard.html", context)

        elif "delete_account" in request.POST:
            form3 = DeleteAccountForm(request.POST)
            if form3.is_valid():
                password = form3.cleaned_data.get('password')
                if check_password(password, user.password):
                    user.delete()
                    return redirect('login')  # Redirect to login after account deletion
                else:
                    messages.error(request, "Wrong Password!")
            else:
                context = {
                    "username": user.username,
                    "email": user.email,
                    "form": ChangeEmailForm(),
                    "form2": ChangePasswordForm(),
                    "form3": form3,
                }
                return render(request, "dashboard.html", context)

        # Default return statement
        return redirect('dashboard')

