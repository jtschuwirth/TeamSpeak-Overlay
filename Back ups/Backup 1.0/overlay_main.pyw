import sys
from time import time, sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import read_log as rl
import threading





class ChangeBackgroundColorThread(QThread):

    def __init__(self, ventana):
        QThread.__init__(self)
        self.changeBackgroundColorTimer = QTimer()
        self.changeBackgroundColorTimer.moveToThread(self)
        self.changeBackgroundColorTimer.timeout.connect(ventana.change_background)
        

    def run(self):
        self.changeBackgroundColorTimer.start(1000)
        loop = QEventLoop()
        loop.exec_()


class MyNotification(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        # < Styles >
        self.background_style_css = """background-color: rgba(255, 255, 255, 255);
                                       border: 2px solid rgba(0,0,0,255);"""
        # </ Styles >

 
        # < Global Settings >

        #Tamaño de la ventana
        self.setFixedSize(510, 50)

        #Ubicacion de la ventana
        self.move(751, 0)
        # </ Global Settings >

        # < Main Style >
        self.main_back = QLabel(self)

        #tamaño del background
        self.main_back.resize(500, 40)

        #estilo del background
        self.main_back.setStyleSheet(self.background_style_css)
        # </ Main Style >
        

        # < Text Label >
        self.text_label0 = QLabel(self)
        self.text_label1 = QLabel(self)
        self.text_label2 = QLabel(self)
        self.text_label3 = QLabel(self)
        self.text_label4 = QLabel(self)

        #espacio que ocupa el texto
        self.text_label0.resize(0, 0)
        self.text_label1.resize(0, 0)
        self.text_label2.resize(0, 0)
        self.text_label3.resize(500, 30)
        self.text_label4.resize(500, 30)

        #mueve el texto
        self.text_label0.move(0, 0)
        self.text_label1.move(0, 0)
        self.text_label2.move(0, 0)
        self.text_label3.move(5, -2)
        self.text_label4.move(5, 13)
        
        #Color del texto
        self.text_label0.setStyleSheet("color: rgb(0, 0, 0);")
        self.text_label1.setStyleSheet("color: rgb(0, 0, 0);")
        self.text_label2.setStyleSheet("color: rgb(0, 0, 0);")
        self.text_label3.setStyleSheet("color: rgb(0, 0, 0);")
        self.text_label4.setStyleSheet("color: rgb(0, 0, 0);")

        #Cambiar el font y el tamaño
        self.text_label0.setFont(QFont('Arial', 10))
        self.text_label1.setFont(QFont('Arial', 10))
        self.text_label2.setFont(QFont('Arial', 10))
        self.text_label3.setFont(QFont('Arial', 10))
        self.text_label4.setFont(QFont('Arial', 10))
        # < Text Label >

        # < Header Style >
        #Que sea una ventana sin bordes y siempre on top.
        self.setWindowFlags(
        QtCore.Qt.FramelessWindowHint |
        QtCore.Qt.WindowStaysOnTopHint
        )

        #background transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # </ Header Style >

        
        #< Ultimos mensajes >

        #Caso base
        self.text_label0.setText("")
        self.text_label1.setText("")
        self.text_label2.setText("")
        self.text_label3.setText("")
        self.text_label4.setText("")
        # </ Ultimos mensajes >



        #Dejarlo falso para que el timer no funcione
        self.termino_timer = False
        self.timer_thread = ChangeBackgroundColorThread(self)

        self.lock = threading.Lock()


    #Metodos
    def agregar_mensaje_nuevo(self, mensaje_nuevo):
        self.text_label0.setText(self.text_label1.text())
        self.text_label1.setText(self.text_label2.text())
        self.text_label2.setText(self.text_label3.text())
        self.text_label3.setText(self.text_label4.text())
        self.text_label4.setText(mensaje_nuevo)

        if self.termino_timer == True:

            self.lock.acquire()
            self.main_back.setStyleSheet("""background-color: rgba(239, 127, 26, 255);
                                        border: 2px solid rgba(0,0,0,255);""")
            self.lock.release()


            self.termino_timer = False
            self.timer_thread.start()
            self.update()
        else:
            print("salto de timer")
            self.update()
    

    def mensaje_prueba(self):
        self.agregar_mensaje_nuevo("Probando Probando Probando")
    
    def change_background(self):
        self.lock.acquire()
        self.main_back.setStyleSheet(self.background_style_css)
        self.lock.release()

        self.termino_timer = True

    def close_window(self):
    
        self.close()
        sys.exit()



if __name__ == '__main__':
    My_Application = QApplication(sys.argv)
    MainWindow = MyNotification()
    MainWindow.show()


    t = threading.Thread(target=rl.leer_mensajes, args=("", MainWindow.agregar_mensaje_nuevo))
    t.start()

    sys.exit(My_Application.exec_())
    