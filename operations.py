import pyautogui
import time

from PySide6.QtCore import (QObject, Signal)


# noinspection PyArgumentList
class FarmAway(QObject):
    finished = Signal(str)
    progress = Signal(str)
    _start = None

    def __init__(self, data):
        super().__init__()
        self._is_paused = False
        self._is_killed = False
        self._data = data

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def stop(self):
        self._is_killed = True

    def _elapsed(self):
        days, rem = divmod(time.time() - self._start, 86400)
        hour, rem = divmod(rem, 3600)
        mins, secs = divmod(rem, 60)
        if days:
            return f"{int(days):0>2}d {int(hour):0>2}h {int(mins):0>2}m {int(secs):0>2}s"
        elif hour:
            return f"{int(hour):0>2}h {int(mins):0>2}m {int(secs):0>2}s"
        else:
            return f"{int(mins):0>2}m {int(secs):0>2}s"

    def status(self, cycle, count, activity):
        self.progress.emit(
            f"<font color='grey'>Cycles</font> {cycle} of {self._data['march']['cycle']} "
            f"<font color='grey'>Marches</font> {count} "
            f"<font color='grey'>Elapsed</font>  {self._elapsed()} "
            f"<font color='grey'>Status</font> {activity}"
        )

    def run(self):
        self._start = time.time()
        count = 0
        cycle = 0
        has_troops = True
        while (cycle < self._data["march"]["cycle"]) and not self._is_killed:
            self.status(cycle, count, "Initializing Location")
            self._enter_location()
            for idx in range(self._data["march"]["cap"]):
                while self._is_paused and not self._is_killed:
                    time.sleep(1)
                if self._is_killed:
                    break
                self._open_location()
                self._target_dialog()
                if not idx:
                    self.status(cycle, count, "Setting Up March")
                    has_troops = self._set_troops()
                    if not has_troops:
                        self._is_killed = True
                        break
                else:
                    self._quick_repeat()
                self.status(cycle, count, f"Sending March #{idx + 1} of {self._data['march']['cap']}")
                self._send_march()
                count += 1
            if has_troops:
                cycle += 1
                sleeper = 0
                while ((sleeper < self._data["march"]["interval"]) and
                       (cycle < self._data["march"]["cycle"]) and not self._is_killed):
                    self.status(cycle, count, f"{self._data['march']['interval'] - sleeper}s Until Next Cycle..")
                    sleeper += 1
                    time.sleep(1)
        if not self._is_killed:
            self.status(cycle, count, "<font color='darkgreen'>Run Completed</font>")
            self.finished.emit(None)
        else:
            if not has_troops:
                self.status(cycle, count, "<font color='darkred'>Troop Not Found!</font>")
                self.finished.emit("Selected Troop Wasn't Found..")
            else:
                self.status(cycle, count, "<font color='darkred'>Run Interrupted!</font>")
                self.finished.emit("Script Was Interrupted By You..")

    def _enter_location(self):
        region = (540, 0, 360, 220)
        while not pyautogui.locateOnScreen(image="./images/train_l.png", region=region, confidence=0.9):
            if self._is_killed:
                return
            if found := pyautogui.locateOnScreen(image="./images/train_m.png", region=region, confidence=0.9):
                point = pyautogui.center(found)
                pyautogui.moveTo(point)
                pyautogui.leftClick()
            time.sleep(0.1)
        if found := pyautogui.locateOnScreen(image="./images/train_l.png", region=region, confidence=0.9):
            point = pyautogui.center(found)
            pyautogui.moveTo(point.x - 13, point.y)
            pyautogui.leftClick()
            pyautogui.write(self._data["location"]["x"])
            pyautogui.moveTo(point.x + 53, point.y)
            pyautogui.leftClick()
            pyautogui.write(self._data["location"]["y"])
            pyautogui.moveTo(point.x + 120, point.y)
            pyautogui.leftClick()

    def _open_location(self):
        while not pyautogui.pixelMatchesColor(714, 455, (33, 32, 33)):
            if self._is_killed:
                return
            time.sleep(0.1)
        pyautogui.moveTo(720, 450)
        pyautogui.leftClick()

    def _target_dialog(self):
        region = (750, 540, 120, 38)
        while not (found := pyautogui.locateOnScreen(image="./images/train_ma.png", region=region, confidence=0.9)):
            if self._is_killed:
                return
            time.sleep(0.1)
        point = pyautogui.center(found)
        pyautogui.moveTo(point.x, point.y)
        pyautogui.leftClick()

    def _set_troops(self):
        region = (358, 400, 711, 330)
        for troop in self._data["march"]["troop"]:
            if troop[0]:
                if found := pyautogui.locateOnScreen(image=troop[0], region=region, confidence=0.9):
                    point = pyautogui.center(found)
                    pyautogui.moveTo(point.x, point.y + 36)
                    pyautogui.leftClick()
                    pyautogui.write(troop[1])
                else:
                    return False
        return True

    @staticmethod
    def _send_march():
        region = (965, 803, 128, 36)
        if found := pyautogui.locateOnScreen(image="./images/train_ta.png", region=region, confidence=0.9):
            point = pyautogui.center(found)
            pyautogui.moveTo(point.x, point.y)
            pyautogui.leftClick()

    @staticmethod
    def _quick_repeat():
        region = (377, 806, 156, 29)
        if found := pyautogui.locateOnScreen(image="./images/train_ls.png", region=region, confidence=0.9):
            point = pyautogui.center(found)
            pyautogui.moveTo(point.x, point.y)
            pyautogui.leftClick()
