from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import sqlite3 as sql

# глобальные переменные для cv и бд
con = sql.connect('second.db')
cur = con.cursor()
cap = cv2.VideoCapture(0)
cur.execute("INSERT INTO sales02 VALUES (?, ?, ?, ?)", (1, 1, 1, 1,))

# разрешение камеры
cap.set(4,480)
time.sleep(2)

font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # чтение с камеры
    ret, frame = cap.read()
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # декодинг
    decodedObjects = pyzbar.decode(im)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # выделяет сам qr код в квадрат(немного магии)
        if len(points) > 4 :
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else :
          hull = points;

        n = len(hull)
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        # Запись в бд и вывод в терминал
        barCode = int(decodedObject.data)
        buyer_id = 1
        ammount = 1

        res = cur.execute("SELECT ID FROM sales02 ORDER BY ID DESC LIMIT 1")
        prev_prod_id = res.fetchall()
        if prev_prod_id is not []: #если не первая запись в бд
            res = cur.execute("SELECT ID FROM sales02 ORDER BY ID DESC LIMIT 1")
            prev_prod_id = res.fetchone()[0]
            if prev_prod_id != barCode:
                print("QR код найден")
                print(barCode, '\n')
                res = cur.execute("SELECT ID FROM sales02 ORDER BY ID DESC LIMIT 1")
                sale_id = res.fetchone()[0] + 1
                cur.execute("INSERT INTO sales02 VALUES (?, ?, ?, ?)", (sale_id, buyer_id, barCode, ammount,))
                con.commit()
            else:
                break
        else: #если первая запись в бд
            print("QR код найден")
            print(barCode, '\n')
            sale_id = 1
            cur.execute("INSERT INTO sales02 VALUES (?, ?, ?, ?)", (sale_id, buyer_id, barCode, ammount,))
            con.commit()

# освобождение ресурсов камеры
cap.release()
cv2.destroyAllWindows()


# TODO: придумать как сделать выход из программы и закрыть камеру