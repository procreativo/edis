#-*- coding: utf-8 -*-

# <Diálogo de configuraciones.>
# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

""" Preferencias """

import os

#from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QIcon
#from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings

from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.dialogos.preferencias import preferencias_general
from edis_c.interfaz.dialogos.preferencias import preferencias_editor
from edis_c.interfaz.dialogos.preferencias import preferencias_tema


class DialogoConfiguracion(QDialog):
    """ Clase QDialog preferencias """

    def __init__(self, parent=None):
        super(DialogoConfiguracion, self).__init__(parent)
        self.setWindowTitle(self.trUtf8("EDIS-C Preferencias"))
        layoutH = QHBoxLayout()

        self.generalConf = preferencias_general.ConfiguracionGeneral(self)
        self.editorConf = preferencias_editor.ConfiguracionEditor(self)
        self.temaConf = preferencias_tema.ConfiguracionTema(self)

        self.contenidos = QListWidget()
        self.contenidos.setViewMode(QListView.IconMode)
        self.contenidos.setIconSize(QSize(96, 84))
        self.contenidos.setMovement(QListView.Static)
        self.contenidos.setMaximumWidth(70)
        self.contenidos.setSpacing(3)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.generalConf)
        self.stack.addWidget(self.editorConf)
        self.stack.addWidget(self.temaConf)

        boton_guardar = QPushButton(self.trUtf8("Guardar"))
        boton_cerrar = QPushButton(self.trUtf8("Cerrar"))

        self.cargar_iconos()
        self.contenidos.setCurrentRow(0)

        layoutH.addWidget(self.contenidos)
        layoutH.addWidget(self.stack, 1)

        layoutBoton = QHBoxLayout()
        layoutBoton.addStretch(1)
        layoutBoton.addWidget(boton_guardar)
        layoutBoton.addWidget(boton_cerrar)

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.addLayout(layoutH)
        layoutPrincipal.addStretch(1)
        layoutPrincipal.addSpacing(10)
        layoutPrincipal.addLayout(layoutBoton)

        self.setLayout(layoutPrincipal)

        boton_guardar.clicked.connect(self.guardar)
        boton_cerrar.clicked.connect(self.close)

    def cambiar(self, actual, anterior):
        if not actual:
            actual = anterior

        self.stack.setCurrentIndex(self.contenidos.row(actual))

    def guardar(self):
        qsettings = QSettings()
        qsettings.beginGroup('editor')
        e = contenedor_principal.ContenedorMain().devolver_editor_actual()

        # General
        qsettings.setValue('paginaInicio',
            self.generalConf.checkPaginaInicio.isChecked())
        configuraciones.MOSTRAR_PAGINA_INICIO = \
        self.generalConf.checkPaginaInicio.isChecked()

        # Idioma
        idioma = self.generalConf.comboIdioma.currentText()
        qsettings.setValue('idioma', idioma)
        idioma = unicode(idioma) + '.qm'
        configuraciones.IDIOMA = os.path.join(recursos.IDIOMAS, idioma)

        # Márgen
        margen_linea = self.editorConf.spinMargen.value()
        qsettings.setValue('margenLinea', margen_linea)
        configuraciones.MARGEN = margen_linea

        qsettings.setValue('mostrarMargen',
            self.editorConf.checkMargen.isChecked())
        configuraciones.MOSTRAR_MARGEN = self.editorConf.checkMargen.isChecked()

         # Indentación
        qsettings.setValue('indentacion', self.editorConf.spinInd.value())
        configuraciones.INDENTACION = self.editorConf.spinInd.value()

        qsettings.setValue('checkInd', self.editorConf.checkInd.isChecked())
        configuraciones.CHECK_INDENTACION = self.editorConf.checkInd.isChecked()

        # Tipo de letra
        textoFuente = self.editorConf.botonFuente.text().replace(' ', '')
        configuraciones.FUENTE = textoFuente.split(',')[0]
        configuraciones.TAM_FUENTE = int(textoFuente.split(',')[1])
        qsettings.setValue('fuente', configuraciones.FUENTE)
        qsettings.setValue('fuenteTam', configuraciones.TAM_FUENTE)
        if e:
            e._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        # Sidebar
        qsettings.setValue('sidebar', self.editorConf.checkSideBar.isChecked())
        configuraciones.SIDEBAR = self.editorConf.checkSideBar.isChecked()

        # Tabs y espacios
        qsettings.setValue('tabs', self.editorConf.checkTabs.isChecked())
        configuraciones.MOSTRAR_TABS = self.editorConf.checkTabs.isChecked()

        # Wrap mode
        qsettings.setValue('wrap', self.editorConf.checkWrap.isChecked())
        configuraciones.MODO_ENVOLVER = self.editorConf.checkWrap.isChecked()

        # Minimapa
        qsettings.setValue('mini', self.editorConf.checkMini.isChecked())
        configuraciones.MINIMAPA = self.editorConf.checkMini.isChecked()
        configuraciones.OPAC_MIN = self.editorConf.spinMiniMin.value() / 100.0
        qsettings.setValue('opac_min', configuraciones.OPAC_MIN)
        configuraciones.OPAC_MAX = self.editorConf.spinMiniMax.value() / 100.0
        qsettings.setValue('opac_max', configuraciones.OPAC_MAX)

        contenedor_principal.ContenedorMain().resetear_flags_editor()
        qsettings.endGroup()
        contenedor_principal.ContenedorMain().actualizar_margen_editor()

        self.close()

    def cargar_iconos(self):
        configGeneral = QListWidgetItem(self.contenidos)
        configGeneral.setIcon(QIcon(recursos.ICONOS['general']))
        configGeneral.setText(self.trUtf8("General"))
        configGeneral.setTextAlignment(Qt.AlignHCenter)
        configGeneral.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        configEditor = QListWidgetItem(self.contenidos)
        configEditor.setIcon(QIcon(recursos.ICONOS['editor']))
        configEditor.setText(self.trUtf8("Editor"))
        configEditor.setTextAlignment(Qt.AlignHCenter)
        configEditor.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        configTema = QListWidgetItem(self.contenidos)
        configTema.setIcon(QIcon(recursos.ICONOS['tema']))
        configTema.setText(self.trUtf8("Tema"))
        configTema.setTextAlignment(Qt.AlignHCenter)
        configTema.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contenidos.currentItemChanged.connect(self.cambiar)