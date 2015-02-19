# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


ACTIONS = ([
    {
        "name": "Archivo nuevo",
        "connection": "add_editor",
        "shortcut": "new"},
    {
        "name": "Abrir archivo",
        "connection": "open_file",
        "shortcut": "open",
        "separator": True},
    {
        "name": "Cerrar",
        "connection": "close_file",
        "shortcut": "close"},
    {
        "name": "Cerrar todo",
        "connection": "close_all"},
    {
        "name": "Cerrar los demás",
        "connection": "close_all_others"},
    {
        "name": "Guardar",
        "connection": "save_file",
        "shortcut": "save"},
    {
        "name": "Guardar como...",
        "connection": "save_file_as"},
    {
        "name": "Guardar todo",
        "connection": "save_all"},
    {
        "name": "Propiedades",
        "connection": "file_properties"},
    {
        "name": "Salir",
        "connection": "edis.close",
        "shortcut": "exit"}],
    # Menú editar
    [{
        "name": "Deshacer",
        "connection": "undo",
        "shortcut": "undo"},
    {
        "name": "Rehacer",
        "connection": "redo",
        "shortcut": "redo"},
    {
        "name": "Cortar",
        "connection": "cut",
        "shortcut": "cut"},
    {
        "name": "Copiar",
        "connection": "copy",
        "shortcut": "copy"},
    {
        "name": "Pegar",
        "connection": "paste",
        "shortcut": "paste"},
    {
        "name": "Seleccionar todo",
        "connection": "select_all",
        "shortcut": "select"},
    {
        "name": "Indentar",
        "connection": "indent",
        "shortcut": "indent"},
    {
        "name": "Quitar indentación",
        "connection": "unindent",
        "shortcut": "unindent"},
    {
        "name": "Duplicar línea",
        "connection": "duplicate_line",
        "shortcut": "duplicate"},
    {
        "name": "Eliminar línea",
        "connection": "delete_line",
        "shortcut": "delete"},
    {
        "name": "A minúsculas",
        "connection": "to_lowercase"},
    {
        "name": "A mayúsculas",
        "connection": "to_uppercase"},
    {
        "name": "A título",
        "connection": "to_title"},
    {
        "name": "Comentar",
        "connection": "comment",
        "shortcut": "comment"},
    {
        "name": "Descomentar",
        "connection": "uncomment",
        "shortcut": "uncomment"},
    {
        "name": "Mover hacia arriba",
        "connection": "move_up"},
    {
        "name": "Mover hacia abajo",
        "connection": "move_down"},
    {
        "name": "Configuración",
        "connection": "edis.show_settings"}],
    # Menú ver
    [{
        "name": "Pantalla completa",
        "connection": "edis.show_full_screen",
        "shortcut": "fullscreen"},
    {
        "name": "Mostrar/ocultar compilador",
        "connection": "edis.show_hide_output",
        "shortcut": "hide-output"},
    {
        "name": "Mostrar/ocultar toolbars",
        "connection": "edis.show_hide_toolbars",
        "shortcut": "hide-toolbar"},
    {
        "name": "Mostrar tabs y espacios en blanco",
        "connection": "show_tabs_and_spaces"},
    {
        "name": "Mostrar guías",
        "connection": "show_indentation_guides"},
    {
        "name": "Selector",
        "connection": "show_selector",
        "shortcut": "show-selector"},
    {
        "name": "Acercar",
        "connection": "zoom_in",
        "shortcut": "zoom-in"},
    {
        "name": "Alejar",
        "connection": "zoom_out",
        "shortcut": "zoom-out"}],
    # Menú buscar
    [{
        "name": "Buscar",
        "connection": "find",
        "shortcut": "find"},
    {
        "name": "Buscar y reemplazar",
        "connection": "find_and_replace",
        "shortcut": "find-replace"},
    {
        "name": "Ir a línea",
        "connection": "show_go_to_line",
        "shortcut": "go-to-line"}],
    # Menú ejecución
    [{
        "name": "Compilar",
        "connection": "build_source_code",
        "shortcut": "build"},
    {
        "name": "Ejecutar",
        "connection": "run_binary",
        "shortcut": "run"},
    {
        "name": "Compilar y ejecutar",
        "connection": "build_and_run",
        "shortcut": "build-run"},
    {
        "name": "Terminar programa",
        "connection": "stop_program",
        "shortcut": "stop"},
    {
        "name": "Limpiar construcción",
        "connection": "clean_construction"}],
    # Menú acerca de
    [{
        "name": "Reportar bug!",
        "connection": "edis.report_bug"},
    {
        "name": "Archivo de log",
        "connection": "show_log_file"},
    {
        "name": "Acerca de Edis",
        "connection": "edis.about_edis"},
    {
        "name": "Acerca de Qt",
        "connection": "edis.about_qt"}]
    )