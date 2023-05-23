from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from reg_log.models import Users


def lk(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'lk/lk.html', {'balance': user.Balance})
    return render(request, 'lk/lk.html')


def out(request):
    logout(request)
    return redirect('reg_log/home')
