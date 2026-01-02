from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk


class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Preferencias")
        self._settings = Gio.Settings.new("com.pauiranzo.WhisperGnome")

        general_page = Adw.PreferencesPage(title="General")
        group = Adw.PreferencesGroup(title="Backend")

        backend_row = Adw.EntryRow(title="Comando backend")
        backend_row.set_text(self._settings.get_string("backend-command"))
        backend_row.connect("notify::text", self._on_backend_changed)
        group.add(backend_row)

        output_row = Adw.EntryRow(title="Directorio de salida")
        output_row.set_text(self._settings.get_string("default-output-dir"))
        output_row.connect("notify::text", self._on_output_dir_changed)
        group.add(output_row)

        language_row = Adw.EntryRow(title="Idioma")
        language_row.set_text(self._settings.get_string("language"))
        language_row.connect("notify::text", self._on_language_changed)
        group.add(language_row)

        model_row = Adw.EntryRow(title="Modelo")
        model_row.set_text(self._settings.get_string("model"))
        model_row.connect("notify::text", self._on_model_changed)
        group.add(model_row)

        general_page.add(group)
        self.add(general_page)

    def _on_backend_changed(self, row: Gtk.Editable, *_args) -> None:
        self._settings.set_string("backend-command", row.get_text())

    def _on_output_dir_changed(self, row: Gtk.Editable, *_args) -> None:
        self._settings.set_string("default-output-dir", row.get_text())

    def _on_language_changed(self, row: Gtk.Editable, *_args) -> None:
        self._settings.set_string("language", row.get_text())

    def _on_model_changed(self, row: Gtk.Editable, *_args) -> None:
        self._settings.set_string("model", row.get_text())
