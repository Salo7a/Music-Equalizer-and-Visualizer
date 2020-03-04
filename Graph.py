from PyQt5 import QtCore
import pyqtgraph as pg


class GraphWidget(pg.PlotWidget):
    resized = QtCore.pyqtSignal()

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.isSet = False
        self.isLive = False
        self.path = ''
        self.LivePos = 0
        self.name = ""
        self.data = []
        self.x = []
        self.y = []
        self.color = "w"
        self.sr = 20
        self.position = 0
        self.width = self.size().width()
        self.height = self.size().height()
        self.curve = self.plot(self.x, self.y, pen=(42, 130, 218), name=self.name)
        self.i = 0

    def setPlot(self, x, y, name="", pen="w"):
        self.color = pen
        if name != "":
            self.name = name
        self.x = x
        self.y = y
        self.curve = self.plot(self.x, self.y, pen=pen, name=self.name)
        self.isSet = True

    def UpdatePlot(self, x, y):
        self.x = x
        self.y = y
        self.curve.setData(self.x, self.y)

    def XRange(self, min, max):
        self.setXRange(min, max)

    def YRange(self, min, max):
        self.setYRange(min, max)


    def XPlus(self):
        self.curve.getViewBox().scaleBy(s=0.9, y=None)
        # ax = self.getAxis('bottom').range
        # if self.i < self.width / 2:
        #     print(int(ax[1] * 0.9))
        #     self.setXRange(0, ax[1] * 0.9)
        # else:
        #     self.setXRange(self.i - int(ax[0] * 0.9 / 2), self.i + int(ax[1] * 0.9 / 2))

    def XMinus(self):
        self.curve.getViewBox().scaleBy(s=1.1, y=None)
        # ax = self.getAxis('bottom').range
        # if self.i < self.width / 2:
        #     print(int(ax[1] * 1.1))
        #     self.setXRange(0, ax[1] * 1.1)
        # else:
        #     self.setXRange(self.i - int(ax[0] * 1.1 / 2), self.i + int(ax[1] * 1.1 / 2))

    def YPlus(self):
        # ax = self.getAxis('left').range
        # self.height = self.size().height()
        # self.setYRange(int(ax[0] * 0.9 / 2), int(ax[1] * 0.9 / 2))
        self.curve.getViewBox().scaleBy(s=0.9, x=None)

    def YMinus(self):
        # ax = self.getAxis('left').range
        # self.height = self.size().height()
        # self.setYRange(int(ax[0] * 1.1 / 2), int(ax[1] * 1.1 / 2))
        self.curve.getViewBox().scaleBy(s=1.1, x=None)

    def ZoomIn(self):
        self.XPlus()
        self.YPlus()

    def ZoomOut(self):
        self.XMinus()
        self.YMinus()

    def SetSampling(self, sr):
        self.sr = sr

    def SeekTo(self, per):
        if per > self.position:
            while per > self.position:
                self.curve.getViewBox().translateBy(x=((1 / self.sr) * 1000) * (len(self.data) / 100))
                self.position += 1
        elif per < self.position:
            while per < self.position:
                self.curve.getViewBox().translateBy(x=-((1 / self.sr) * 1000) * (len(self.data) / 100))
                self.position -= 1

    def GetCurve(self):
        return self.curve

    def GetViewBox(self):
        return self.curve.getViewBox()
