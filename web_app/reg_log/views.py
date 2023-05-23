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
from .models import Users

global mydict
from django.db.models import F


def reg_log(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/reg_log.html', {'balance': user.Balance})
    return render(request, 'reg_log/reg_log.html')


# def create_DB():
#     try:
#         con = sql.connect('../third.db')
#
#         with con:
#             con.execute("""
#                     CREATE TABLE IF NOT EXISTS users (
#                         ID INTEGER PRIMARY KEY,
#                         Name STRING,
#                         Surname STRING,
#                         Email STRING,
#                         Password STRING,
#                         Date_of_birth STRING,
#                         Face STRING,
#                         Balance INTEGER
#             );
#                 """)
#         con.commit()
#
#         with con:
#             con.execute("""
#                     CREATE TABLE IF NOT EXISTS goods (
#                         ID INTEGER PRIMARY KEY,
#                         Name STRING,
#                         Manufacturer STRING,
#                         Price INTEGER,
#                         Quantity INTEGER
#             );
#                 """)
#         con.commit()
#
#         with con:
#             con.execute("""
#                     CREATE TABLE IF NOT EXISTS cart (
#                         buyer_id INTEGER,
#                         cart JSON,
#                         status JSON,
#                         FOREIGN KEY (buyer_id) REFERENCES users(ID)
#             );
#                 """)
#
#         con.commit()
#
#     except sql.Error as error:
#         print("Ошибка при подключении к sqlite", error)
#
#     finally:
#         if (con):
#             data = {'id': 0, 'name': 'Tim', 'surname': 'Sosnin', 'email': 'tim_sosnin@gmail.com', 'pass': '111111',
#                     'age': '18',
#                     'face': 'https://downloader.disk.yandex.ru/disk/4d77d064cf44808a14da8b851d29f202b687fce56da06602bde6bb80f8753aac/6435ae94/x6m59NaE7ol88Bg7tK2hR7bVlGtc-zjn96Uvws9cyrXsxfvsKI0Mzy3B37Rse4p3ludyYMUkyNOWPbqaVL90SA%3D%3D?uid=1768214715&filename=_tim.sosnin%40gmail.com&disposition=attachment&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=1768214715&fsize=73890&hid=7a25bd8167b22e519a4baf422147c5c4&media_type=executable&tknv=v2&etag=5be1cfd70f7128d8350fce0846adb876'}
#             query = f"INSERT INTO users VALUES ('{data['id']}', '{data['name']}', '{data['surname']}', '{data['email']}', '{data['pass']}', '{data['dob']}', '{data['face']}', {0})"
#             cur = con.cursor()
#             cur.execute(query)
#             con.commit()
#             con.close()
#             print("Соединение с SQLite закрыто")


# def reg(request):
# if request.method == "POST":
#     name = request.POST['name']
#     surname = request.POST['surname']
#     age = request.POST['age']
#     email = request.POST['email']
#     pass1 = request.POST['pass1']
#     pass2 = request.POST['pass2']

# if user.objects.filter(email=User.email).exists():
#     messages.error(request, "Email Already Registered!!")
#     return redirect('reg')
#
# if user.pass1 != pass2:
#     messages.error(request, "Passwords didn't matched!!")
#     return redirect('reg')
#
# if not user.name.isalnum():
#     messages.error(request, "Username must be Alpha-Numeric!!")
#     return redirect('reg')
#
# if not user.surname.isalnum():
#     messages.error(request, "Surname must be Alpha-Numeric!!")
#     return redirect('reg')
#
# if not user.age.isalnum():
#     messages.error(request, "Age must be Alpha-Numeric!!")
#     return redirect('reg')

# con = sql.connect('../third.db')
# curs = con.cursor()
# query = "SELECT ID FROM users ORDER BY ID DESC LIMIT 1"
# res = curs.execute(query)
# if res.fetchone()[0] == 0:
#     create_DB()
# res = curs.execute(query)
# prev_user_id = res.fetchone()[0]
# user.ID = prev_user_id + 1
# curs.close()
# con.close()
# user = User.objects.create_user(name, surname, age, email, pass1)
# user.save()
# messages.success(request, "ЩИИИЩ, ты успешно балдежнул!")
# user = authenticate(username=user.email, password=user.pass1) пока не знаю надо ли
# login(request, user)
#     return render(request, 'home')
# else:
#     return render(request, 'reg_log/reg.html')

def reg(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.Face = 'ooo'
            user.Balance = 0

            if User.objects.filter(email=user.Email).exists():
                # TODO: сделать нормальную обработку ошибок
                return redirect('home')

            if user.Pass1 != user.Pass2:
                # TODO: сделать нормальную обработку ошибок
                return redirect('reg')

            myuser = User.objects.create_user(username=user.Email, password=user.Pass1)
            myuser.first_name = user.Name
            myuser.save()
            user.ID = myuser.id
            au_user = authenticate(username=user.Email, password=user.Pass1)
            login(request, au_user)
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
