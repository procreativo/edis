#-*- coding: utf-8 -*-

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton

from PyQt4.QtCore import SIGNAL

from side_c import recursos

_instanciaBarraDeEstado = None


def BarraDeEstado(*args, **kw):
    global _instanciaBarraDeEstado
    if _instanciaBarraDeEstado is None:
        _instanciaBarraDeEstado = _BarraDeEstado(*args, **kw)

    return _instanciaBarraDeEstado


class _BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()

        v_layout = QVBoxLayout(self.widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        #self.buscador = WidgetBuscar(self)
        #self.addWidget(self.buscador)
        self.linea_columna = EstadoLineaColumna(self)
        self.connect(self, SIGNAL("messageChanged(QString)"),
            self.mensaje_terminado)

        self.addWidget(self.widget)

    def showMessage(self, mensaje, tiempo):
        self.linea_columna.hide()
        QStatusBar.showMessage(self, mensaje, tiempo)

    def mensaje_terminado(self, mensaje):
        if not mensaje:
            self.linea_columna.show()


class EstadoLineaColumna(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.parent = parent

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        self.texto = "Lin: %s | Col: %s"
        self.posicion_cursor = QLabel(self.trUtf8(
            self.texto % (0, 0)))
        layoutH.addWidget(self.posicion_cursor)

        layoutV.addLayout(layoutH)

    def actualizar_linea_columna(self, linea, columna):
        self.posicion_cursor.setText(
            self.trUtf8(self.texto % (linea, columna)))