import face_recognition
import imutils
import pickle
import time
from tkinter import *
import cv2
import os


def end():
    print("Streaming started")
    video_capture = cv2.VideoCapture(0)
    root = Tk()
    root.title("Покуп0чка")
    root.geometry("300x250")

    label = Label(text="Хотите завершить покупку?")
    label.pack()

    btnYes = Button(text="ДаДа")

    btnYes.pack()
    btnYes.bind('<Button-1>', lambda event: recognize(root, video_capture))
    root.mainloop()
    return root


def failed(rot):
    rot.destroy()
    end()


def spisali_rubiki(rot):
    rot.destroy()
    minus_dengi = True
    end()


def accept(name):
    root = Tk()
    root.title("Покуп0чка")
    root.geometry("300x250")

    label = Label(text=name + " это вы?")
    label.pack()

    btnYes = Button(text="ДаДа")
    btnYes.pack()
    btnYes.bind('<Button-1>', lambda event: failed(root))
    btnNo = Button(text="НетНет")
    btnNo.pack()
    btnNo.bind('<Button-1>', lambda event: failed(root))
    root.mainloop()
    return root


def recognize(rot, video_capture):
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(60, 60),
                                             flags=cv2.CASCADE_SCALE_IMAGE)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        name = "Unknown"
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)

            names.append(name)
            for ((x, y, w, h), name) in zip(faces, names):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        if name != "Unknown":
            cv2.imwrite('cam.png', frame)
            print(name)
            rot.destroy()
            video_capture.release()
            cv2.destroyAllWindows()
            accept(name)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            break



cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)
data = pickle.loads(open('face_enc', "rb").read())



win1 = end()
