from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from reg_log.models import Users, Cart, Good
import yadisk
from pyzbar.pyzbar import decode
import cv2
import pandas as np


class Product:
    def __init__(self, name, cost, count, amount):
        self.name = name
        self.cost = cost
        self.count = count
        self.amount = amount


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


def from_bd(BarCode):
    pass


def camera_work(request):
    print("OK")
    barCode = -1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        # чтение с камеры
        ret, frame = cap.read()
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # декодинг
        decodedObjects = decode(im)

        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # выделяет сам qr код в квадрат(немного магии)
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
            barCode = int(decodedObject.data)

            if barCode != -1:
                print(barCode)
                update_cart(request.user.id, barCode)
                return redirect('lk')
            else:
                return redirect('lk')


def update_cart(buyer_id, good):
    good_id = str(good)
    if Cart.objects.filter(buyer_id=buyer_id).exists():
        cart = Cart.objects.get(buyer_id=buyer_id)
        if good_id in cart.cart:
            cart.cart[good_id] += 1
        else:
            cart.cart[good_id] = 1
        cart.save()
        print(cart.cart)
    else:
        cart_data = {good_id: 1}
        cart = Cart(buyer_id=buyer_id, cart=cart_data, status=True)
        cart.save()
        print(cart.cart)


@login_required
def lk(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        if Cart.objects.filter(buyer_id=request.user.id).exists():
            cart = Cart.objects.get(buyer_id=request.user.id)
            products = []
            for key, value in cart.cart.items():
                products.append(Product(Good.objects.get(id=int(key)).title,
                                        Good.objects.get(id=int(key)).price,
                                        value,
                                        Good.objects.get(id=int(key)).price * value))

            data = {
                'balance': user.Balance,
                'products': products
            }

            return render(request, 'lk/lk.html', data)

        else:
            data = {
                'balance': user.Balance,
                'products': []
            }

            return render(request, 'lk/lk.html', data)

        # path = user.FaceLink
        # user.FaceLink = photo_to_cloud(path, user.Email)
        # if user.FaceLink == 'Error':
        #     user.delete()
        #     request.user.delete()
        #     # надо заново регаться
        #     # TODO: сделать нормальную обработку ошибок
        #     return redirect('home')

    return render(request, 'lk/lk.html')


def out(request):
    logout(request)
    return redirect('reg_log/home')
