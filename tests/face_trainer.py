import json
import os

import cv2
import numpy

datasets = "datasets"
DIR = os.path.dirname(os.path.abspath(__file__))
os.mkdir(os.path.join(DIR, datasets))
PHOTOS_DIR = os.path.join(DIR, datasets)

haar_file = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_file)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
names = {}
labels = []
images = []

for root, dirs, files in os.walk(PHOTOS_DIR):
    for subdir in dirs:
        image_files = os.listdir(os.path.join(root, subdir))

        for image_file in image_files:
            if image_file.endswith(".jpg"):
                path = os.path.join(root, subdir, image_file)
                name = os.path.basename(subdir).replace(" ", "-").lower()
                names[name] = current_id

                img = cv2.imread(path)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30))

                # get region of interest
                for (x, y, w, h) in faces:
                    roi = gray_img[y:y + h, x:x + w]
                    images.append(roi)
                    labels.append(current_id)

        current_id += 1

# save the ids with labels
data = json.dumps(names, indent=4)
with open("label_ids.json", "w") as f:
    f.write(data)

# save the trained images
face_recognizer.train(images, numpy.array(labels))
face_recognizer.save("trainers.yaml")
