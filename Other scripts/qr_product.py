import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
def camera_work():
    print("OK")
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
                hull = points;

            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            # Запись в бд и вывод в терминал
            barCode = int(decodedObject.data)
            print(barCode)
if __name__ == '__main__':
    camera_work()