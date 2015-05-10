# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QPixmap,
    QLabel
    )

from PyQt4.QtCore import Qt

from src import ui


class AcercaDe(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle(self.tr("About Edis"))
        self.setMinimumWidth(485)
        box = QVBoxLayout(self)
        label_logo = QLabel()
        label_logo.setPixmap(QPixmap(":image/edis"))
        title_label = QLabel(self.tr("<h1>Edis</h1>\n<i>a simple "
                                     "cross-platform IDE for C</i>"))
        title_label.setAlignment(Qt.AlignRight)
        box_logo = QHBoxLayout()
        box_logo.addWidget(label_logo)
        box_logo.addWidget(title_label)
        box.addLayout(box_logo)
        lbl_version = QLabel(self.tr("<b>Version:</b> {0}").format(
                             ui.__version__))
        box.addWidget(lbl_version)
        lbl_link = QLabel("<b>Web:</b> <a href='%s'><span style='color: "
                          "#0197FD;'>%s</span></a>" % (ui.__web__, ui.__web__))
        lbl_sc = QLabel(self.tr("<b>Source Code:</b> <a href='{0}'><span"
                        " style='color: #0197FD;'>{1}</span></a>").format(
                        ui.__source_code__, ui.__source_code__))
        box.addWidget(lbl_link)
        box.addWidget(lbl_sc)
        # License
        box.addWidget(QLabel(self.tr("<b>License:</b> <i>Edis</i> is licensed "
                                     "under the terms of the <b>G</b>NU "
                                     "<b>P</b>ublic <b>L</b>icense "
                                     "version 3 or later.")))
        box.addWidget(QLabel(self.tr("<b>Author:</b> {0}").format(
                      ui.__author__)))
        box.addWidget(QLabel(self.tr("<b>Email:</b> {0}").format(
                      ui.__email_author__)))
        # Thanks to
        lbl_contributors = QLabel(self.tr("<b>Spatial thanks:</b> <a href="
                                  "'{0}'><span style=color: #0197FD;'>"
                                  "Contributors</span></a>").format(
                                  ui.__contributors__))
        box.addWidget(lbl_contributors)

        box_boton = QHBoxLayout()
        box_boton.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Ok"))
        box_boton.addWidget(btn_ok)
        box.addLayout(box_boton)

        # Conexiones
        btn_ok.clicked.connect(self.close)
        lbl_link.linkActivated['QString'].connect(self._open_link)
        lbl_sc.linkActivated['QString'].connect(self._open_link)
        lbl_contributors.linkActivated['QString'].connect(self._open_link)

    def _open_link(self, link):
        webbrowser.open_new(link)