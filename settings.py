from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtCore import QByteArray
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox, QDialogButtonBox
import yaml
import pathlib
import sys

class Settings(object):
    def __init__(self):
        
        # Settings
        self.last_used_camera = None
        self.last_used_resolution = None
        self.times_to_detect = None
        self.max_detection_time = None
        self.time_to_close = None

        # Selected camera settings
        self.camera = None
        self.camera_w = None
        self.camera_h = None
        self.camera_index = None
        self.camera_resolution_index = None

        # Default settings
        self.default_last_used_camera = None
        self.default_last_used_resolution = None
        self.default_times_to_detect = 10
        self.default_max_detection_time = 3
        self.default_time_to_close = 7

        # List of cameras
        self.list_of_cameras = list()
        self.camera_data = dict()
        self.fetch_cameras()

        # Load settings
        self.settings_path = pathlib.Path(sys.path[0], "settings.cfg")
        self.settings = dict()
        if not self.load_settings():
            self.create_settings()
            if not self.load_settings():
                print("Failed to create settings file! Loading defaults...")

                self.last_used_camera = self.default_last_used_camera
                self.last_used_resolution = self.default_last_used_resolution
                self.times_to_detect = self.default_times_to_detect
                self.max_detection_time = self.default_max_detection_time
                self.time_to_close = self.default_time_to_close
            else:
                print("Loaded new settings!")
        else:
            print("Loaded settings!")
        
        # Auto choose camera
        self.load_camera()

        # Save
        self.save_settings()

    def get_settings(self):
        settings = dict()
        settings["camera"] = self.camera
        settings["camera_w"] = self.camera_w
        settings["camera_h"] = self.camera_h
        settings["times_to_detect"] = self.times_to_detect
        settings["max_detection_time"] = self.max_detection_time
        settings["time_to_close"] = self.time_to_close

        return settings
    
    def fetch_cameras(self):
        cameras = QMediaDevices.videoInputs()

        if cameras:
            for camera in cameras:
                camera_name = camera.description()
                camera_resolutions = set()
                camera_resolutions_formatted = list()
                optimal_resolution = tuple()
                camera_id = None
                
                self.list_of_cameras.append(camera_name)

                for resolution in camera.photoResolutions():
                    w = resolution.width()
                    h = resolution.height()

                    if w >= 640 and h >= 480:
                        camera_resolutions.add((w, h))

                        if w <= 1920 and h <= 1080:
                            if not optimal_resolution:
                                optimal_resolution = (w, h)
                            elif w > optimal_resolution[0] and h > optimal_resolution[1]:
                                optimal_resolution = (w, h)

                camera_id = camera.id().toStdString()

                camera_resolutions = list(camera_resolutions)
                camera_resolutions.sort()
                
                for w, h in camera_resolutions:
                    camera_resolutions_formatted.append(f"{w} x {h}")

                self.camera_data[camera_name] = (camera_id, optimal_resolution, camera_resolutions, camera_resolutions_formatted)
    
    def load_camera(self):
        if self.list_of_cameras:
            if self.last_used_camera and self.last_used_camera in self.list_of_cameras:
                camera = self.last_used_camera
                w, h = self.last_used_resolution
                self.camera_index = self.list_of_cameras.index(camera)
            else:
                self.last_used_camera = None
                self.last_used_resolution = None
                camera = self.list_of_cameras[0]
                w, h = self.camera_data[camera][1]
                self.camera_index = 0

            camera_id = self.camera_data[camera][0]
            camera_resolutions = self.camera_data[camera][2]
            
            self.camera = camera_id
            self.camera_w = w
            self.camera_h = h

            for i in range(0, len(camera_resolutions)):
                if camera_resolutions[i][0] == w and camera_resolutions[i][1] == h:
                    self.camera_resolution_index = i
                    break
            
            if not self.last_used_camera:
                self.last_used_camera = camera
                self.last_used_resolution = self.camera_data[camera][1]
    
    def load_settings(self):
        if self.settings_path.is_file():
            try:
                file_stream = open(self.settings_path, 'r')
                settings = yaml.load(file_stream, Loader=yaml.CLoader)
                file_stream.close()
            except:
                return False
            else:
                self.last_used_camera = settings["last_used_camera"]
                if settings["last_used_resolution"]:
                    self.last_used_resolution = (settings["last_used_resolution"][0], settings["last_used_resolution"][1])
                else:
                    self.last_used_resolution = None
                self.times_to_detect = settings["times_to_detect"]
                self.max_detection_time = settings["max_detection_time"]
                self.time_to_close = settings["time_to_close"]
                return True
        else:
            return False
    
    def create_settings(self):
        settings = dict()
        settings["last_used_camera"] = self.default_last_used_camera
        settings["last_used_resolution"] = self.default_last_used_resolution
        settings["times_to_detect"] = self.default_times_to_detect
        settings["max_detection_time"] = self.default_max_detection_time
        settings["time_to_close"] = self.default_time_to_close

        file_stream = open(self.settings_path, 'w')

        yaml.dump(settings, file_stream, Dumper=yaml.CDumper)

        file_stream.close()
    
    def save_settings(self):
        settings = dict()
        settings["last_used_camera"] = self.last_used_camera
        if self.last_used_resolution:
            settings["last_used_resolution"] = [self.last_used_resolution[0], self.last_used_resolution[1]]
        else:
            settings["last_used_resolution"] = None
        settings["times_to_detect"] = self.times_to_detect
        settings["max_detection_time"] = self.max_detection_time
        settings["time_to_close"] = self.time_to_close

        file_stream = open(self.settings_path, 'w')

        yaml.dump(settings, file_stream, Dumper=yaml.CDumper)

        file_stream.close()
    
    def load_camera_from_index(self, camera_index, resolution_index):
        self.last_used_camera = self.list_of_cameras[camera_index]
        self.camera = self.camera_data[self.last_used_camera][0]
        self.camera_w = self.camera_data[self.last_used_camera][2][resolution_index][0]
        self.camera_h = self.camera_data[self.last_used_camera][2][resolution_index][1]
        self.last_used_resolution = (self.camera_w, self.camera_h)
        self.camera_index = camera_index
        self.camera_resolution_index = resolution_index

class SettingsUI(QDialog):
    def __init__(self, cameras, camera_data, current_camera, current_resolution, times_to_detect, max_detection_time, time_to_close, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")

        self.cameras = cameras
        self.camera_data = camera_data
        self.current_camera_index = current_camera
        self.current_resolution_index = current_resolution

        self.new_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)

        self.current_camera = QComboBox(self)
        self.current_camera.addItems(self.cameras)
        self.current_camera.setCurrentIndex(self.current_camera_index)
        self.current_camera.currentIndexChanged.connect(self.update_resolutions)

        self.current_resolution = QComboBox(self)
        self.current_resolution.addItems(self.camera_data[self.cameras[self.current_camera_index]][3])
        self.current_resolution.setCurrentIndex(self.current_resolution_index)

        self.times_to_detect = QDoubleSpinBox(self)
        self.times_to_detect.setValue(times_to_detect)
        self.times_to_detect.setDecimals(0)

        self.max_detection_time = QDoubleSpinBox(self)
        self.max_detection_time.setValue(max_detection_time)
        self.max_detection_time.setDecimals(0)

        self.time_to_close = QDoubleSpinBox(self)
        self.time_to_close.setValue(time_to_close)
        self.time_to_close.setDecimals(0)

        self.form_layout.addRow("Camera:", self.current_camera)
        self.form_layout.addRow("Resolution:", self.current_resolution)
        self.form_layout.addRow("Times to detect:", self.times_to_detect)
        self.form_layout.addRow("Max detection time (seconds):", self.max_detection_time)
        self.form_layout.addRow("Time before closing (seconds):", self.time_to_close)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.new_layout.addLayout(self.form_layout)
        self.new_layout.addWidget(self.button_box)

        self.setLayout(self.new_layout)

    def update_resolutions(self):
        camera_index = self.current_camera.currentIndex()
        camera = self.cameras[camera_index]

        self.current_resolution.clear()
        self.current_resolution.addItems(self.camera_data[camera][3])
