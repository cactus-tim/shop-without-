from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from reg_log.models import Users, Good, Cart
import yadisk
from pyzbar.pyzbar import decode
import cv2
import pandas as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class Product:
    def __init__(self, name, cost, count, amount):
        self.name = name
        self.cost = cost
        self.count = count
        self.amount = amount


class HistoryCart:
    def __init__(self, id, names, counts, amount):
        self.id = id
        self.names = names
        self.counts = counts
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
    if Cart.objects.filter(buyer_id=buyer_id, status=True).exists():
        cart = Cart.objects.filter(buyer_id=buyer_id, status=True).first()
        price = Good.objects.get(id=good).price
        if good_id in cart.cart:
            cart.cart[good_id] += 1
        else:
            cart.cart[good_id] = 1
        cart.total += price
        cart.save()
        print(cart.cart)
    else:
        cart_data = {good_id: 1}
        price = Good.objects.get(id=good).price
        cart = Cart(buyer_id=buyer_id, cart=cart_data, total=price, status=True)
        user = Users.objects.get(id=buyer_id)
        cart.save()
        print(cart.cart)


@login_required
def lk(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        if Cart.objects.filter(buyer_id=request.user.id, status=True).exists():
            cart = Cart.objects.filter(buyer_id=request.user.id, status=True).first()
            products = []
            for key, value in cart.cart.items():
                products.append(Product(Good.objects.get(id=int(key)).title,
                                        Good.objects.get(id=int(key)).price,
                                        value,
                                        Good.objects.get(id=int(key)).price * value))

            data = {
                'balance': user.Balance,
                'products': products,
                'total': cart.total
            }

            return render(request, 'lk/lk.html', data)

        else:
            data = {
                'balance': user.Balance,
                'products': [],
                'total': '0'
            }

            return render(request, 'lk/lk.html', data)

    return render(request, 'lk/lk.html')


def out(request):
    logout(request)
    return redirect('reg_log/home')


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
    return render(request, 'reg_log/lk.html')


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

        data = {
            'balance': user.Balance,
            'user': user
        }

        return render(request, 'reg_log/profile.html', data)
    return render(request, 'reg_log/profile.html')


@login_required
def history(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        carts = Cart.objects.filter(buyer_id=request.user.id, status=False)
        historycarts = []
        for cart in carts:
            names = []
            counts = []
            for key, value in cart.cart.items():
                names.append(Good.objects.get(id=int(key)).title)
                counts.append(value)
            historycarts.append(HistoryCart(cart.id, names, counts, cart.total))

        data = {
            'balance': user.Balance,
            'historycarts': historycarts
        }

        return render(request, 'lk/history.html', data)
    return render(request, 'lk/history.html')


@csrf_exempt
def update_product_count(request):
    name = request.POST.get('product_name')
    product_id = Good.objects.get(title=name).id
    action = request.POST.get('action')

    if product_id and action:
        cart = Cart.objects.filter(buyer_id=request.user.id, status=True).first()

        if action == 'minus':
            if cart.cart[product_id] > 0:
                cart.cart[product_id] -= 1
                cart.save()
            else:
                cart.cart.pop(product_id)
                cart.save()

        if action == 'plus':
            cart.cart[product_id] += 1
            cart.save()

        return redirect('lk')

    return redirect('lk')
