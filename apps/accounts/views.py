from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not password or not username:
            return HttpResponse('Parol yoki nom maydoni bosh')
        if User.objects.filter(username = username).exists():
            return HttpResponse('Bunday username ga ega foydalanuvchi allaqachon bor')
        user = User.objects.create_user(username=username, password = password)
        login(request, user)
        return redirect('product_list')
    return render(request, 'accounts/auth_form.html', {'mode': 'register'})
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not password or not username:
            return HttpResponse('Qaysidir maydon bosh')
        user = authenticate(request, username = username, password=password)
        if user is None:
            return HttpResponse('Kechirasiz bunday user yoq')
        login(request, user)
        return redirect('product_list')
    return render(request, 'accounts/auth_form.html', {'mode': 'login'})
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




