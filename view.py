import os
import sys

from PySide6.QtCore import (Qt, QSize, Signal)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QSpinBox, QComboBox, QSizePolicy, QPushButton,
    QStyle
)


def image_path(relative_path):
    base_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "images")
    return os.path.join(base_path, relative_path)


class Container(QWidget):
    def __init__(self, parent, layout="grid", tighten=False):
        super().__init__(parent)
        if layout == "grid":
            self._layout = QGridLayout(self)
        elif layout == "vbox":
            self._layout = QVBoxLayout(self)
        else:
            self._layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        if tighten:
            self._layout.setSpacing(1)

    def add_widget(self, *args):
        self._layout.addWidget(*args)

    def size_hint(self):
        return self._layout.sizeHint()


class ComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setIconSize(QSize(32, 16))


class Label(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setText(text)


class PushButton(QPushButton):
    def __init__(self, parent, is_play):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        if is_play:
            self.setCheckable(True)
            self.toggled.connect(self._toggled)
            self._toggled(self.isChecked())
        else:
            self.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))

    def _toggled(self, state):
        if state:
            self.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))


class SpinBox(QSpinBox):
    def __init__(self, parent, minimum, maximum, default, prefix=None, suffix=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setRange(minimum, maximum)
        self.setValue(default)
        if prefix:
            self.setPrefix(f"{prefix} ")
            self.setAlignment(Qt.AlignmentFlag.AlignLeading)
        elif suffix:
            self.setSuffix(f" {suffix}")
            self.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        else:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class MainContainer(QWidget):
    buttonToggled = Signal(bool)
    buttonClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setSpacing(1)
        self._label1 = Label(self, text="Location:")
        self._layout.addWidget(self._label1, 0, 0, 1, 1)
        self._container1 = Container(self, layout="hbox")
        self._container1_spinbox1 = SpinBox(self._container1, minimum=-300, maximum=299, default=0, prefix="X:")
        self._container1.add_widget(self._container1_spinbox1)
        self._container1_spinbox2 = SpinBox(self._container1, minimum=-300, maximum=299, default=0, prefix="Y:")
        self._container1.add_widget(self._container1_spinbox2)
        self._container1_label1 = Label(self._container1, text="Cap:")
        self._container1.add_widget(self._container1_label1)
        self._container1_spinbox3 = SpinBox(self._container1, minimum=1, maximum=20, default=1)
        self._container1.add_widget(self._container1_spinbox3)
        self._container1_label2 = Label(self._container1, text="Cycles:")
        self._container1.add_widget(self._container1_label2)
        self._container1_spinbox4 = SpinBox(self._container1, minimum=1, maximum=999999, default=1)
        self._container1.add_widget(self._container1_spinbox4)
        self._container1_label3 = Label(self._container1, text="Interval:")
        self._container1.add_widget(self._container1_label3)
        self._container1_spinbox5 = SpinBox(self._container1, minimum=0, maximum=120, default=60, suffix="s")
        self._container1.add_widget(self._container1_spinbox5)
        self._layout.addWidget(self._container1, 0, 1, 1, 1)

        self._label2 = Label(self, text="Troops:")
        self._layout.addWidget(self._label2, 1, 0, 1, 1)
        self._container2 = Container(self, layout="grid")
        self._container2_combobox1 = ComboBox(self._container2)
        self._container2.add_widget(self._container2_combobox1, 0, 0, 1, 1)
        self._container2_label1 = Label(self._container2, text="Quantity:")
        self._container2.add_widget(self._container2_label1, 0, 1, 1, 1)
        self._container2_spinbox1 = SpinBox(self._container2, minimum=1, maximum=9999999, default=1)
        self._container2.add_widget(self._container2_spinbox1, 0, 2, 1, 1)
        self._container2_combobox2 = ComboBox(self._container2)
        self._container2.add_widget(self._container2_combobox2, 1, 0, 1, 1)
        self._container2_label2 = Label(self._container2, text="Quantity:")
        self._container2.add_widget(self._container2_label2, 1, 1, 1, 1)
        self._container2_spinbox2 = SpinBox(self._container2, minimum=1, maximum=9999999, default=1)
        self._container2.add_widget(self._container2_spinbox2, 1, 2, 1, 1)
        self._container2_filler1 = QWidget(self._container2)
        self._container2.add_widget(self._container2_filler1, 1, 3, 1, 1)
        self._container2_button1 = PushButton(self._container2, is_play=True)
        self._container2.add_widget(self._container2_button1, 1, 4, 1, 1)
        self._container2_button2 = PushButton(self._container2, is_play=False)
        self._container2.add_widget(self._container2_button2, 1, 5, 1, 1)
        self._layout.addWidget(self._container2, 1, 1, 1, 1)

        self._label4 = QLabel("<font color='grey'>Nothing To Display..</font>")
        self._layout.addWidget(self._label4, 3, 0, 1, 2)

        self._container2_button1.toggled.connect(self.buttonToggled)
        self._container2_button2.clicked.connect(self.button_stop_clicked)

    def button_stop_clicked(self):
        self._container2_button1.setChecked(False)
        self.buttonClicked.emit()

    @property
    def attack_troop(self):
        return self._container2_combobox1.currentText()

    @attack_troop.setter
    def attack_troop(self, data):
        self._container2_combobox1.clear()
        for item in data:
            self._container2_combobox1.addItem(
                QIcon(image_path(data[item]["icon"])), item, userData=data[item]["data"]
            )

    @property
    def load_troop(self):
        return self._container2_combobox2.currentText()

    @load_troop.setter
    def load_troop(self, data):
        self._container2_combobox2.clear()
        for item in data:
            self._container2_combobox2.addItem(
                QIcon(image_path(data[item]["icon"])), item, userData=data[item]["data"]
            )

    @property
    def config(self):
        data = {
            "location": {
                "x": str(self._container1_spinbox1.value()),
                "y": str(self._container1_spinbox2.value())
            },
            "march": {
                "cap": self._container1_spinbox3.value(),
                "cycle": self._container1_spinbox4.value(),
                "interval": self._container1_spinbox5.value(),
                "troop": [
                    [self._container2_combobox1.currentData(), str(self._container2_spinbox1.value())],
                    [self._container2_combobox2.currentData(), str(self._container2_spinbox2.value())]
                ]
            }
        }
        return data

    def set_status(self, text):
        self._label4.setText(text)

    def reset_button(self):
        if self._container2_button1.isChecked():
            self._container2_button1.blockSignals(True)
            self._container2_button1.animateClick()
            self._container2_button1.blockSignals(False)
