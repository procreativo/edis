#-*- coding: utf-8 -*-
import time
import sys
import os

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush

from PyQt4.QtCore import QProcess
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.nucleo import configuraciones


class EjecutarWidget(QWidget):

    def __init__(self):
        super(EjecutarWidget, self).__init__()
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        self.output = SalidaWidget(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Proceso
        self.proceso_actual = None
        self.ejecutable = None
        self.proceso = QProcess(self)
        self.proceso_ejecucion = QProcess(self)

        # Conexión
        self.connect(self.proceso, SIGNAL("readyReadStandardOutput()"),
            self.output.salida_estandar)
        self.connect(self.proceso, SIGNAL("readyReadStandardError()"),
            self.output.error_estandar)
        self.connect(self.proceso, SIGNAL(
            "finished(int, QProcess::ExitStatus)"), self.ejecucion_terminada)
        self.connect(self.proceso, SIGNAL("error(QProcess::ProcessError)"),
            self.ejecucion_error)

    def correr_compilacion(self, nombre_ejecutable, path):
        """ Se corre el comando gcc para la compilación """

        self.output.setCurrentCharFormat(self.output.formato_ok)
        self.ejecutable = nombre_ejecutable

        if sys.platform is not configuraciones.LINUX:
            path = "\"%s\"" % path

        comando = 'gcc -Wall -o %s %s' % (self.ejecutable, path)
        self.proceso.start(comando)

        archivo = path.split('/')[-1]
        self.output.setPlainText(
            'Compilando archivo:  %s\nDirectorio: %s ( %s )\n' %
            (archivo, os.path.dirname(path), time.ctime()))
        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_terminada(self, codigoError, exitStatus):
        """ valores de codigoError
            0 = Cuando se compila bien, aún con advertencias
            1 = Error en la compilación
        """

        formato = QTextCharFormat()
        formato.setAnchor(True)

        self.output.textCursor().insertText('\n\n')
        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(
                QBrush(QColor(recursos.COLOR_EDITOR['salida-exitosa'])))
            self.output.textCursor().insertText(
                self.trUtf8("¡Compilación exitosa!"), formato)

        else:
            formato.setForeground(
                QBrush(QColor(recursos.COLOR_EDITOR['salida-error'])))
            self.output.textCursor().insertText(
                self.trUtf8("No hubo compilación!"), formato)
        self.output.textCursor().insertText('\n')
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_error(self, error):
        pass

    def correr_programa(self):
        self.proceso_actual = self.proceso_ejecucion

        #if sys.platform is not configuraciones.TUX:
            #comando = '%s'
            #print "Ejecutando..."
            #self.ejecutable = 'C:\\Documents'
            #print self.ejecutable
            #self.proceso_ejecucion.start(self.ejecutable)
        comando = 'xterm -e bash -c ./%s'
        self.proceso_ejecucion.start(comando % self.ejecutable)


class SalidaWidget(QPlainTextEdit):

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self._parent = parent
        self.setReadOnly(True)

        # Formato para la salida estándar
        self.formato_ok = QTextCharFormat()
        #self.formato_ok.setForeground(recursos.COLOR_EDITOR['texto'])

        # Formato para la salida de error
        self.error_f = QTextCharFormat()
        self.error_f.setForeground(Qt.red)

        # Se carga el estilo
        self.cargar_estilo()

    def cargar_estilo(self):
        """ Carga estilo de color de QPlainTextEdit """

        tema = 'QPlainTextEdit {color: #afb4af; background-color: #1d1f21;}' \
        'selection-color: #FFFFFF; selection-background-color: #009B00;'

        self.setStyleSheet(tema)

    def salida_estandar(self):

        cp = self._parent.proceso
        text = cp.readAllStandardOutput().data()
        self.textCursor().insertText(text, self.error_f)

    def error_estandar(self):

        codificacion = 'utf-8'
        cursor = self.textCursor()
        proceso = self._parent.proceso
        texto = proceso.readAllStandardError().data().decode(codificacion)
        cursor.insertText(texto, self.error_f)