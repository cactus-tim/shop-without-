import face_recognition
import imutils
import pickle
import time
from tkinter import *
import cv2
import os
import sqlite3 as sql
import yadisk

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


def spisali_rubiki(rot, id):
    rot.destroy()
    minus_dengi = True
    con = sql.connect('../web_app/db.first')
    c = con.cursor()
    query = "SELECT * FROM reg_log_cart WHERE buyer_id = ?"
    c.execute(query, id)
    result = c.fetchone()
    if result is None:
        print("пользователь ничего не покупал")
        con.commit()
        con.close()
        os.remove('face_enc')
        end()
    else:
        query1 = "SELECT Balance FROM reg_log_users WHERE id = ?"
        c.execute(query1, id)
        balance = c.fetchone()
        query2 = "SELECT total FROM reg_log_cart WHERE buyer_id = ?"
        c.execute(query2, id)
        summa = c.fetchone()
        new_balance = balance[0] - summa[0]
        print(balance[0])
        print(summa[0])
        print(new_balance)
        if new_balance < 0:
            print('недостаточно средств')
            label = Label(text="На балансе недостаточно средств")
            label.pack()
            con.commit()
            con.close()
            os.remove('face_enc')
            end()
        query3 = "UPDATE reg_log_users SET Balance = ? WHERE id = ?"

        c.execute(query3, (new_balance, id[0], ))

        c.execute("DELETE FROM reg_log_cart WHERE buyer_id = ?", id)
        con.commit()
        con.close()
        os.remove('face_enc')
        end()



def accept(mail):
    root = Tk()
    root.title("Покуп0чка")
    root.geometry("300x250")

    con = sql.connect('../web_app/db.first')
    c = con.cursor()
    c.execute("SELECT Name FROM reg_log_users WHERE Email = ?", (mail, ))
    name = c.fetchone()
    # print(ans)
    c.execute("SELECT Surname FROM reg_log_users WHERE Email = ?", (mail, ))
    surname = c.fetchone()
    # surname = ans[1]
    c.execute("SELECT id FROM reg_log_users WHERE Email = ?", (mail, ))
    id = c.fetchone()
    print(name)
    print(surname)
    print(id)
    con.commit()
    con.close()

    label = Label(text=name[0] + ' ' + surname[0] + " это вы?")
    label.pack()

    btnYes = Button(text="ДаДа")
    btnYes.pack()
    btnYes.bind('<Button-1>', lambda event: spisali_rubiki(root, id))
    btnNo = Button(text="НетНет")
    btnNo.pack()
    btnNo.bind('<Button-1>', lambda event: failed(root))
    root.mainloop()
    return root


def recognize(rot, video_capture):
    client_id = "9ccafedf10664913b01666dbceb950b1"
    secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
    token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"

    disk = yadisk.YaDisk(client_id, secret_id, token)
    path = 'face_enc'

    if disk.exists('face_enc'):
        disk.download('/face_enc', path)

    cascPathface = os.path.dirname(
        cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPathface)
    data = pickle.loads(open('face_enc', "rb").read())
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


win1 = end()
