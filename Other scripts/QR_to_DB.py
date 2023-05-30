import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import openpyxl
import pandas as pd

def camera_work():
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
                return barCode


if __name__ == '__main__':
    barCode = camera_work()
    prod = pd.read_excel('data.xlsx')
    # print(prod)
    # print(prod.head())
    chosen = prod.loc[(prod['id'] == barCode)]
    print(chosen)
    already_cart = pd.read_excel('cart.xlsx')
    already_cart = pd.concat([already_cart, chosen])
    with pd.ExcelWriter('cart.xlsx') as writer:
        already_cart.to_excel(writer, sheet_name='cartname')