import sys
from time import time, sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import read_log as rl
import read_log_server as rls




#Timer thread (cambiar al formato nuevo)
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


#Worker class
class ReadLog(QObject):
    finished = pyqtSignal()
    new_msg = pyqtSignal(list)

    def run(self):
        while True:
            self.mensaje = rl.leer_mensajes()
            self.new_msg.emit(self.mensaje)
            self.finished.emit()

#Worker class
class ReadLogServer(QObject):
    finished = pyqtSignal()
    new_msg = pyqtSignal(list)

    def run(self):
        while True:
            self.mensaje = rls.leer_mensajes()
            self.new_msg.emit(self.mensaje)
            self.finished.emit()


    


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
        self.text_label3.resize(480, 30)
        self.text_label4.resize(480, 30)

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
        self.termino_timer = True
        self.timer_thread = ChangeBackgroundColorThread(self)


    #Metodos
    def runReadLog(self):
        #Step 2: Create a QThread object
        self.thread1 = QThread()
        # Step 3: Create a worker object
        self.worker1 = ReadLog()
        # Step 4: Move worker to the thread
        self.worker1.moveToThread(self.thread1)
        # Step 5: Connect signals and slots
        self.thread1.started.connect(self.worker1.run)
        #self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        self.worker1.new_msg.connect(self.agregar_mensaje_nuevo)
        # Step 6: Start the thread
        self.thread1.start()

    def runReadLogServer(self):
        #Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = ReadLogServer()
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        # Step 5: Connect signals and slots
        self.thread2.started.connect(self.worker2.run)
        #self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        self.worker2.new_msg.connect(self.agregar_mensaje_nuevo)
        # Step 6: Start the thread
        self.thread2.start()

    def agregar_mensaje_nuevo(self, mensaje_nuevo):
        color_texto = "black"
        if mensaje_nuevo[5] == "serverlog":
            color_texto = "red"
            msg = mensaje_nuevo[2]
        elif mensaje_nuevo[4] == "normal":
            msg = "["+mensaje_nuevo[1]+"] "+ mensaje_nuevo[2]+": "+mensaje_nuevo[3]

        elif mensaje_nuevo[4] == "bosses":
            color_texto = "blue"
            msg = "["+mensaje_nuevo[1]+"] "+ mensaje_nuevo[2]+": "+mensaje_nuevo[3]

        elif mensaje_nuevo[4] == "respawn":
            color_texto = "green"
            msg = "["+mensaje_nuevo[1]+"] "+ mensaje_nuevo[2]+": "+mensaje_nuevo[3]


        self.text_label0.setText(self.text_label1.text())
        self.text_label1.setText(self.text_label2.text())
        self.text_label2.setText(self.text_label3.text())
        self.text_label3.setText(self.text_label4.text())
        self.text_label4.setText(msg)

        if self.termino_timer == True:

            self.main_back.setStyleSheet("""background-color: rgba(239, 127, 26, 255);
                                        border: 2px solid rgba(0,0,0,255);""")


            self.termino_timer = False
            self.timer_thread.start()
            self.update()
        else:
            print("salto de timer")
            self.update()

    
    def mensaje_prueba(self):
        self.agregar_mensaje_nuevo("Probando Probando Probando")
    
    def change_background(self):
        self.main_back.setStyleSheet(self.background_style_css)

        self.termino_timer = True

    def close_window(self):
    
        self.close()
        sys.exit()



if __name__ == '__main__':
    My_Application = QApplication(sys.argv)
    MainWindow = MyNotification()
    MainWindow.show()
    MainWindow.runReadLog()
    MainWindow.runReadLogServer()

    sys.exit(My_Application.exec_())
    