import json
import os
import random
import sqlite3

import cv2
import numpy
from PyQt5.QtGui import QIcon


class Model:
    def __init__(self):
        self.root = os.getcwd()
        self.config = self.read()

        self.title = "Kedi"
        self.table_titles = ["ID", "İSİM", "SOYİSİM", "TELEFON NUMARASI"]
        self.DATASETS_DIR = os.path.join(self.root, "model", "datasets")
        self.camera_index = 0
        self.fps = 20
        self.anticipate = 55
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.scale_factor = 1.2
        self.min_neighbors = 4
        self.min_size = (30, 30)
        self.cat_running = False

        self.cascadeClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
        self.videoCapture = cv2.VideoCapture(self.camera_index)

        self.current_id = 0
        self.names = {}
        self.labels = []
        self.images = []
        self.keys = []

        self.selected_row = None
        self.selected_id = None

        self.img_assets = os.path.join(self.root, "assets", "img")
        self.css_assets = os.path.join(self.root, "assets", "css")
        self.config_path = os.path.join(self.root, "model", "config.json")
        self.trainers_file = os.path.join(self.root, "model", "trainers.yaml")
        self.label_ids_file = os.path.join(self.root, "model", "label_ids.json")

        self.icon = QIcon(os.path.join(self.img_assets, "icon.png"))

        self.database = os.path.join(self.root, "model", "datatable.db")
        self.conn = sqlite3.connect(self.database)
        self.main_sql = "SELECT id, name, surname, phone FROM people;"

        self.add_icon = QIcon(os.path.join(self.img_assets, "database--plus.png"))
        self.del_icon = QIcon(os.path.join(self.img_assets, "database--minus.png"))
        self.edit_icon = QIcon(os.path.join(self.img_assets, "database--pencil.png"))
        self.find_icon = QIcon(os.path.join(self.img_assets, "magnifier.png"))
        self.refresh_icon = QIcon(os.path.join(self.img_assets, "arrow-circle-225.png"))
        self.exit_icon = QIcon(os.path.join(self.img_assets, "door-open-in.png"))

        self.full_icon = QIcon(os.path.join(self.img_assets, "application-resize-full.png"))
        self.menu_icon = QIcon(os.path.join(self.img_assets, "ui-menu.png"))
        self.toolbar_icon = QIcon(os.path.join(self.img_assets, "ui-toolbar.png"))
        self.dark_icon = QIcon(os.path.join(self.img_assets, "smiley-glass.png"))

        self.help_icon = QIcon(os.path.join(self.img_assets, "question.png"))
        self.about_icon = QIcon(os.path.join(self.img_assets, "information.png"))

    def is_selected(self) -> bool:
        """
        Seçilme ile ilgili verilerin seçili olup olmadığını yansıtır
        :rtype: bool
        """
        if self.selected_id is not None and self.selected_row is not None:
            return True
        return False

    def deselect(self) -> None:
        """
        Seçili verileri seçilmemiş haline geri döndürür
        :rtype: None
        """
        self.selected_id = self.selected_row = None

    def _write(self) -> None:
        """
        Sınıf içerisinde dosyaya yazmak için kullanılmalıdır.
        :rtype: None
        """
        dumping = json.dumps(self.config, indent=4, sort_keys=True)

        with open(self.config_path, "w") as f:
            f.write(dumping)

    def update(self, key: str, value: any) -> None:
        """
        Belli bir ayarı değiştirmek ve kaydetmek için kullanılır
        :rtype: None
        """
        self.config = self.read()
        self.config[key] = value
        self._write()

    def read(self) -> dict:
        """
        Ayarları okutur ve geri döndürür
        :rtype: dict
        """
        with open(os.path.join(self.root, "model", "config.json")) as f:
            json_data = f.read()
            dict_data = json.loads(json_data)
            self.config = dict_data
            return dict_data

    def read_stylesheets(self) -> any:
        """
        json dosyasından alınıp css dosyasına yazılan verileri döndürür
        :rtype: any
        """
        self.config = self.read()

        if self.config.get('dark'):
            with open(os.path.join(self.css_assets, "{}.min.css".format('dark'))) as f:
                return f.read()
        return None

    def detect_face_by_path(self, path: str) -> tuple:
        """
        cascadeClassifier fonksiyonu sayesinde dosya yolu belirtilen resim üzerinde yüz tespiti yapar ve ilk önce resmi
        iterable tipinde sonrasında üzerinde işlem yapılan kareyi gri rengine dönüştürüp geri döndürür.
        :param path:
        :rtype: tuple
        """
        img = cv2.imread(path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return (self.cascadeClassifier.detectMultiScale(gray_img, scaleFactor=self.scale_factor,
                                                        minNeighbors=self.min_neighbors,
                                                        minSize=self.min_size), gray_img)

    def prepare_train(self) -> None:
        """
        datasets klasörü altındaki klasör ve resimleri hakkında bilgi toplar ve bu resimler içindeki yüzleri tespit
        eder sonrasında bu bilgileri array() & dict() veri tipleri olarak kaydeder
        :rtype: None
        """
        for root, dirs, files in os.walk(self.DATASETS_DIR):
            for subdir in dirs:
                # datasets klasörünün altındaki her bir klasörü ve onun altında bulunan resimleri bul
                image_files = os.listdir(os.path.join(root, subdir))

                for image_file in image_files:
                    path = os.path.join(root, subdir, image_file)
                    name = os.path.basename(subdir).replace(" ", "-").lower()

                    # veri tabanında bulunan ve isim-soyisim şeklindeki verileri sözlüğe kaydet
                    self.names[name] = self.current_id

                    # resimleri tek tek okut ardından gri rengine çevirt ardından yüz tespitini yap
                    # IMPORTANT: we do not need to detect the faces because our program stores detected faces already.
                    faces, gray_img = self.detect_face_by_path(path)
                    #
                    # # get region of interest
                    for (x, y, w, h) in faces:
                        roi = gray_img[y:y + h, x:x + w]
                        self.images.append(roi)
                        self.labels.append(self.current_id)

                    # img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    # self.images.append(img)
                    # self.labels.append(self.current_id)

                self.current_id += 1

    def run_face_detector(self) -> None:
        """
        cv2.VideoCapture() fonksiyonu ile belirtilen kamera üzerinden kayda geçer ve kayıtta görünen yüzlerle
        veritabanındaki kayıtlı olan kişilerin yüzleri ile karşılaştırma yapar.
        :rtype: None
        """
        while self.videoCapture.isOpened():
            ok, frame = self.videoCapture.read()
            # the scene must be flipped
            frame = cv2.flip(frame, 1)

            if not ok:
                print("[ERROR] : Could not get frame")
                break

            # her bir sahneyi tek tek okut ardından gri rengine çevirt ardından yüz tespitini yap
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.cascadeClassifier.detectMultiScale(gray_img, scaleFactor=self.scale_factor,
                                                            minNeighbors=self.min_neighbors,
                                                            minSize=self.min_size)

            for (x, y, w, h) in faces:
                # pick different colors for different faces
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # color = (0, 0, 255)

                roi_gray = gray_img[y:y + h, x:x + w]
                id_, prediction = self.faceRecognizer.predict(roi_gray)

                # yüz tespiti yapılan kişilerin isimlerini bul
                if prediction >= self.anticipate and prediction <= 85:
                    name = self.keys[id_]
                    text = str(int(prediction)) + ' ' + name

                else:
                    text = "????"

                # ekrana belirtilen verileri yazdır ve tespit edilen yüzlerin etrafına dikdörtgen çizdir
                cv2.putText(img=frame, text=text, org=(x - 5, y - 10), fontFace=self.font, fontScale=1,
                            color=color, thickness=1, lineType=cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color=color, thickness=2, lineType=cv2.LINE_AA)

            # her bir sahneyi kare kare video gibi göster.
            cv2.imshow(self.title, frame)
            k = cv2.waitKey(self.fps)

            if k == ord('q'):
                break

        # döngü bittiğinde bütün cv2 pencerelerini kapat
        cv2.destroyAllWindows()

    def train_images(self) -> None:
        """
        datasets klasörürün altına kaydedilmiş olan resim dosyalarını yüz tespitinin yapılmasını sağlar.
        :rtype: None
        """
        self.faceRecognizer.train(self.images, numpy.array(self.labels))
        self.faceRecognizer.save(self.trainers_file)

    def trained_images(self) -> None:
        """
        yüz tespiti yapılan ve faceRecognizer sınıfının içerisine kaydedilmiş olan bilgilerin okutulmasını sağlar.
        :rtype: None
        """
        self.faceRecognizer.read(self.trainers_file)

    def save_trained_names(self) -> None:
        """
        Yüz tespiti yapılan kişilerin isimleri ve beraberindeki id numaralarının kaydını JSON formatında tutmayı sağlar.
        :rtype: None
        """
        data = json.dumps(self.names, indent=4)
        with open(self.label_ids_file, "w") as f:
            f.write(data)

    def trained_names(self) -> list:
        """
        Yüz tespiti yapılan kişilerin JSON kaydında bulunan isimleri döndürür.
        :rtype: list
        """
        with open(self.label_ids_file) as f:
            names = json.load(f)
            self.keys = list(names.keys())
        return self.keys

    def add_datasets(self, row: str, files: list):
        """
        Verilen satır ve dosya bilgilerine göre resimleri tek tek açar ve resimlerde bulunan varsa yüzleri tespit eder
        ve datasets klasörünün altına yüz tespiti yapılan kareleri 1,2,3... jpg formatında kaydeder.
        :param row: str
        :param files: list
        :rtype: None
        """
        file_count = 0

        try:
            os.makedirs(os.path.join(self.DATASETS_DIR, row), exist_ok=False)

        except FileExistsError:
            print("[*] File or directory exists. Continuing...")

        finally:
            row_dir = os.path.join(self.DATASETS_DIR, row)

            for file in files:
                file_count += 1
                faces, gray_img = self.detect_face_by_path(file)

                for (x, y, w, h) in faces:
                    roi = gray_img[y:y + h, x:x + w]
                    filename = str(file_count) + '.jpg'
                    cv2.imwrite(os.path.join(row_dir, filename), roi)

    def format_calling(self, name: str, surname: str) -> str:
        """
        isim ve soyisim olarak verilen bilgileri isim-soyisim şekline ve arada boşluk olmadan biçimlendirir
        :param name:
        :param surname:
        :return:
        :rtype: str
        """
        return f"{str(name).replace(' ', '-')}-{str(surname).replace(' ', '-')}"
