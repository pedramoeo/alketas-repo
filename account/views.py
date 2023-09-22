from django.shortcuts import render, redirect

from .forms import *
from .models import  *
from .serializers import *

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated






# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # at first we save user's data
            form.save()
            """
            then we create an authentification token for the first time using
            their username and password
            """
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # after authentification, we automatically log the user into their account
            login(request, user)
            # then we redirect them to their profile dashboard
            return redirect('dashboard', parameters='dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})




@api_view(['GET', 'POST'])
def signup_view_api(request):
    if request.method == "POST":
        form = SignUpForm(request.data)  # Use request.data instead of request.POST
        if form.is_valid():
            # ... rest of your code ...
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)  # Return form.errors
    else:
        form = SignUpForm()
    return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)







def login_view(request):
    if request.method == "GET":
        form = LogInForm()
        return render(request, 'login.html', {'form':form})

    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():  # Validate the form first
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard/')
        return HttpResponse("failed to log in")

@csrf_exempt
@api_view(['GET', 'POST'])
def login_api_view(request):
    if request.method == 'GET':
        form = LogInForm()
        return Response({"form": {"username": "", "password": ""}}, status=status.HTTP_200_OK)
        
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid data", "errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)







def logout_view(request):
    logout(request)
    return redirect('home')



@api_view(['GET'])
def logout_api_view(request):
    logout(request)
    return Response({"message": "logged out successfully"}, status=status.HTTP_200_OK)






class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'dashboard.html'
    success_url = 'profile-update'

    """
    a function to only call the specific user's data
    it's like shouting "GIVE ME ALL THIS USER'S DATA FIRST!!"
    """
    def get_object(self):
        return self.request.user

    def get_context_data(self, request, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user)
        context['profile_picture'] = user.profile.profile_picture
        return context

    # handle all post requests in views.py first

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if 'delete_account' in request.POST:
            delete_account_form = DeleteAccountForm(request.POST)
            if delete_account_form.is_valid:
                entered_password = delete_account_form.cleaned_data.get('password')
                if user.check_password(entered_password):
                    user.delete()
                    messages.success('account has been successfully deleted!')
                    return redirect('home')
                else:
                    messages.error('Invalid Password.')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success('Password has been successfully changes.')
                return redirect('dashboard', kwargs = {'parameters':'password_changed'})
            else:
                return self.form_invalid(password_form)



    """
    ***** below is how you merge multiple classes from
    ***** forms.py in a single view
    """

    # handle post requests regarding the forms.py

    def get_form_class(self):
        if 'email' in self.request.POST:
            return ChangeEmailForm
        elif 'profile_picture' in self.request.POST:
            return ProfilePictureForm

    def form_valid(self, form):
        if isinstance(form, ChangeEmailForm):
            email = form.cleaned_data['email']
            user = self.request.user
            user.email = email
            user.save()

        elif isinstance(form, ProfilePictureForm):
            profile_picture = form.cleaned_data['profile_picture']
            user = self.request.user
            user.profile.profile_picture = profile_picture
            user.profile.save()
        return super().form_valid(form)



class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'profile_picture': user.profile.profile_picture.url if user.profile.profile_picture else None,
        })

    def post(self, request):
        user = request.user
        if 'delete_account' in request.data:
            form = DeleteAccountForm(request.data)
            if form.is_valid():
                entered_password = form.cleaned_data.get('password')
                if user.check_password(entered_password):
                    user.delete()
                    return Response({"message": "Account has been successfully deleted!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid Password."}, status=status.HTTP_400_BAD_REQUEST)

        elif 'change_password' in request.data:
            form = PasswordChangeForm(user, request.data)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                return Response({"message": "Password has been successfully changed."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed to change password."}, status=status.HTTP_400_BAD_REQUEST)

        elif 'email' in request.data:
            form = ChangeEmailForm(request.data)
            if form.is_valid():
                email = form.cleaned_data['email']
                user.email = email
                user.save()
                return Response({"message": "Email has been successfully changed."}, status=status.HTTP_200_OK)

        elif 'profile_picture' in request.data:
            form = ProfilePictureForm(request.data)
            if form.is_valid():
                profile_picture = form.cleaned_data['profile_picture']
                user.profile.profile_picture = profile_picture
                user.profile.save()
                return Response({"message": "Profile picture has been successfully changed."}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)