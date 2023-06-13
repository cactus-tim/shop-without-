from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegForm, UserLogForm
import yadisk
from .models import Users
from imutils import paths
import face_recognition
import pickle
import cv2
import os
import shutil


def enc():
    imagePaths = list(paths.list_images('images'))
    knownEncodings = []
    knownNames = []
    for (i, imagePath) in enumerate(imagePaths):
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()


def try_upload(disk, path, filename):
    try:
        if disk.exists('/face_enc'):
            disk.remove('/face_enc')
        disk.upload(path, filename)
        if disk.exists(filename):

            os.mkdir('images')
            photos = disk.get_last_uploaded()
            for photo in photos:
                if photo.name == 'face_enc':
                    continue
                p = 'images/' + photo.name
                os.mkdir(p)
                name = photo.path
                p += '/' + photo.name + '.jpg'
                disk.download(name, p)

            enc()

            shutil.rmtree('images')

            p1 = 'face_enc'
            f1 = '/face_enc'
            disk.upload(p1, f1)
            os.remove('face_enc')
    except Exception as ex:
        print(ex)


def photo_to_cloud(path, email):
    client_id = "9ccafedf10664913b01666dbceb950b1"
    secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
    token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"

    disk = yadisk.YaDisk(client_id, secret_id, token)

    link = ''

    if disk.check_token():
        filename = '/' + email
        if disk.exists(filename):
            link = disk.get_download_link(filename)
            return link
        else:
            try_upload(disk, path, filename)
            if disk.exists(filename):
                link = disk.get_download_link(filename)
                return link
            else:
                return 'Error'
    else:
        return 'Error'


def reg_log(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/reg_log.html', {'balance': user.Balance})
    return render(request, 'reg_log/reg_log.html')


def valid(user, myuser):
    pass


def reg(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserRegForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.FaceLink = user.Face.path
            user.Balance = 0

            if User.objects.filter(username=user.Email).exists():
                # TODO: сделать нормальную обработку ошибок
                return redirect('home')

            if user.Pass1 != user.Pass2:
                # TODO: сделать нормальную обработку ошибок
                return redirect('reg')

            myuser = User.objects.create_user(username=user.Email, password=user.Pass1)
            myuser.first_name = user.Name
            user.id = myuser.id
            au_user = authenticate(username=user.Email, password=user.Pass1)
            login(request, au_user)
            valid(user, myuser)
            myuser.save()
            user.save()
            return redirect('profile')
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
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/footer.html', {'balance': user.Balance})
    return render(request, 'reg_log/footer.html')


def politics(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/politics.html', {'balance': user.Balance})
    return render(request, 'reg_log/politics.html')


def katalog(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/katalog.html', {'balance': user.Balance})
    return render(request, 'reg_log/katalog.html')


def LichnyK(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/lk.html', {'balance': user.Balance})
    return render(request, 'lk/lk.html')


@login_required
def balance(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        if request.method == 'POST':
            add_balance = request.POST.get('custom-amount-input')
            user.Balance += int(add_balance)
            user.save()
        return render(request, 'reg_log/balance.html', {'balance': user.Balance})
    return render(request, 'reg_log/balance.html')


@login_required
def profile(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)

        path = user.FaceLink
        user.FaceLink = photo_to_cloud(path, user.Email)
        if user.FaceLink == 'Error':
            user.delete()
            request.user.delete()
            # надо заново регаться
            # TODO: сделать нормальную обработку ошибок
            return redirect('home')
        else:
            user.save()

        data = {
            'balance': user.Balance,
            'user': user
        }

        return render(request, 'reg_log/profile.html', data)
    return render(request, 'reg_log/profile.html')


def how_to_use(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/how_to_use.html', {'balance': user.Balance})
    return render(request, 'reg_log/how_to_use.html')


def akcii(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/akcii.html', {'balance': user.Balance})
    return render(request, 'reg_log/akcii.html')
