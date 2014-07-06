#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from edis_c import recursos
#from side_c.interfaz.dialogos import preferencias
from edis_c.interfaz.dialogos import pref
#from edis_c.interfaz.editor import acciones_


class MenuEditar(QObject):
    """ Items del menú Editar """

    def __init__(self, menu_editar, toolbar, ide):
        super(MenuEditar, self).__init__()

        self.ide = ide

        # Se cargan los shortcut
        self.atajoDeshacer = QShortcut(recursos.ATAJOS['deshacer'], self.ide)
        self.atajoRehacer = QShortcut(recursos.ATAJOS['rehacer'], self.ide)
        self.atajoCortar = QShortcut(recursos.ATAJOS['cortar'], self.ide)
        self.atajoCopiar = QShortcut(recursos.ATAJOS['copiar'], self.ide)
        self.atajoPegar = QShortcut(recursos.ATAJOS['pegar'], self.ide)

        # Conexiones
        self.connect(self.atajoDeshacer, SIGNAL("activated()"),
            self.ide.contenedor_principal.deshacer)
        self.connect(self.atajoRehacer, SIGNAL("activated()"),
            self.ide.contenedor_principal.rehacer)
        self.connect(self.atajoCortar, SIGNAL("activated()"),
            self.ide.contenedor_principal.cortar)
        self.connect(self.atajoCopiar, SIGNAL("activated()"),
            self.ide.contenedor_principal.copiar)
        self.connect(self.atajoPegar, SIGNAL("activated()"),
            self.ide.contenedor_principal.pegar)

        # Acciones
        self.accionDeshacer = menu_editar.addAction(QIcon(
            recursos.ICONOS['deshacer']), self.trUtf8("Deshacer"))
        self.cargar_status_tip(self.accionDeshacer,
            self.trUtf8("Deshacer cambios"))
        self.accionDeshacer.setShortcut(recursos.ATAJOS['deshacer'])
        self.accionRehacer = menu_editar.addAction(
            QIcon(recursos.ICONOS['rehacer']), self.trUtf8("Rehacer"))
        self.cargar_status_tip(self.accionRehacer,
            self.trUtf8("Rehacer cambios"))
        self.accionRehacer.setShortcut(recursos.ATAJOS['rehacer'])
        menu_editar.addSeparator()
        self.accionCortar = menu_editar.addAction(
            QIcon(recursos.ICONOS['cortar']), self.trUtf8("Cortar"))
        self.cargar_status_tip(self.accionCortar,
            self.trUtf8("Acción cortar"))
        self.accionCortar.setShortcut(recursos.ATAJOS['cortar'])
        self.accionCopiar = menu_editar.addAction(
            QIcon(recursos.ICONOS['copiar']), self.trUtf8("Copiar"))
        self.cargar_status_tip(self.accionCopiar,
            self.trUtf8("Acción copiar"))
        self.accionCopiar.setShortcut(recursos.ATAJOS['copiar'])
        self.accionPegar = menu_editar.addAction(
            QIcon(recursos.ICONOS['pegar']), self.trUtf8("Pegar"))
        self.cargar_status_tip(self.accionPegar,
            self.trUtf8("Acción pegar"))
        self.accionPegar.setShortcut(recursos.ATAJOS['pegar'])
        menu_editar.addSeparator()
        self.accionIndentarMas = menu_editar.addAction(
            QIcon(recursos.ICONOS['indentar']), self.trUtf8("Indentar más"))
        self.cargar_status_tip(self.accionIndentarMas,
            self.trUtf8("Indentar una o más líneas"))
        self.accionIndentarMenos = menu_editar.addAction(
            QIcon(recursos.ICONOS['desindentar']),
            self.trUtf8("Indentar menos"))
        self.cargar_status_tip(self.accionIndentarMenos,
            self.trUtf8("Sacar indentación a una o más líneas"))
        menu_editar.addSeparator()
        self.accionBorrar = menu_editar.addAction(self.trUtf8("Borrar"))
        menu_editar.addSeparator()
        self.accionSeleccionarTodo = menu_editar.addAction(
            self.trUtf8("Seleccionar todo"))
        self.cargar_status_tip(self.accionSeleccionarTodo,
            self.trUtf8("Seleccionar todo el código fuente"))
        menu_editar.addSeparator()
        self.accionConfiguracion = menu_editar.addAction(
            self.trUtf8("Configuración"))
        self.cargar_status_tip(self.accionConfiguracion,
            self.trUtf8("Configurar preferencias de EDIS-C"))
        #self.accionIrLinea = menu_editar.addAction(
            #self.trUtf8("Ir a linea"))

        # Conexiones a métodos
        self.accionDeshacer.triggered.connect(
            self.ide.contenedor_principal.deshacer)
        self.accionRehacer.triggered.connect(
            self.ide.contenedor_principal.rehacer)
        self.accionCortar.triggered.connect(
            self.ide.contenedor_principal.cortar)
        self.accionCopiar.triggered.connect(
            self.ide.contenedor_principal.copiar)
        self.accionPegar.triggered.connect(
            self.ide.contenedor_principal.pegar)
        self.accionConfiguracion.triggered.connect(
            self._configuraciones)
        self.accionIndentarMas.triggered.connect(
            self.ide.contenedor_principal.indentar_mas)
        self.accionIndentarMenos.triggered.connect(
            self.ide.contenedor_principal.indentar_menos)
        #self.accionIrLinea.triggered.connect(
            #self.ir_a_lin)

        # Toolbar - Items
        self.items_toolbar = {
            "deshacer": self.accionDeshacer,
            "rehacer": self.accionRehacer,
            "cortar": self.accionCortar,
            "copiar": self.accionCopiar,
            "pegar": self.accionPegar,
            "indentar": self.accionIndentarMas,
            "desindentar": self.accionIndentarMenos
            }

    def cargar_status_tip(self, accion, texto):
        self.ide.cargar_status_tips(accion, texto)

    def _configuraciones(self):
        self.preferencias = pref.DialogoConfiguracion(self.ide)
        self.preferencias.show()

    #def ir_a_lin(self):
        #ew = self.ide.contenedor_principal.devolver_editor_actual()
        #if ew:
            #acciones_.ir_a_linea_(ew)