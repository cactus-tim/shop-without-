from django.http import JsonResponse
from django.shortcuts import render
import numpy as np

from pyzbar.pyzbar import decode
import pandas as pd
def lk(request):
     return render(request, 'lk/lk.html')
import cv2
def run_script(request):
    # Ваш Python-скрипт
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow("camera", img)
        if cv2.waitKey(10) == 27: # Клавиша Esc
            break
    cap.release()
    cv2.destroyAllWindows()
def from_bd(BarCode):
    prod = pd.read_excel('../../Other scripts/pipip.xlsx')

    chosen = prod.loc[(prod['A'] == BarCode)]
    print(chosen)



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
        decodedObjects = pyzbar.decode(im)

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
            from_bd(BarCode=barCode)