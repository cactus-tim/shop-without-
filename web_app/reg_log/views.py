from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.backends import sqlite3
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import sqlite3 as sql
from .forms import UserRegForm, UserLogForm
import yadisk
from .models import Users

from django.db.models import F


def reg_log(request):
    # if request.user.is_authenticated:
    #     user = Users.objects.get(id=request.user.id)
    #     return render(request, 'reg_log/reg_log.html', {'balance': user.Balance})
    return render(request, 'reg_log/reg_log.html')


def try_upload(disk, path, filename):
    flag = False
    for i in range(1, 101):
        try:
            disk.upload(path, filename)
            if disk.exists(filename):
                flag = True
                return True
        except Exception as ex:
            print(ex)
    if not flag:
        return False


def photo_to_cloud(path, email):
    client_id = "9ccafedf10664913b01666dbceb950b1"
    secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
    token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"

    disk = yadisk.YaDisk(client_id, secret_id, token)

    link = ''

    if disk.check_token():
        filename = '/' + email
        if try_upload(disk, path, filename):
            link = disk.get_download_link(filename)
            return link
        else:
            return 'Error'
    else:
        return 'Error'


def reg(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserRegForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            path = user.Face.path[0:62] + 'images/' + user.Face.path[62:].replace(' ', '_')
            #если поменяем путь, надо менять
            user.FaceLink = photo_to_cloud(path, user.Email)
            if user.FaceLink == 'Error':
                # TODO: сделать нормальную обработку ошибок
                return redirect('home')

            user.Balance = 0

            if User.objects.filter(username=user.Email).exists():
                # TODO: сделать нормальную обработку ошибок
                return redirect('home')

            if user.Pass1 != user.Pass2:
                # TODO: сделать нормальную обработку ошибок
                return redirect('reg')

            myuser = User.objects.create_user(username=user.Email, password=user.Pass1)
            myuser.first_name = user.Name
            myuser.save()
            user.id = myuser.id
            au_user = authenticate(username=user.Email, password=user.Pass1)
            login(request, au_user)
            myuser.save()
            user.save()
            return redirect('lk')
        else:
            error = "Форма заполненна неправильно"

    form = UserRegForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'reg_log/reg.html', data)


def log(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserLogForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            au_user = authenticate(username=user.Email, password=user.Pass1)
            if au_user is not None:
                login(request, au_user)
                return redirect('lk')
            else:
                error = "Неверный логин или пароль"
        else:
            error = "Форма заполненна неправильно"

    form = UserLogForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'reg_log/log.html', data)


def out(request):
    logout(request)
    return redirect('home')


def footer(request):
    return render(request, 'reg_log/footer.html')


def politics(request):
    return render(request, 'reg_log/politics.html')
