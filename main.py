from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMainWindow, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL.ImageQt import ImageQt
import time
from PIL import ImageGrab
from random import random, randint
import sys

class GetScreenshot(QWidget):
	def __init__(self, bbox=None):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		print('init screen')
		self.setGeometry(100, 100, 300, 220)
		self.setWindowTitle('GetScreenshot')      
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowOpacity(0.3)
		
		self.bbox = (self.geometry().x(), self.geometry().y(), 
					 self.geometry().x()+self.geometry().width(),
					 self.geometry().y()+self.geometry().height())
		self.show() # bbox = (geometry.x(), geometry.y(), geometry.width(), geometry.height())
			
	def closeEvent(self, event):
		event.accept()
		app = QtCore.QCoreApplication.instance()
		app.closeAllWindows()
		QtCore.QCoreApplication.exit(0)   
		
	def moveEvent(self, event):        
		self.bbox = (self.geometry().x(), self.geometry().y(), 
					 self.geometry().x()+self.geometry().width(),
					 self.geometry().y()+self.geometry().height())
		
	def resizeEvent(self, event):
		self.bbox = (self.geometry().x(), self.geometry().y(), 
					 self.geometry().x()+self.geometry().width(),
					 self.geometry().y()+self.geometry().height())  
			
class Controller(QWidget):
	def __init__(self, bbox=None):
		super().__init__()        
		self.capturewindow = GetScreenshot()    
		self.debugger = Debugger()    
		self.initUI()
		
	def initUI(self):
		self.setGeometry(800, 300, 300, 220)
		self.setWindowTitle('Controller')
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)    
		captureScreenBtn = QPushButton('Capture', self)
		captureScreenBtn.clicked.connect(self.captureScreen)
	
		self.show()
	
	def captureScreen(self, bbox=None):

		bbox= self.capturewindow.bbox
		print(bbox)
		im = ImageGrab.grab(bbox)
		imqt = ImageQt(im)
		qim = QImage(imqt)
		pm = QPixmap(qim)
		self.debugger.resize(bbox[2]-bbox[0], bbox[3]-bbox[1])
		self.debugger.updateImage(pm)
		#print(bbox[2]-bbox[0], bbox[3]-bbox[1])

	def closeEvent(self, event):
		event.accept()
		app = QtCore.QCoreApplication.instance()
		app.closeAllWindows()
		QtCore.QCoreApplication.exit(0)
		
class Debugger(QWidget): 
	def __init__(self, bbox=None):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		self.setGeometry(2700, 800, 300, 220)
		self.setWindowTitle('Debugger') 
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)       
		
		self.label = QLabel(self) 
		#self.show()
		
	def updateImage(self, img):  
#         pixmap = QPixmap("images/test.jpg")
		self.label.setPixmap(img)
#         self.resize(pixmap.width(),pixmap.height())
		#self.show()

	def closeEvent(self, event):
		event.accept()
		app = QtCore.QCoreApplication.instance()
		app.closeAllWindows()
		QtCore.QCoreApplication.exit(0)
		
class MainWindow():
	def __init__(self):
		super().__init__()
		self.openwindow()
	
	def openwindow(self):      
		self.controller = Controller()    
		
app = QtCore.QCoreApplication.instance()
if app is None:
	app = QApplication(sys.argv)
screen = MainWindow()
sys.exit(app.exec_())