import win32gui
import win32con
from PIL import ImageGrab,Image,ImageChops
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot,Qt
import sys
import pythoncom
import PyHook3
from threading import Thread

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 541+900
        self.top = 649
        self.width = 601-110
        self.height = 758-382
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                       Qt.WindowCloseButtonHint |
                       Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1)
        l1 = QLabel(self)
        png = QPixmap('1.jpg')
        l1.setPixmap(png)
        button = QPushButton("刷新", self)
        # button.move(100, 70)
        button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        flush_game()
        self.initUI()


def flush_game():
    # 从顶层窗口向下搜索主窗口，无法搜索子窗口
    # FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
    handle = win32gui.FindWindow('#32770', '大家来找茬')

    #获取某个句柄的类名和标题
    title = win32gui.GetWindowText(handle)
    clsname = win32gui.GetClassName(handle)
    print(title,'------',clsname)
    # 打印句柄
    print(handle)
    # 强行显示界面后才好截图
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    # 将游戏窗口提到最前
    win32gui.SetForegroundWindow(handle)
    # 获取窗口位置
    wrect = win32gui.GetWindowRect(handle)
    print(wrect)
    img = ImageGrab.grab(wrect)
    contrast_img(img)


def contrast_img(img):
    print(img.size)
    i1 = img.crop((110, 382, 601, 758))
    # i1.save('0.jpg')
    i2 = img.crop((681, 382, 681 + 601 - 110, 758))
    # i2.save('00.jpg')
    i3 = ImageChops.invert(i2)
    Image.blend(i1, i3, 0.5).save('1.jpg')

global t1

def aaa(event):
    if event.Key == 'Oem_3':
        global t1
        flag = True
        if flag:
            falg = False
            t1 = Thread(target=create_qt5).start()
        else:
            t1.stop()
            t1 = Thread(target=create_qt5).start()
    return True

def create_qt5():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

def create_hook():
    hm = PyHook3.HookManager()
    hm.KeyUp = aaa
    hm.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    create_qt5()
