# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import bisect

from PyQt4.QtGui import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QToolButton,
    QStackedWidget,
    QMessageBox,
    QIcon,
    QMenu,
    QSizePolicy,
    QLabel
    )

from PyQt4.QtCore import (
    pyqtSignal,
    SIGNAL,
    QSize,
    Qt
    )

from src.ui.editor import editor
from src.ui.main import EDIS


class EditorWidget(QWidget):

    # Señales
    allFilesClosed = pyqtSignal()
    saveCurrentFile = pyqtSignal()
    fileClosed = pyqtSignal(int)
    recentFile = pyqtSignal('QStringList')

    def __init__(self):
        super(EditorWidget, self).__init__()
        self.not_open = True
        self._recents_files = []

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        # Combo container
        self.combo = ComboContainer(self)
        box.addWidget(self.combo)

        # Stacked
        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        self.connect(self.combo.combo_file,
                     SIGNAL("currentIndexChanged(int)"), self.change_item)

    def add_widget(self, widget):
        index = self.stack.addWidget(widget)
        if not self.combo.isVisible():
            self.combo.setVisible(True)
        self.stack.setCurrentIndex(index)

    def add_item_combo(self, text):
        self.combo.combo_file.addItem(text)
        self.combo.combo_file.setCurrentIndex(self.combo.combo_file.count() - 1)

    def remove_item_combo(self, index):
        self.combo.combo_file.removeItem(index)

    def change_item(self, index):
        editor_container = EDIS.componente("principal")
        self.stack.setCurrentIndex(index)
        editor_container.change_widget(index, True)

    def current_widget(self):
        return self.stack.currentWidget()

    def current_index(self):
        return self.stack.currentIndex()

    def widget(self, index):
        return self.stack.widget(index)

    def count(self):
        return self.stack.count()

    def close_file(self):
        self.remove_widget(self.current_widget(), self.current_index())

    def close_all(self):
        for index in range(self.count()):
            self.remove_widget(self.current_widget(), 0)

    def editor_modified(self, value):
        weditor = self.current_widget()
        index = self.current_index()
        if value and self.not_open:
            weditor.texto_modificado = True
        else:
            weditor.texto_modificado = False
        self.combo.set_modified(weditor, index, value)

    def _add_to_recent(self, filename):
        if not filename:
            return
        if filename not in self._recents_files:
            self._recents_files.append(filename)
            self.recentFile.emit(self._recents_files)

    def check_files_not_saved(self):
        value = False
        for index in range(self.count()):
            weditor = self.widget(index)
            value = value or weditor.texto_modificado
        return value

    def files_not_saved(self):
        files = []
        for index in range(self.count()):
            weditor = self.widget(index)
            if weditor.texto_modificado:
                files.append(weditor.filename)
        return files

    def opened_files(self):
        files = []
        for index in range(self.count()):
            weditor = self.widget(index)
            path = weditor.filename
            if not path:
                continue
            cursor_position = weditor.getCursorPosition()
            files.append([path, cursor_position])
        return files

    def remove_widget(self, widget, index):
        if not isinstance(widget, editor.Editor):
            return
        if index != -1:
            self.stack.setCurrentIndex(index)

            flags = QMessageBox.Yes
            flags |= QMessageBox.No
            flags |= QMessageBox.Cancel

            result = QMessageBox.No
            if widget.texto_modificado:
                result = QMessageBox.question(self, self.tr(
                                              "Archivo no guardado"),
                                              self.tr("El archivo <b>%s</b> "
                                              "no se ha guardado<br>"
                                              "¿Guardar?") % widget.filename,
                                              QMessageBox.Yes, QMessageBox.No,
                                              QMessageBox.Cancel)
                if result == QMessageBox.Cancel:
                    return
                elif result == QMessageBox.Yes:
                    self.saveCurrentFile.emit()
            #FIXME: para no
            self._add_to_recent(widget.filename)
            self.stack.removeWidget(widget)
            self.fileClosed.emit(index)
            self.remove_item_combo(index)
            if self.current_widget() is not None:
                self.current_widget().setFocus()
            else:
                self.allFilesClosed.emit()

    def add_symbols(self, symbols):
        self.combo.add_symbols_combo(symbols)


class ComboContainer(QWidget):

    def __init__(self, parent=None):
        super(ComboContainer, self).__init__()
        self._editor_widget = parent
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        self._lines_symbols = []

        # Basado en la GUI de Qt Creator
        # Combo archivos
        self.combo_file = QComboBox()
        self.combo_file.setIconSize(QSize(18, 18))
        self.combo_file.setContextMenuPolicy(Qt.CustomContextMenu)
        box.addWidget(self.combo_file)
        # Botón cerrar
        btn_close_editor = QToolButton()
        btn_close_editor.setObjectName("combo-button")
        btn_close_editor.setMaximumHeight(30)
        btn_close_editor.setToolTip(self.tr("Cerrar archivo"))
        btn_close_editor.setIcon(QIcon(":image/close"))
        box.addWidget(btn_close_editor)
        # Combo símbolos
        self.combo_symbols = QComboBox()
        self.combo_symbols.setIconSize(QSize(18, 18))
        self.combo_symbols.setMaximumWidth(250)
        box.addWidget(self.combo_symbols)
        # Label número de línea y columna
        self.label_line_row = QLabel()
        self.label_line_row.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label_line_row.setObjectName("combo-label")
        self.line_row = "# Lin: %s, Col: %s - %s"
        self.label_line_row.setText(self.line_row % (0, 0, 0))
        box.addWidget(self.label_line_row)

        dock = EDIS.componente("dock")

        # Conexiones
        self.connect(btn_close_editor, SIGNAL("clicked()"),
                     self._close_current_file)
        self.connect(dock, SIGNAL("updateSyntaxCheck(bool)"),
                     self._show_icon_checker)
        self.connect(self.combo_symbols, SIGNAL("activated(int)"),
                     self._go_to_symbol)
        self.connect(self.combo_file,
                     SIGNAL("customContextMenuRequested(const QPoint)"),
                     self._load_menu_combo_file)

    def update_cursor_position(self, line, row, lines):
        self.label_line_row.setText(self.line_row % (line, row, lines))

    def _load_menu_combo_file(self, point):
        """ Muestra el menú """

        menu = QMenu()
        editor_container = EDIS.componente("principal")
        compile_action = menu.addAction(self.tr("Compilar"))
        execute_action = menu.addAction(self.tr("Ejecutar"))
        menu.addSeparator()
        close_action = menu.addAction(self.tr("Cerrar archivo"))

        # Conexiones
        self.connect(compile_action, SIGNAL("triggered()"),
                     editor_container.build_source_code)
        self.connect(execute_action, SIGNAL("triggered()"),
                     editor_container.run_binary)
        self.connect(close_action, SIGNAL("triggered()"),
                     editor_container.close_file)

        menu.exec_(self.mapToGlobal(point))

    def _go_to_symbol(self, index):
        editor_container = EDIS.componente("principal")
        line = self._lines_symbols[index]
        editor_container.go_to_line(line)

    def _show_icon_checker(self, value):
        index = self._editor_widget.current_index()
        icon = QIcon()
        if not value:
            icon = QIcon(":image/bug")
            self.combo_file.setItemIcon(index, icon)
        else:
            self.combo_file.setItemIcon(index, icon)

    def _close_current_file(self):
        current_editor = self._editor_widget.current_widget()
        current_index = self._editor_widget.current_index()
        self._editor_widget.remove_widget(current_editor, current_index)

    def set_modified(self, weditor, index, modified):
        #FIXME: texto nuevo archivo
        if modified:
            text = " \u2022"  # Bullet caracter
            current_text = self.combo_file.currentText()
            self.combo_file.setItemText(index, current_text + text)
        else:
            if not weditor.filename:
                text = "Nuevo_archivo"
            else:
                text = weditor.filename
            self.combo_file.setItemText(index, text)

    def add_symbols_combo(self, symbols):
        """ Agrega símbolos al combo """

        self.combo_symbols.clear()
        lines = []
        for symbol in symbols:
            lines.append(symbol[0])
            to_combo = symbol[1][0]
            if symbol[1][1] == 'function':
                icon = QIcon(":image/function")
            elif symbol[1][1] == 'struct':
                icon = QIcon(":image/struct")
            self.combo_symbols.addItem(icon, to_combo)
        self._lines_symbols = lines

    def move_to_symbol(self, line):
        line += 1
        index = bisect.bisect(self._lines_symbols, line)
        self.combo_symbols.setCurrentIndex(index - 1)