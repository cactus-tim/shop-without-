import face_recognition
import os

encodings = list()

# 36 x 36 = 1296 пар фото
for photo in os.listdir('Images/Andre_Agassi'):
    im = face_recognition.load_image_file('Images/Andre_Agassi/' + photo)
    encodings.append(face_recognition.face_encodings(im)[0])

for i in range(len(encodings)):
    for j in range(len(encodings)):
        res = face_recognition.compare_faces([encodings[i]], encodings[j])
        print(res, i, j)
