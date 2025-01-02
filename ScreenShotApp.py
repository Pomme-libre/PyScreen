import os
import sys
import shutil

from PySide6 import QtCore, QtWidgets, QtGui
import pyautogui
from pynput.mouse import Listener


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # イメージオブジェクト
        self.photoimage = None

        # スクリーンショットの座標変数
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.width = 0
        self.height = 0

        # スクリーンショットの回数変数
        self.COUNT = 0
        self.OVER_COUNT = 2

        # viewボタンの上限
        self.view = 0

        # Range Selectボタンを押していないときの対処
        self.no_signal = 0

        # アプリのメインウィンドウの設定
        self.setWindowTitle("PyScreen")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # メインウィンドウのウィジェット設定
        self.preview_label = QtWidgets.QLabel(
                "Image",
                alignment=QtCore.Qt.AlignCenter
                )
        self.renge_selection_button = QtWidgets.QPushButton("Range Selection")
        self.view_button = QtWidgets.QPushButton("View")
        self.save_button = QtWidgets.QPushButton("Save")
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.end_button = QtWidgets.QPushButton("Quit")

        # ウィジェットの配置
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.preview_label)
        self.layout.addWidget(self.renge_selection_button)
        self.layout.addWidget(self.view_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.end_button)

        # クリック時の応答
        self.renge_selection_button.clicked.connect(self.get_position)
        self.view_button.clicked.connect(self.take_screenshot)
        self.save_button.clicked.connect(self.save_dialog)
        self.reset_button.clicked.connect(self.image_reset)
        self.end_button.clicked.connect(self.window_close)

    # スクリーンショットをして、画像を表示
    @QtCore.Slot()
    def take_screenshot(self):
        if self.view == 0:
            if self.x1 >= self.x2 and self.y1 >= self.y2:
                self.width = self.x1 - self.x2
                self.height = self.y1 - self.y2
                if self.no_signal == 0:
                    pass
                else:
                    self.photoimage = pyautogui.screenshot(
                            region=(self.x2, self.y2, self.width, self.height)
                            )
                    self.photoimage.save(r'./Image/screenshot_region.png')
                    self.img = QtGui.QPixmap(r'./Image/screenshot_region.png')
                    self.preview_label.setPixmap(self.img)

            if self.x1 <= self.x2 and self.y1 >= self.y2:
                self.width = self.x2 - self.x1
                self.height = self.y1 - self.y2
                if self.no_signal == 0:
                    pass
                else:
                    self.photoimage = pyautogui.screenshot(
                            region=(self.x1, self.y2, self.width, self.height)
                            )
                    self.photoimage.save(r'./Image/screenshot_region.png')
                    self.img = QtGui.QPixmap(r'./Image/screenshot_region.png')
                    self.preview_label.setPixmap(self.img)

            if self.x1 >= self.x2 and self.y1 <= self.y2:
                self.width = self.x1 - self.x2
                self.height = self.y2 - self.y1
                if self.no_signal == 0:
                    pass
                else:
                    self.photoimage = pyautogui.screenshot(
                            region=(self.x2, self.y1, self.width, self.height)
                            )
                    self.photoimage.save(r'./Image/screenshot_region.png')
                    self.img = QtGui.QPixmap(r'./Image/screenshot_region.png')
                    self.preview_label.setPixmap(self.img)

            if self.x1 <= self.x2 and self.y1 <= self.y2:
                self.width = self.x2 - self.x1
                self.height = self.y2 - self.y1
                if self.no_signal == 0:
                    pass
                else:
                    self.photoimage = pyautogui.screenshot(
                            region=(self.x1, self.y1, self.width, self.height)
                            )
                    self.photoimage.save(r'./Image/screenshot_region.png')
                    self.img = QtGui.QPixmap(r'./Image/screenshot_region.png')
                    self.preview_label.setPixmap(self.img)

        else:
            pass

    # スクリーンショットの回数指定
    def click_counter(self):
        self.COUNT += 1
        if True if self.COUNT >= self.OVER_COUNT else False:
            self.listener.stop()

    # スクリーンショットの位置取得
    def on_click(self, x, y, button, pressed):
        """
        x : クリック時のX座標(浮動小数点型)
        y : クリック時のY座標(浮動小数点型)
        button : 左・右クリックかの判別
        pressed : クリック時はTrue, 話したときFalse
        """
        if self.COUNT == 0:
            self.x1, self.y1 = int(x), int(y)
        if self.COUNT == 1:
            self.x2, self.y2 = int(x), int(y)

        if pressed:
            self.click_counter()

    @QtCore.Slot()
    def get_position(self):
        """
        選択範囲のリセット
        """
        self.COUNT = 0
        self.view = 0
        self.no_signal += 1
        with Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

    # スクリーンショットの任意保存
    @QtCore.Slot()
    def save_dialog(self):
        self.file_name = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save File",
                "./Image/screenshot_region.png",
                "Images (*.png *.jpg *.jpeg)"
                )
        if self.file_name[0] == '':
            pass
        else:
            self.photoimage.save(self.file_name[0])

    @QtCore.Slot()
    def image_reset(self):
        self.preview_label.setText("Image")
        self.setGeometry(1200, 50, 280, 270)

    # ウィンドウの終了
    @QtCore.Slot()
    def window_close(self):
        widget.close()


if __name__ == "__main__":
    # スクリーンショット画像の一時保存フォルダの作成
    folder_pass = "./Image"
    file_pass_png = './Image/screenshot_region.png'
    file_pass_jpg = './Image/screenshot_region.jpg'
    file_pass_jpeg = './Image/screenshot_region.jpeg'

    if os.path.isdir(folder_pass):
        if os.path.isfile(file_pass_png or file_pass_jpg or file_pass_jpeg):
            shutil.rmtree('Image')
            os.makedirs(folder_pass)

        else:
            pass
    else:
        os.makedirs(folder_pass)

    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(280, 270)
    widget.show()

    sys.exit(app.exec())
