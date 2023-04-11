import face_recognition
import pickle
import cv2
import os

cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"

faceCascade = cv2.CascadeClassifier(cascPathface)

data = pickle.loads(open('face_enc', "rb").read())

# Программа знает Тимошу, но не знает Стива Джобса
image = cv2.imread('to_check/Steve-jobs.jpg')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(60, 60),
                                     flags=cv2.CASCADE_SCALE_IMAGE)

encodings = face_recognition.face_encodings(rgb)
print(encodings)
names = []

for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"],
                                             encoding)
    name = "Face"
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", image)
    cv2.waitKey(0)

    if True in matches:
        image = cv2.imread('to_check/tim5.jpg')
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
        for ((x, y, w, h), name) in zip(faces, names):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

        cv2.imshow("Frame", image)
        cv2.waitKey(0)
