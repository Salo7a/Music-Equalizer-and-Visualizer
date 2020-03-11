import pyqtgraph as pg
from PyQt5.QtGui import QBrush, QGradient


class GraphWidget(pg.PlotWidget):

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.gradient = QGradient(QGradient.DenseWater)
        self.gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
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

    def setPlotEQ(self, pen="w"):
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.YRange(0, 0.6)
        self.XRange(4, 100)
        self.color = pen
        self.curve = self.plot([], pen=(0, 0, 0, 0), name=self.name, fillLevel=-1, brush=QBrush(self.gradient))
        self.isSet = True

    def UpdatePlot(self, x, y):
        self.x = x
        self.y = y
        self.curve.setData(self.x, self.y)

    def UpdatePlotEQ(self, amp):
        self.y = amp[:int(len(amp) / 2)]
        self.curve.setData(self.y)

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


class MultiGraph(pg.PlotWidget):

    def __init__(self, **kwargs):
        super(MultiGraph, self).__init__(**kwargs)
        self.name = list()
        self.data = list()
        self.color = list()
        self.x = list()
        self.y = list()
        self.width = self.size().width()
        self.height = self.size().height()
        self.curves = list()
        self.i = 0

    def AddPlot(self, x, y, name="", pen="w"):
        if name != "":
            self.name = name
        self.color.append(pen)
        self.x.append(x)
        self.y.append(y)
        self.curves.append(self.plot(self.x[-1], self.y[-1], pen=pen, name=self.name))

    def UpdatePlot(self, x, y, i):
        self.x[i] = x
        self.y[i] = y
        self.curves[i].setData(self.x[i], self.y[i])

    def XPlus(self):
        self.curves[0].getViewBox().scaleBy(s=0.9, y=None)

    def XMinus(self):
        self.curves[0].getViewBox().scaleBy(s=1.1, y=None)

    def YPlus(self):
        # self.height = self.size().height()
        # if len(self.curves) == 0:
        #     ax = self.getAxis('left').range
        #     self.setXRange(int(ax[0] * 0.9 / 2), int(ax[1] * 0.9 / 2))
        # else:
        self.curves[0].getViewBox().scaleBy(s=0.9, x=None)

    def YMinus(self):
        # self.height = self.size().height()
        # if len(self.curves) == 0:
        #     ax = self.getAxis('left').range
        #     self.setXRange(int(ax[0] * 1.1 / 2), int(ax[1] * 1.1 / 2))
        # else:
        self.curves[0].getViewBox().scaleBy(s=1.1, x=None)

    def ZoomIn(self):
        self.XPlus()
        self.YPlus()

    def ZoomOut(self):
        self.XMinus()
        self.YMinus()

    def RemovePlot(self, x):
        if x < len(self.curves):
            self.removeItem(self.curves[x])
            self.legend.removeItem(self.name[x])
            del self.curves[x]
            del self.name[x]
            del self.data[x]
            del self.color[x]
            print(self.name)
            # self.UpdateLegend()

    def GetLen(self):
        return len(self.curves)

    def HidePlot(self, x):
        if x < len(self.curves):
            self.removeItem(self.curves[x])
            self.legend.removeItem(self.name[x])

    def ShowPlot(self, x):
        if x < len(self.curves):
            if self.curves[x] not in self.getPlotItem().items:
                self.addItem(self.curves[x])
