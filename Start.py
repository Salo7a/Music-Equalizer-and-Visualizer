import sys

from PyQt5 import QtCore, QtWidgets

from EqualizerTest import Ui_Sliders
from Main import Ui_MainWindow


class Slider(Ui_Sliders, QtWidgets.QWidget):
    SendValues = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(Slider, self).__init__()
        self.setupUi(self)
        self.sliders[0].valueChanged.connect(lambda: self.test(0, self.sliders[0].value()))
        self.sliders[1].valueChanged.connect(lambda: self.test(1, self.sliders[1].value()))
        self.sliders[2].valueChanged.connect(lambda: self.test(2, self.sliders[2].value()))
        self.sliders[3].valueChanged.connect(lambda: self.test(3, self.sliders[3].value()))
        self.sliders[4].valueChanged.connect(lambda: self.test(4, self.sliders[4].value()))

    @QtCore.pyqtSlot()
    def test(self, index, value):
        self.SendValues.emit(index, value)


class ApplicationWindow(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setupUi(self)
        self.sliders = Slider()
        self.Equalizer.clicked.connect(self.on_button_clicked)
        self.sliders.SendValues.connect(self.on_SendValues)

    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        self.sliders.show()

    @QtCore.pyqtSlot(int, int)
    def on_SendValues(self, index, value):
        self.labels[index].setText(str(value))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
