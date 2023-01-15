import json

import cv2

haar_file = "haarcascade_frontalface_default.xml"
img_file = "../model/images/photo1.jpg"
title = "face detection test"
label_ids_file = "label_ids.json"
fps = 20
anticipate = 55
font = cv2.FONT_HERSHEY_PLAIN

# todo : train faces and store them as grayscale but crop the face first and only one face must be stored within an image

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_file)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("trainers.yaml")

with open(label_ids_file) as f:
    names = json.load(f)
    keys = list(names.keys())
    del names

while cap.isOpened():
    ok, frame = cap.read()
    # the scene must be flipped
    frame = cv2.flip(frame, 1)

    if not ok:
        print("[ERROR] : Could not get frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # pick different colors for different faces
        # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color = (0, 0, 255)

        roi_gray = gray[y:y + h, x:x + w]
        id_, prediction = face_recognizer.predict(roi_gray)

        if prediction >= anticipate:
            name = keys[id_]
            text = str(int(prediction)) + ' ' + name

        else:
            text = "Not recognized"

        cv2.putText(img=frame, text=text, org=(x - 5, y - 10), fontFace=font, fontScale=1,
                    color=color, thickness=1, lineType=cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=color, thickness=2, lineType=cv2.LINE_AA)

    cv2.imshow(title, frame)
    k = cv2.waitKey(fps)

    if k == ord('q'):
        break

cv2.destroyAllWindows()
