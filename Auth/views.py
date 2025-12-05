from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
import json
from .decorators import csrf_required
from django.shortcuts import render

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

@csrf_exempt
@csrf_required
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"message": "Signup successful", "user": username})

    return JsonResponse({"error": "Invalid request"}, status=400)

def signup_view(request):
    if request.method == "GET":
        return render(request, "signup.html")


@csrf_exempt
@csrf_required
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": username})

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
