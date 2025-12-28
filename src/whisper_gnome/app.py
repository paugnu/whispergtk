from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio

from .main_window import MainWindow
from .preferences import PreferencesWindow


class WhisperGnomeApplication(Adw.Application):
    def __init__(self) -> None:
        super().__init__(application_id="com.pauiranzo.WhisperGnome")
        self._main_window: MainWindow | None = None
        self._preferences_window: PreferencesWindow | None = None
        self.create_action("quit", self.quit)
        self.create_action("preferences", self.show_preferences)

    def do_activate(self) -> None:  # type: ignore[override]
        if not self._main_window:
            self._main_window = MainWindow(application=self)
        self._main_window.present()

    def show_preferences(self, *_args) -> None:
        if not self._preferences_window:
            self._preferences_window = PreferencesWindow(self)
        self._preferences_window.present()

    def create_action(self, name: str, callback) -> None:
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
