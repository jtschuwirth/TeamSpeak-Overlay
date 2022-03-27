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


class Mensaje(QWidget):
    def __init__(self, parent, m_data=["","","","","",""]):
        QWidget.__init__(self, parent)
        grid = QGridLayout()
        self.setLayout(grid)

        self.resize(498, 40)
        self.m_data = m_data

        self.text_label_type = QLabel(self)
        self.text_label_type.setText(m_data[1])

        self.text_label_sender = QLabel(self)
        self.text_label_sender.setText(m_data[2])

        self.text_label_mensaje = QLabel(self)
        self.text_label_mensaje.setText(m_data[3])

        grid.addWidget(self.text_label_type, 0, 0)
        grid.addWidget(self.text_label_sender, 0, 1)
        grid.addWidget(self.text_label_mensaje, 0, 2)

        self.update()

    def cambiar_mensaje(self, m_data):
        if m_data[5] == "serverlog":
            color_texto = "red"
        elif m_data[4] == "bosses":
            color_texto = "blue"
        elif m_data[4] == "respawn":
            color_texto = "green"
        else:
            color_texto = "black"

        self.m_data = m_data
        self.text_label_type.setText(m_data[1])
        self.text_label_type.setStyleSheet("color: "+color_texto)
        self.text_label_type.setFixedWidth(27)
        self.text_label_type.setFont(QFont('Arial', 10))

        self.text_label_sender.setText(m_data[2])
        self.text_label_sender.setStyleSheet("color: "+color_texto)
        self.text_label_sender.setFixedWidth(60)
        self.text_label_sender.setFont(QFont('Arial', 10))

        self.text_label_mensaje.setText(m_data[3])
        self.text_label_mensaje.setStyleSheet("color: "+color_texto)
        self.text_label_mensaje.setFont(QFont('Arial', 10))
        self.update()



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
        
        #Widgets
        self.qwidget1 = Mensaje(self)
        self.qwidget2 = Mensaje(self)

        self.qwidget1.move(0,-8)
        self.qwidget2.move(0,8)


        # < Header Style >
        #Que sea una ventana sin bordes y siempre on top.
        self.setWindowFlags(
        QtCore.Qt.FramelessWindowHint |
        QtCore.Qt.WindowStaysOnTopHint
        )

        #background transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # </ Header Style >


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

        self.qwidget1.cambiar_mensaje(self.qwidget2.m_data)
        self.qwidget2.cambiar_mensaje(mensaje_nuevo)

        if self.termino_timer == True:

            self.main_back.setStyleSheet("""background-color: rgba(239, 127, 26, 255);
                                        border: 2px solid rgba(0,0,0,255);""")


            self.termino_timer = False
            self.timer_thread.start()
            self.update()
        else:
            print("salto de timer")
            self.update()
    
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
    