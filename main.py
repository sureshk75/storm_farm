import pygetwindow
from PySide6.QtCore import (QThread, Slot)
from PySide6.QtWidgets import (QApplication, QMessageBox)

from operations import *
from view import *

APP_TITLE = "STORM FARM Enhanced By AlphaQ2"
ATTACK_TROOPS = {
            "Banshee": {"icon": "icon_bs.png", "data": "train_bs.png"},
            "Lava Jaw": {"icon": "icon_lj.png", "data": "train_lj.png"},
            "Longbowman": {"icon": "icon_lb.png", "data": "train_lb.png"},
            "Sand Strider": {"icon": "icon_ss.png", "data": "train_ss.png"},
            "Swift Strike Dragon": {"icon": "icon_sd.png", "data": "train_sd.png"},
            "Venge Wyrm": {"icon": "icon_vw.png", "data": "train_vw.png"}
        }
LOAD_TROOPS = {
            "": {"icon": "", "data": ""},
            "Armored Transport": {"icon": "icon_at.png", "data": "train_at.png"},
            "Pack Dragon": {"icon": "icon_pd.png", "data": "train_pd.png"}
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
        self.setWindowIcon(QIcon(image_path("icon.ico")))

        self._main = MainContainer(self)
        self._main.buttonToggled.connect(self._state_changed)
        self._main.buttonClicked.connect(self.thread_stopped)

        self._container = Container(self)
        self._container.add_widget(self._main)

        self.setFixedSize(self._container.size_hint())
        self.move(0, 0)
        self._initialize()

    def closeEvent(self, event):
        if self._thread and self._thread.isRunning():
            self._worker.stop()
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

    # noinspection PyUnresolvedReferences
    @Slot(bool)
    def _state_changed(self, state):
        if self._thread and self._thread.isRunning():
            self._worker.resume() if state else self._worker.pause()
        if state:
            self._thread = QThread()
            self._worker = FarmAway(data=self._main.config)
            self._worker.progress.connect(self._main.set_status)
            self._worker.finished.connect(self.thread_ended)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._thread.start()

    def thread_stopped(self):
        if self._thread and self._thread.isRunning():
            self._worker.stop()

    def thread_ended(self, text):
        self._thread.quit()
        self._thread.wait()
        if text:
            QMessageBox.critical(self, APP_TITLE, f"{text}\nDon't You Know How To Run A Simple Script?")
        else:
            QMessageBox.information(self, APP_TITLE, "I Did All The Heavy Lifting As Usual, You Lazy Ass!")
        self._main.reset_button()
        self._thread = None


if __name__ == '__main__':
    app = QApplication()
    main = MainUI()
    app.exec()
