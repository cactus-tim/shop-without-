from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from reg_log.models import Users
import yadisk


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
        if flag:
            return False


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
            if try_upload(disk, path, filename):
                link = disk.get_download_link(filename)
                return link
            else:
                return 'Error'
    else:
        return 'Error'


def lk(request):
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

        return render(request, 'lk/lk.html', {'balance': user.Balance})
    return render(request, 'lk/lk.html')


def out(request):
    logout(request)
    return redirect('reg_log/home')
