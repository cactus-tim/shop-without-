import face_recognition
import yadisk
import sqlite3 as sql
import sys


def start(id):  # хз как назвать, у кого будут идеи - исправьте пж
    # DB
    con = sql.connect('../../third.db')
    cur = con.cursor()
    query = f"SELECT Face FROM users WHERE ID = '{id}'"
    res = cur.execute(query)
    if not res.fetchall():
        print("this user dont exist")
        sys.exit(0)
    res = cur.execute(query)
    link = res.fetchone()[0]
    query = f"SELECT Email FROM users WHERE ID = '{id}'"
    res = cur.execute(query)
    email = res.fetchone()[0]
    path = "/Users/timofejsosnin/data/" + str(id) + '_' + email + ".jpeg"

    # YaDisk
    client_id = "9ccafedf10664913b01666dbceb950b1"
    secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
    token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"
    disk = yadisk.YaDisk(client_id, secret_id, token)
    disk.download_by_link(link, path)

    photo_to_emb(path)


def photo_to_emb(path):
    im = face_recognition.load_image_file(path)
    emb = face_recognition.face_encodings(im)[0]
    print(emb)


if __name__ == '__main__':
    id = int(input())  # вместо этого надо передать айдишник

    start(id)
