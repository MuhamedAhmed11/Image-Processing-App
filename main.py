from PyQt5 import QtWidgets
from window import Ui_MainWindow
from PIL import Image
import sys
import numpy as np
import cv2
import pyqtgraph as pg
from subWindow import Ui_Form
import logging
logging.basicConfig(filename='test.log', level=logging.INFO)


class imageClass():
    def __init__(self):
        self.imageArray = []
        self.imageItem = []
        self.magnitudeArray = []
        self.copyMagnitudeArray = []
        self.phaseArray = []
        self.imaginaryArray = []
        self.realArray = []
        self.fourierArray = []

    def openImage(self, filepath):
        self.imageArray = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        dimensions = (500, 500)
        self.imageArray = cv2.resize(self.imageArray, dimensions)
        self.imageItem = pg.ImageItem(self.imageArray)
        self.imageItem.rotate(270)
    ############################# FOURIER TRANSFORT #######################################
        self.fourierArray = np.fft.fft2(self.imageArray)
        self.magnitudeArray = (np.abs(self.fourierArray))
        self.copyMagnitudeArray = 20*np.log(self.magnitudeArray)
        self.phaseArray = np.angle(self.fourierArray)
        self.imaginaryArray = np.imag(self.fourierArray)
        self.realArray = np.real(self.fourierArray)

    def mixingImages(img_1, img_2, firstComponentValueofImage_1, secondComponentValueOfImage_1, comboBoxText, comboBoxText_2):

        if (comboBoxText == 'Magnitude' and comboBoxText_2 == 'Phase'):
            logging.info(
                'User chose Magnitude as a first component and Phase as a second component for mixing')
            result_1 = np.add(np.multiply(firstComponentValueofImage_1, img_1.magnitudeArray),
                              np.multiply((1-firstComponentValueofImage_1), img_2.magnitudeArray))
            result_2 = np.add(np.multiply(secondComponentValueOfImage_1, img_1.phaseArray),
                              np.multiply((1-secondComponentValueOfImage_1), img_2.phaseArray))
        if (comboBoxText == 'Phase' and comboBoxText_2 == 'Magnitude'):
            logging.info(
                'User chose Phase as a first component and Magnitude as a second component for mixing')
            result_1 = np.add(np.multiply(secondComponentValueOfImage_1, img_1.magnitudeArray),
                              np.multiply((1 - secondComponentValueOfImage_1), img_2.magnitudeArray))
            result_2 = np.add(np.multiply(firstComponentValueofImage_1, img_1.phaseArray),
                              np.multiply((1-firstComponentValueofImage_1), img_2.phaseArray))
        if (comboBoxText == 'Real'and comboBoxText_2 == 'Imaginary'):
            logging.info(
                'User chose Real as a first component and Imaginary as a second component for mixing')
            result_1 = np.add(np.multiply(firstComponentValueofImage_1, img_1.realArray),
                              np.multiply((1 - firstComponentValueofImage_1), img_2.realArray))
            result_2 = np.add(np.multiply(secondComponentValueOfImage_1, img_1.imaginaryArray),
                              np.multiply((1-secondComponentValueOfImage_1), img_2.imaginaryArray))
        if (comboBoxText == 'Imaginary' and comboBoxText_2 == 'Real'):
            logging.info(
                'User chose Imaginary as a first component and Real as a second component for mixing')
            result_1 = np.add(np.multiply(secondComponentValueOfImage_1, img_1.realArray),
                              np.multiply((1 - secondComponentValueOfImage_1), img_2.realArray))
            result_2 = np.add(np.multiply(firstComponentValueofImage_1, img_1.imaginaryArray),
                              np.multiply((1-firstComponentValueofImage_1), img_2.imaginaryArray))
        if comboBoxText == 'Magnitude' or comboBoxText == 'Phase':
            combine = np.multiply(result_1, np.exp(1j*result_2))
            output = np.fft.ifft2(combine)
            return output
        if comboBoxText == 'Real' or comboBoxText == 'Imaginary':
            combine = np.add(result_1, (1j*result_2))
            output = np.fft.ifft2(combine)
            return output


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mixerOutput = ''
        self.imageBoxItem = ''
        self.imageBoxItem_2 = ''
        self.firstComponentValueofImage_1 = ''
        self.secondComponentValueOfImage_1 = ''
        self.firstComponentValueOfImage_2 = ''
        self.secondComponentValueOfImage_2 = ''
        self.componentBoxItem = ''
        self.componentBoxItem_2 = ''
        self.sliderValue = ''
        self.sliderValue2 = ''
        ##########
        self.comboBoxText = ''
        self.ui.mixerBtn.clicked.connect(self.OpenWindow)
        self.ui.browseImage1.clicked.connect(self.browseImage)
        self.ui.browseImage1_2.clicked.connect(self.browseImage2)
        self.ui.browseBtn1.clicked.connect(self.checkComboBox)
        self.ui.browsebtn2.clicked.connect(self.checkComboBox2)

        self.myImage_1 = imageClass()
        self.myImage_2 = imageClass()

    def browseImage(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName()
        if filepath[0] != '':
            self.myImage_1.openImage(filepath[0])
            self.ui.imageViewer1.addItem(self.myImage_1.imageItem)
            logging.info('User open first image')
        else:
            logging.warning(
                'YOU DID NOT CHOOSE ANY IMAGES, PLEASE CHOOSE IMAGE')

    def browseImage2(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName()
        if filepath[0] != '':
            self.myImage_2.openImage(filepath[0])
            self.ui.imageViewer2.addItem(self.myImage_2.imageItem)
            logging.info('User open second image')
        else:
            logging.warning(
                'YOU DID NOT CHOOSE ANY IMAGES, PLEASE CHOOSE IMAGE')

    def checkComboBox(self):
        self.comboBoxText = self.ui.comboBox.currentText()
        self.ui.graph1.clear()
        if self.comboBoxText == 'Magnitude':
            self.ui.graph1.addItem(pg.ImageItem(
                self.myImage_1.copyMagnitudeArray))
            logging.info('User chose Magnitude for first image')
        elif self.comboBoxText == 'Phase':
            self.ui.graph1.addItem(pg.ImageItem(self.myImage_1.phaseArray))
            logging.info('User chose Phase for first image')
        elif self.comboBoxText == 'Real':
            self.ui.graph1.addItem(pg.ImageItem(self.myImage_1.realArray))
            logging.info('User chose Real for first image')
        elif self.comboBoxText == 'Imaginary':
            self.ui.graph1.addItem(pg.ImageItem(self.myImage_1.imaginaryArray))
            logging.info('User chose Imaginary for first image')

    def checkComboBox2(self):
        self.comboBoxText = self.ui.comboBox_2.currentText()
        self.ui.graph2.clear()
        if self.comboBoxText == 'Magnitude':
            self.ui.graph2.addItem(pg.ImageItem(
                self.myImage_2.copyMagnitudeArray))
            logging.info('User chose Magnitude for second image')
        elif self.comboBoxText == 'Phase':
            self.ui.graph2.addItem(pg.ImageItem(self.myImage_2.phaseArray))
            logging.info('User chose Phase for second image')
        elif self.comboBoxText == 'Real':
            self.ui.graph2.addItem(pg.ImageItem(self.myImage_2.realArray))
            logging.info('User chose Real for second image')
        elif self.comboBoxText == 'Imaginary':
            self.ui.graph2.addItem(pg.ImageItem(self.myImage_2.imaginaryArray))
            logging.info('User chose Imaginary for second image')

    def values(self):
        self.mixerOutput = self.ui.outputComboBox.currentText()
        self.imageBoxItem = self.ui.imageComboBox1.currentText()
        self.sliderValue = self.ui.slider1.value()
        self.componentBoxItem = self.ui.componentComboBox1.currentText()

        self.imageBoxItem_2 = self.ui.ImageComboBox2.currentText()
        self.sliderValue2 = self.ui.horizontalSlider_2.value()
        self.componentBoxItem_2 = self.ui.componentComboBox2.currentText()

        if self.imageBoxItem == 'Image 1':
            logging.info('User chose first image for mixing')
            self.firstComponentValueofImage_1 = self.sliderValue/100
            self.firstComponentValueOfImage_2 = 1 - self.firstComponentValueofImage_1

        if self.imageBoxItem == 'Image 2':
            logging.info('User chose second image for mixing')
            self.firstComponentValueOfImage_2 = self.sliderValue/100
            self.firstComponentValueofImage_1 = 1 - self.firstComponentValueOfImage_2

        if self.imageBoxItem_2 == 'Image 1':
            logging.info('User chose first image for mixing')
            self.secondComponentValueOfImage_1 = self.sliderValue2/100
            self.firstComponentValueOfImage_2 = 1 - self.secondComponentValueOfImage_1

        if self.imageBoxItem_2 == 'Image 2':
            logging.info('User chose second image for mixing')
            self.secondComponentValueOfImage_2 = self.sliderValue2/100
            self.secondComponentValueOfImage_1 = 1 - self.secondComponentValueOfImage_2
        self.showResut()

    def showResut(self):
        mix = imageClass.mixingImages(self.myImage_1, self.myImage_2, self.firstComponentValueofImage_1,
                                      self.secondComponentValueOfImage_1, self.componentBoxItem, self.componentBoxItem_2)

        if self.ui.componentComboBox1.currentText() == 'Magnitude':
            self.ui.componentComboBox2.clear()
            self.ui.componentComboBox2.addItems(
                ['Phase', 'Uni Phase'])

        if self.ui.componentComboBox1.currentText() == 'Phase':
            self.ui.componentComboBox2.clear()
            self.ui.componentComboBox2.addItems(
                ['Magnitude', 'Uni Magnitude'])

        if self.ui.componentComboBox1.currentText() == 'Real':
            self.ui.componentComboBox2.clear()
            self.ui.componentComboBox2.addItems(
                ['Imaginary'])

        if self.ui.componentComboBox1.currentText() == 'Imaginary':
            self.ui.componentComboBox2.clear()
            self.ui.componentComboBox2.addItems(['Real'])

        if self.mixerOutput == 'Output 1':
            logging.info('User chose first Output to see mixing result')
            self.ui.graphicsView.clear()
            self.ui.graphicsView.addItem(pg.ImageItem(mix))
        elif self.mixerOutput == 'Output 2':
            logging.info('User chose second Output to see mixing result')
            self.ui.graphicsView.clear()
            self.ui.graphicsView_2.addItem(pg.ImageItem(mix))

    def OpenWindow(self):
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.show()
        self.ui.resultButton.clicked.connect(self.values)
        logging.info('User Open mixer window')
        self.ui.componentComboBox1.activated.connect(self.showResut)
        self.ui.componentComboBox2.activated.connect(self.showResut)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
