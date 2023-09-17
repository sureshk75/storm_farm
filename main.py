from PySide6.QtWidgets import (QApplication, QMessageBox)
from PySide6.QtCore import (QThread, Slot)

import pygetwindow

from view import *
from operations import *
import sys

APP_TITLE = "STORM FARM Enhanced By AlphaQ2"
ATTACK_TROOPS = {
            "Banshee": {"icon": "./images/icon_bs.png", "data": "./images/train_bs.png"},
            "Lava Jaw": {"icon": "./images/icon_lj.png", "data": "./images/train_lj.png"},
            "Longbowman": {"icon": "./images/icon_lb.png", "data": "./images/train_lb.png"},
            "Sand Strider": {"icon": "./images/icon_ss.png", "data": "./images/train_ss.png"},
            "Swift Strike Dragon": {"icon": "./images/icon_sd.png", "data": "./images/train_sd.png"},
            "Venge Wyrm": {"icon": "./images/icon_vw.png", "data": "./images/train_vw.png"}
        }
LOAD_TROOPS = {
            "": {"icon": "", "data": ""},
            "Armored Transport": {"icon": "./images/icon_at.png", "data": "./images/train_at.png"},
            "Pack Dragon": {"icon": "./images/icon_pd.png", "data": "./images/train_pd.png"}
        }


class MainUI(QWidget):
    _app_window = None
    _worker = None
    _thread = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(":/icons/icon.ico"))

        self._main = MainContainer(self)
        self._main.buttonToggled.connect(self._state_changed)
        self._main.buttonClicked.connect(self.thread_interrupt)

        self._container = Container(self)
        self._container.add_widget(self._main)

        self.setFixedSize(self._container.size_hint())
        self.move(0, 0)
        self._initialize()

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()
        sys.exit()

    def _initialize(self):
        self._main.attack_troop = ATTACK_TROOPS
        self._main.load_troop = LOAD_TROOPS
        try:
            self._app_window = pygetwindow.getWindowsWithTitle("Conquerors of Atlantis")[0]
            self._app_window.resizeTo(1440, 900)
            self._app_window.moveTo(0, 0)
            self._app_window.activate()
            self.show()
        except IndexError:
            QMessageBox.critical(self, APP_TITLE, "Did You Think I Would Magically Load The Game\n"
                                                  "For You? Move Your Lazy Ass.. Idiot!")
            self.close()
        self._thread = QThread()

    # noinspection PyUnresolvedReferences
    @Slot(bool)
    def _state_changed(self, state):
        if self._thread.isRunning():
            self._worker.resume() if state else self._worker.pause()
        if state:
            self._worker = FarmAway(data=self._main.config)
            self._worker.moveToThread(self._thread)
            self._worker.progress.connect(self._main.set_status)
            self._worker.finished.connect(self.thread_ended)
            self._thread.started.connect(self._worker.run)
            self._thread.start()

    def thread_interrupt(self):
        if self._thread.isRunning():
            self._worker.pause()
            self._worker.stop()

    def thread_ended(self, text):
        self._thread.quit()
        self._thread.wait()
        if text:
            QMessageBox.critical(self, APP_TITLE, f"{text}\nDon't You Know How To Run A Simple Script?")
        else:
            QMessageBox.information(self, APP_TITLE, "I Did All The Heavy Lifting As Usual, You Lazy Ass!")
        self._main.reset_button()


if __name__ == '__main__':
    app = QApplication()
    main = MainUI()
    app.exec()
