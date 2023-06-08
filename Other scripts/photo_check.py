import yadisk
import sys
from imutils import paths
import face_recognition
import pickle
import cv2
import os
import shutil

def enc():
    imagePaths = list(paths.list_images('images'))
    knownEncodings = []
    knownNames = []
    for (i, imagePath) in enumerate(imagePaths):
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()


def try_upload(disk, path, filename):
    try:
        if disk.exists('/face_enc'):
            disk.remove('/face_enc')
        disk.upload(path, filename)
        if disk.exists(filename):

            os.mkdir('images')
            photos = disk.get_last_uploaded()
            for photo in photos:
                if photo.name == 'face_enc':
                    continue
                p = 'images/' + photo.name
                os.mkdir(p)
                name = photo.path
                p += '/' + photo.name + '.jpg'
                disk.download(name, p)

            enc()

            shutil.rmtree('images')

            p1 = 'face_enc'
            f1 = '/face_enc'
            disk.upload(p1, f1)
            os.remove('face_enc')
    except Exception as ex:
        print(ex)


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
            try_upload(disk, path, filename)
            if disk.exists(filename):
                link = disk.get_download_link(filename)
                return link
            else:
                return 'Error'
    else:
        return 'Error'


if __name__ == '__main__':
    path = '/Users/timofejsosnin/senyaxuisosi/shop-without-/Other scripts/media/wdckn.jpeg'
    email = 'tutr@mail.ru'
    print(photo_to_cloud(path, email))