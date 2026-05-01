from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Slot)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QLabel,
    QListView, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout, 
    QWidget, QMessageBox, QFileDialog, QDialogButtonBox, QAbstractItemView)

from PySide6.QtMultimedia import QMediaDevices

import sys, cv2, atexit
from math import gcd

from main_window import Ui_MainWindow
from logic import LogicThread
from database import database
from submenus import Unsaved_warning, Barrier_warning, AddEdit_plate, Remove_plate, Generic_warning, About
from settings import Settings, SettingsUI

import serial
from barrier import get_barrier_status, open_barrier, close_barrier, set_time
#from dummy_barrier import get_barrier_status, open_barrier, close_barrier, set_time

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Load settings
        self.settings = Settings()
        self.settings_dict = self.settings.get_settings()
        set_time(self.settings_dict["time_to_close"])

        self.logic_thread = LogicThread(self.settings_dict, self)
        self.logic_thread.update_frame.connect(self.set_frame)
        self.logic_thread.update_plate.connect(self.set_plate)
        self.logic_thread.clear_plate.connect(self.clear_plate)
        self.logic_thread.update_barrier_status.connect(self.set_barrier_status)
        self.plates = list()
        
        # Load UI
        self.setupUi(self)

        # Setup
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.pushButtonOpen.setDisabled(True)
        self.pushButtonClose.setDisabled(False)
        self.set_barrier_status(get_barrier_status())

        # Submenus
        self.ui_unsaved_warning = Unsaved_warning(self)
        self.ui_barrier_warning = Barrier_warning(self)
        self.ui_add_edit = None
        self.ui_remove = Remove_plate(self)
        if self.settings.camera_index != None:
            self.ui_settings = SettingsUI(self.settings.list_of_cameras, self.settings.camera_data, self.settings.camera_index, self.settings.camera_resolution_index, self.settings.times_to_detect, self.settings.max_detection_time, self.settings.time_to_close, self)
        self.ui_about = About(self)

        # Triggers
        self.actionNew_database.triggered.connect(self.new_db)
        self.actionOpen_database.triggered.connect(self.open_db)
        self.actionSave.triggered.connect(self.save_db)
        self.actionSave_As.triggered.connect(self.save_as_db)
        self.actionQuit.triggered.connect(self.exit_program)

        self.actionAdd.triggered.connect(self.add_db)
        self.listWidget.itemDoubleClicked.connect(self.edit_db)
        self.actionRemove.triggered.connect(self.remove_db)

        self.actionPreferences.triggered.connect(self.settings_app)

        self.actionAbout_ParkManager.triggered.connect(self.about)

        self.pushButtonOpen.pressed.connect(self.open_barrier_ui)
        self.pushButtonClose.pressed.connect(self.close_barrier_ui)

    @Slot(QImage, int, int)
    def set_frame(self, frame, w, h):
        frame_w, frame_h = self.resolution_calculator(w, h, self.centralwidget.size().width(), self.centralwidget.size().height())
        scaled_frame = frame.scaled(frame_w, frame_h, Qt.KeepAspectRatio)
        self.labelCamera.setPixmap(QPixmap.fromImage(scaled_frame))

    @Slot(QImage, int, int, str, bool)
    def set_plate(self, frame, w, h, text, is_allowed):
        frame_w, frame_h = self.resolution_calculator(w, h, self.dWidgetPlateReader.size().width()-20, self.dWidgetPlateReader.size().height()-20)
        scaled_frame = frame.scaled(frame_w, frame_h, Qt.KeepAspectRatio)
        self.labelPlate.setPixmap(QPixmap.fromImage(scaled_frame))
        self.labelPlateText.setText(text)
        if is_allowed:
            self.labelPlateText.setStyleSheet("color: lime; font-size: 30pt;")
        else:
            self.labelPlateText.setStyleSheet("color: red; font-size: 30pt;")
    
    @Slot()
    def clear_plate(self):
        self.labelPlate.clear()
        self.labelPlateText.clear()

    @Slot(bool)
    def set_barrier_status(self, is_open):
        if is_open:
            self.labelBarrierStatus.setText("Open")
        else:
            self.labelBarrierStatus.setText("Closed")

        self.labelBarrierStatus.setStyleSheet("font-size: 30pt;")
    
    def resolution_calculator(self, init_w, init_h, w, h):
        largest_common_divisor = gcd(init_w, init_h)
        aspect_ratio = (init_w / largest_common_divisor) / (init_h / largest_common_divisor)
        new_w = int(h * aspect_ratio)
        new_h = int(w / aspect_ratio)

        return (new_w, new_h)

    def clear_list_widget(self):
        self.listWidget.clear()
    
    def fetch_db(self):
        self.clear_list_widget()
        try:
            formatted_data, plates = database.fetch_database_data()
        except:
            self.listWidget.clear()
            self.plates = []
        else:
            if formatted_data:
                self.listWidget.addItems(formatted_data)
                self.plates = plates


    def new_db(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open:
                self.kill_threads()
            
            if database.close_database():
                database.new_database()
            else:
                result = self.ui_unsaved_warning.exec()

                match result:
                    case QMessageBox.StandardButton.Save:
                        self.save_db(self.ui_unsaved_warning)
                        if database.close_database():
                            database.new_database()
                            self.clear_list_widget()
                            self.pushButtonOpen.setDisabled(False)
                            self.pushButtonClose.setDisabled(False)
                        else:
                            print("Couldn't create new database")
                    case QMessageBox.StandardButton.Discard:
                        database.close_database(True)
                        database.new_database()
                        self.clear_list_widget()
                        self.pushButtonOpen.setDisabled(False)
                        self.pushButtonClose.setDisabled(False)
                    case QMessageBox.StandardButton.Cancel:
                        pass
            
            if database.db_open:
                self.logic_thread.plates = self.plates
                self.logic_thread.start()
        
        return
    
    def open_db(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open:
                self.kill_threads()
            

            path = QFileDialog.getOpenFileName(caption="Select Database", filter="Database (*.db)")[0]
            
            if path:
                if database.open_database(path):
                    print("Database opened!")
                    self.clear_list_widget()
                    self.fetch_db()
                    self.pushButtonOpen.setDisabled(False)
                    self.pushButtonClose.setDisabled(False)
                else:
                    result = self.ui_unsaved_warning.exec()

                    match result:
                        case QMessageBox.Save:
                            self.save_db(self.ui_unsaved_warning)
                            if database.close_database():
                                path = QFileDialog.getOpenFileName(caption="Select Database", filter="Database (*.db)")[0]
                                if path:
                                    if database.open_database(path):
                                        print("Database opened!")
                                        self.clear_list_widget()
                                        self.fetch_db()
                                        self.pushButtonOpen.setDisabled(False)
                                        self.pushButtonClose.setDisabled(False)
                            else:
                                print("Couldn't open database")
                        case QMessageBox.Discard:
                            path = QFileDialog.getOpenFileName(caption="Select Database", filter="Database (*.db)")[0]
                            if path:
                                database.close_database(True)
                                if database.open_database(path):
                                    print("Database opened!")
                                    self.clear_list_widget()
                                    self.fetch_db()
                                    self.pushButtonOpen.setDisabled(False)
                                    self.pushButtonClose.setDisabled(False)
                        case QMessageBox.Cancel:
                            pass
            
            if database.db_open:
                self.logic_thread.plates = self.plates
                self.logic_thread.start()
        
        return
        
                
    def save_db(self, parent = None):
        if database.db_open:
            if database.save_database():
                print("Database saved!")
            else:
                self.save_as_db(parent)
        
        return
    
    def save_as_db(self, parent = None):
        if database.db_open:
            if parent:
                path = QFileDialog.getSaveFileName(parent = parent, caption="Save Database", filter="Database (*.db)")[0]
            else:
                path = QFileDialog.getSaveFileName(caption="Save Database", filter="Database (*.db)")[0]
            if path:
                database.set_database_path(path)
                if database.save_database():
                    print("Database saved")
                else:
                    print("Failed to save database!")
        
        return
    
    def exit_program(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open:
                self.kill_threads()
            
            if database.close_database():
                sys.exit()
            else:
                result = self.ui_unsaved_warning.exec()

                match result:
                    case QMessageBox.StandardButton.Save:
                        self.save_db(self.ui_unsaved_warning)
                        if database.close_database():
                            sys.exit()
                        else:
                            print("Couldn't close database")
                    case QMessageBox.StandardButton.Discard:
                        database.close_database(True)
                        sys.exit()
                    case QMessageBox.StandardButton.Cancel:
                        pass

            if database.db_open:
                self.logic_thread.plates = self.plates
                self.logic_thread.start()
        
        return
    
    def add_db(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open:
                self.kill_threads()
            
                self.ui_add_edit = AddEdit_plate(self)
                result = self.ui_add_edit.exec()
                if result:
                    plate = self.ui_add_edit.plate.text()
                    name = self.ui_add_edit.name.text()
                    if plate and name:
                        if not database.check_if_plate_is_allowed(plate):
                            database.add_to_database(plate, name)
                            self.fetch_db()
                        else:
                            print("Plate already exists! Not adding.")
                            warning = Generic_warning("Information", "Plate already exists!", None, False, self)
                            warning.exec()
                    else:
                        print("Nothing was added.")
                
                self.logic_thread.plates = self.plates
                self.logic_thread.start()
    
    def edit_db(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open:
                self.kill_threads()

                text = self.listWidget.selectedItems()[0].text()
                text_split = text.split('(')
                old_plate = text_split[0][:-1]
                old_name = text_split[1][:-1]
                print(f"{old_plate} ({old_name})")

                self.ui_add_edit = AddEdit_plate(self, (old_plate, old_name))
                result = self.ui_add_edit.exec()

                if result:
                    plate = self.ui_add_edit.plate.text()
                    name = self.ui_add_edit.name.text()
                    if (plate and name) and (plate != old_plate and name != old_name):
                        if database.edit_database(old_plate, plate, name):
                            print("Edited entry!")
                            self.fetch_db()
                        else:
                            print("Failed to edit.")
                            warning = Generic_warning("Warning", "Failed to edit!", None, True, self)
                            warning.exec()
                    elif plate and plate != old_plate:
                        if database.edit_database(old_plate, plate, None):
                            print("Edited entry!")
                            self.fetch_db()
                        else:
                            print("Failed to edit.")
                            warning = Generic_warning("Warning", "Failed to edit!", None, True, self)
                            warning.exec()
                    elif name and name != old_name:
                        if database.edit_database(old_plate, None, name):
                            print("Edited entry!")
                            self.fetch_db()
                        else:
                            print("Failed to edit.")
                            warning = Generic_warning("Warning", "Failed to edit!", None, True, self)
                            warning.exec()
                    else:
                        print("Nothing was edited.")

                self.logic_thread.plates = self.plates
                self.logic_thread.start()

    def remove_db(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        else:
            if database.db_open and self.plates:
                self.kill_threads()

                result = self.ui_remove.exec()

                if result:
                    plate = self.ui_remove.plate.text()

                    if plate:
                        if database.remove_from_database(plate):
                            print("Removed!")
                            self.fetch_db()
                        else:
                            print("Failed to remove.")
                            warning = Generic_warning("Warning", "Failed to remove!", None, True, self)
                            warning.exec()

                self.logic_thread.plates = self.plates
                self.logic_thread.start()

    def settings_app(self):
        if get_barrier_status():
            self.ui_barrier_warning.exec()
        elif self.settings.camera_index != None:
            if database.db_open:
                self.kill_threads()
            
            result = self.ui_settings.exec()

            if result:
                changed = False
                camera_index = self.ui_settings.current_camera.currentIndex()
                resolution_index = self.ui_settings.current_resolution.currentIndex()
                times_to_detect = int(self.ui_settings.times_to_detect.value())
                max_detection_time = int(self.ui_settings.max_detection_time.value())
                time_to_close = int(self.ui_settings.time_to_close.value())
                
                if (camera_index != self.settings.camera_index or resolution_index != self.settings.camera_resolution_index) and camera_index != -1 and resolution_index != -1:
                    self.settings.load_camera_from_index(camera_index, resolution_index)
                    changed = True

                if times_to_detect and times_to_detect != self.settings.times_to_detect:
                    self.settings.times_to_detect = times_to_detect
                    changed = True

                if max_detection_time and max_detection_time != self.settings.max_detection_time:
                    self.settings.max_detection_time = max_detection_time
                    changed = True

                if time_to_close and time_to_close != self.settings.time_to_close:
                    self.settings.time_to_close = time_to_close
                    changed = True

                if changed:
                    self.settings.save_settings()
                    self.logic_thread.setup(self.settings.get_settings())
                    print("Saved!")

            if database.db_open:
                self.logic_thread.plates = self.plates
                self.logic_thread.start()
    
    def open_barrier_ui(self):
        if get_barrier_status():
            warning = Generic_warning("Warning", "Barrier is already raised!", None, False, self)
            warning.exec()
        else:
            if not open_barrier():
                warning = Generic_warning("Warning", "Cannot raise barrier at the moment.", None, False, self)
                warning.exec()
            else:
                self.set_barrier_status(get_barrier_status())

    def close_barrier_ui(self):
        if not get_barrier_status():
            warning = Generic_warning("Warning", "Barrier is already lowered!", None, False, self)
            warning.exec()
        else:
            if not close_barrier():
                warning = Generic_warning("Warning", "Cannot lower barrier at the moment.", None, False, self)
                warning.exec()
            else:
                self.set_barrier_status(get_barrier_status())

    def about(self):
        self.ui_about.exec()

    def kill_threads(self):
        self.logic_thread.stop()
        self.clear_plate()

def on_exit():
    window.kill_threads()
    database.clean_temp()
    close_barrier()

if __name__  == "__main__":
    #database.new_database()
    #database.dummy_write()
    #database.set_database_path("/home/adrian/Downloads/test.db")
    #database.save_database()
    #database.close_database()
    #database.open_database("/home/adrian/Downloads/test.db")
    #print(database.fetch_database_data())
    #database.edit_database("BN 19 CTL", "BN 18 CTL", "Hosu Adrian")
    #print(database.fetch_database_data())
    #database.save_database()
    #database.close_database()
    get_barrier_status()
    
    app = QApplication(sys.argv)

    atexit.register(on_exit)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
