from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from ultralytics import YOLO
from re import findall
from time import time
import cv2
import pytesseract
import numpy as np

import serial
from barrier import get_barrier_status, open_barrier, close_barrier, set_time
#from dummy_barrier import get_barrier_status, open_barrier, close_barrier, set_time

class LogicThread(QThread):
    update_frame = Signal(QImage, int, int)
    update_plate = Signal(QImage, int, int, str, bool)
    clear_plate = Signal()
    update_barrier_status = Signal(bool)

    def __init__(self, settings, parent=None):
        QThread.__init__(self, parent)
        self.thread_status = True
        self.model = YOLO(model='model/best.pt')
        pytesseract.pytesseract.tesseract_cmd = "tesseract"
        self.capture = None

        # Settings
        self.setup(settings)
        self.plates = None
        
        self.barrier_opened_by_ai = False
        self.plate_appearance = dict()
        self.time_first_detection = None
        self.time_open = None
        self.time_denied = None

    def setup(self, settings):
        self.camera = settings["camera"]
        self.camera_w = settings["camera_w"]
        self.camera_h = settings["camera_h"]
        self.times_to_detect = settings["times_to_detect"]
        self.max_detection_time = settings["max_detection_time"]
        self.time_to_close = settings["time_to_close"]
    
    def run(self):
        self.thread_status = True
        self.capture = cv2.VideoCapture(self.camera)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_w)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_h)
        set_time(self.time_to_close)

        print(f"Camera: {self.camera}\nResolution: {self.camera_w} x {self.camera_h}\nTimes to detect: {self.times_to_detect}\nMax detection time: {self.max_detection_time}\nTime before closing: {self.time_to_close}")
        
        while self.thread_status:
            #frame = cv2.imread('test.png', cv2.IMREAD_COLOR)
            #ret = True

            ret, frame = self.capture.read()

            if ret:
                color_corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                list_plates = self.predict(color_corrected_frame)
                
                for data in list_plates:
                    p1 = data[0]
                    p2 = data[1]
                    text = data[2]

                    cv2.rectangle(color_corrected_frame, p1, p2, (0, 255, 0), 3)
                    cv2.putText(color_corrected_frame, text,(p1[0], p1[1]-10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
                
                self.set_camera_label(color_corrected_frame)

                self.plate_checker(list_plates)


    def stop(self):
        # Inchidem thread-ul
        self.thread_status = False
        if self.capture:
            self.capture.release()
        self.quit()
        
        self.barrier_opened_by_ai = False
        self.plate_appearance = dict()
        self.time_first_detection = None
        self.time_open = None
        self.time_denied = None

    def plate_checker(self, list_plates):
        if self.time_denied and time() - self.time_denied > 5:
            self.time_denied = None
            self.clear_plate_label()

        # Verificam daca bariera este deschisa sau nu
        barrier_status = get_barrier_status()
        # Bariera este inchisa
        if barrier_status != "fail" and barrier_status == False:
            # Resetam variabila barrier_opened_by_ai
            self.barrier_opened_by_ai = False

            # Verificam sa existe cel putin un numar de imatriculare
            if list_plates:
                # Daca exista incercam sa obtinem text-ul si 
                # frame-ul de la cel mai mare numar de imatriculare
                text, frame = self.get_largest_valid_plate(list_plates)
                # Verificam sa fim siguri ca acest numar de imatriculare are text
                if text:
                    # Verificam daca am mai citit inainte un numar de imatriculare inainte
                    if self.plate_appearance:
                        # Daca da atunci ne intereseaza de cate ori o aparut acest numar de imatriculare
                        end = time()
                        # Daca nu au trecut self.max_detection_time secunde atunci specificam ca
                        # am gasit un numar de imatriculare inca odata
                        if end - self.time_first_detection < self.max_detection_time:
                            if text in self.plate_appearance:
                                self.plate_appearance[text]['appearance'] += 1
                            else:
                                self.plate_appearance[text] = dict()
                                self.plate_appearance[text]['appearance'] = 1
                                self.plate_appearance[text]['frame'] = frame
                        # Daca au trecut self.max_detection_time atunci vedem care numar de imatriculare
                        # cu text detectat a aparut de cele mai multe ori
                        else:
                            max_appearance = 0
                            final_text = None
                            final_frame = None
                            for key, value in self.plate_appearance.items():
                                if value['appearance'] > max_appearance:
                                    final_text = key
                                    final_frame = value['frame']
                                    max_appearance = value['appearance']
                            
                            # Daca numarul maxim de aparitii este mai mare decat numarul minim de apariti
                            # permis atunci putem deschide bariera daca numarul de imatriculare se afla
                            # in baza de date si curatam dictionarul cu aparitii
                            if max_appearance > self.times_to_detect:
                                if final_text in self.plates:
                                    if open_barrier():
                                        # Marcam ca bariera a fost deschisa de AI si nu manual
                                        self.barrier_opened_by_ai = True
                                        self.set_plate_label(final_frame, final_text, True)
                                        # V-om retine cat timp a fost deschis bariera
                                        self.time_open = time()
                                        # Curatam dictionarul cu aparitii
                                        self.plate_appearance = dict()
                                        self.time_first_detection = None
                                        self.update_barrier_status.emit(get_barrier_status())
                                # Daca numarul de imatriculare nu are voie atunci nu deschidem bariera
                                else:
                                    self.set_plate_label(final_frame, final_text, False)
                                    self.plate_appearance = dict()
                                    self.time_first_detection = None
                                    self.time_denied = time()
                            # Daca nu a aparut de cate ori trebuie curatam dictionarul cu aparitii
                            else:
                                # Curatam dictionarul cu aparitii
                                self.plate_appearance = dict()
                                self.time_first_detection = None
                    # Daca este pentru prima data cand detectam un numar de imatriculare cu text atunci
                    # il adaugam in dictionar si incepem timer-ul
                    else:
                        self.time_first_detection = time()
                        self.plate_appearance[text] = dict()
                        self.plate_appearance[text]['appearance'] = 1
                        self.plate_appearance[text]['frame'] = frame
        # Daca bariera este deschisa si a fost deschisa de AI atunci dupa self.time_to_close incercam sa o inchidem
        # daca se poate. Daca nu mai incercam inca odata data viitoare
        elif barrier_status and self.barrier_opened_by_ai:
            time_end = time()
            if time_end - self.time_open > self.time_to_close:
                if close_barrier():
                    self.barrier_opened_by_ai = False
                    self.clear_plate_label()
                    self.time_open = None
                    self.update_barrier_status.emit(get_barrier_status())
        # Daca bariera a fost deschisa de main.py si nu de AI atunci inseamna ca bariera a fost deschisa manual.
        elif barrier_status:
            # Curatam dictionarul cu aparitii
            self.plate_appearance = dict()
            self.time_first_detection = None



    def get_largest_valid_plate(self, list_plates):
        max_w = 0
        final_text = None
        final_frame = None

        for data in list_plates:
            text = data[2]
            frame = data[3]
            if hasattr(frame, 'shape'):
                h, w, ch = frame.shape

                if w > max_w and text:
                    max_w = w
                    final_text = text
                    final_frame = frame

        return (final_text, final_frame)

    def set_camera_label(self, frame: cv2.UMat):
        h, w, ch = frame.shape
        frame_qt = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)

        self.update_frame.emit(frame_qt, w, h)

    def set_plate_label(self, frame: cv2.UMat, text, is_allowed):
        color_corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = color_corrected_frame.shape
        frame_qt = QImage(color_corrected_frame.data, w, h, ch * w, QImage.Format_RGB888)

        self.update_plate.emit(frame_qt, w, h, text, is_allowed)

    def clear_plate_label(self):
        self.clear_plate.emit()

    def trim_plate_name(self, plate_text: str):
        police = False
        plate_text = plate_text.upper()

        plate_text = plate_text.split()
        
        if "RO" in plate_text[0]:
            plate_text.pop(0)

        if plate_text[0][-1:] == 'B' and (plate_text[0][-2:] != 'AB' and plate_text[0][-2:] != 'DB' and plate_text[0][-2:] != 'SB'):
            plate_text[0] = 'B'
        elif plate_text[0][-3:] == 'MAI':
            plate_text[0] = 'MAI'
            police = True
        else:
            judet = findall('AB|AG|AR|BC|BH|BN|BR|BT|BV|BZ|CJ|CL|CS|CT|CV|DB|DJ|GJ|GL|GR|HD|HR|IF|IL|IS|MH|MM|MS|NT|OT|PH|SB|SJ|SM|SV|TL|TM|TR|VL|VN|VS', plate_text[0][-2:])

            if judet:
                plate_text[0] = judet[0]
            else:
                return ""

        plate_text_length = len(plate_text)

        if plate_text_length == 3:
            if not plate_text[1].isdigit():
                return ""
            plate_text[2] = plate_text[2][:3]
        elif plate_text_length == 2:
            if not plate_text[1].isdigit():
                return ""
        else:
            return ""
        
        final_plate_text = " ".join(plate_text)

        return final_plate_text

    def predict(self, frame: cv2.UMat):
        results = self.model.predict(frame)
        h, w, ch = frame.shape
        list_plates = list()

        for result in results:
            for coords in result.boxes:
                letters = ""
                final_frame = None
                p1 = (int(coords.xyxy[0][0]-2), int(coords.xyxy[0][1])-2)
                p2 = (int(coords.xyxy[0][2]+2), int(coords.xyxy[0][3])+2)

                try:
                    cropped_frame = frame[p1[1]:p2[1], p1[0]:p2[0]]
                    final_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
                except:
                    print("Invalid cropped frame, ignoring.")
                    final_frame = None
                    valid_frame = False
                else:
                    valid_frame = True

                if valid_frame:
                    h, w, ch = final_frame.shape

                    #cv2.imwrite("test.jpg", final_frame)

                    ocr = pytesseract.image_to_string(final_frame, lang='eng', config='--tessdata-dir ./tessdata --psm 7')

                    if ocr:
                        #letters = ocr
                        letters = self.trim_plate_name(ocr)

                list_plates.append((p1, p2, letters, final_frame))

                print(f"{w}, {h}, {p1}, {p2}, {letters}")
        
        return list_plates