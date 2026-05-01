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
    QWidget, QMessageBox, QDialog, QLineEdit, QFormLayout, QDialogButtonBox)

class Unsaved_warning(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Save database?")
        self.setText("Do you want to save the database before closing?")
        self.setInformativeText("If you don't save, your changes will be lost.")
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Save)

class Barrier_warning(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Barrier Warning!")
        self.setText("Cannot perform action while barrier is raised!")
        self.setStandardButtons(QMessageBox.Ok)

class Generic_warning(QMessageBox):
    def __init__(self, window_title, text, informative_text=None, critical=False, parent=None):
        super().__init__(parent)

        if critical:
            self.setIcon(QMessageBox.Critical)
        else:
            self.setIcon(QMessageBox.Warning)
        
        self.setWindowTitle(window_title)
        self.setText(text)

        if informative_text:
            self.setInformativeText(informative_text)

        self.setStandardButtons(QMessageBox.Ok)

class AddEdit_plate(QDialog):
    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)

        self.setMinimumSize(QSize(300, 100))

        self.edit_mode = False

        if edit_data:
            self.old_plate, self.old_name = edit_data
            self.edit_mode = True
            self.setWindowTitle("Edit plate")
        else:
            self.setWindowTitle("Add new plate")

        self.new_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)

        self.plate = QLineEdit(parent=self)
        self.name = QLineEdit(parent=self)

        if self.edit_mode:
            self.plate.setPlaceholderText(self.old_plate)
            self.plate.setText(self.old_plate)
            self.name.setPlaceholderText(self.old_name)
            self.name.setText(self.old_name)

        else:
            self.plate.setPlaceholderText("BN 18 CTL")
            self.name.setPlaceholderText("Hosu Adrian")

        self.form_layout.addRow("Plate:", self.plate)
        self.form_layout.addRow("Name:", self.name)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        if not edit_data:
            self.button_box.button(QDialogButtonBox.Ok).setText("Add")
        else:
            self.button_box.button(QDialogButtonBox.Ok).setText("Edit")

        self.new_layout.addLayout(self.form_layout)
        self.new_layout.addWidget(self.button_box)

        self.setLayout(self.new_layout)

class Remove_plate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(QSize(300, 80))

        self.setWindowTitle("Remove plate")

        self.new_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)

        self.plate = QLineEdit(parent=self)
        self.plate.setPlaceholderText("BN 18 CTL")

        self.form_layout.addRow("Plate to remove:", self.plate)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Ok).setText("Remove")

        self.new_layout.addLayout(self.form_layout)
        self.new_layout.addWidget(self.button_box)

        self.setLayout(self.new_layout)

class About(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("About")
        self.setText("ParkManager was created by Hosu Adrian")
        self.setStandardButtons(QMessageBox.Ok)