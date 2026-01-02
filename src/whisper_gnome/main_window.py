from __future__ import annotations

from pathlib import Path
from typing import Iterable

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk

from .job_store import JobStore
from .job_runner import JobRunner
from .models import Job


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, application: Adw.Application):
        super().__init__(application=application, title="Whisper GNOME")
        self.set_default_size(960, 640)

        self.job_store = JobStore()
        self.runner = JobRunner()

        header_bar = self._build_headerbar()
        split_view = self._build_layout()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(header_bar)
        box.append(split_view)
        self.set_content(box)

    def _build_headerbar(self) -> Adw.HeaderBar:
        header = Adw.HeaderBar()

        add_btn = Gtk.Button(label="Añadir")
        add_btn.connect("clicked", self._on_add_clicked)
        header.pack_start(add_btn)

        transcribe_btn = Gtk.Button(label="Transcribir")
        transcribe_btn.connect("clicked", self._on_transcribe_clicked)
        header.pack_start(transcribe_btn)

        stop_btn = Gtk.Button(label="Detener")
        stop_btn.connect("clicked", self._on_stop_clicked)
        header.pack_start(stop_btn)

        prefs_btn = Gtk.Button(label="Preferencias")
        prefs_btn.connect("clicked", self._on_preferences_clicked)
        header.pack_end(prefs_btn)

        return header

    def _build_layout(self) -> Gtk.Widget:
        split = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        split.set_wide_handle(True)

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_top=12, margin_bottom=12, margin_start=12, margin_end=6, spacing=6)
        sidebar.append(Gtk.Label(label="Cola de trabajos", xalign=0))
        list_view = self._build_list_view()
        sidebar.append(list_view)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_top=12, margin_bottom=12, margin_start=6, margin_end=12, spacing=6)
        content.append(Gtk.Label(label="Estado", xalign=0))
        self.status_label = Gtk.Label(label="Listo", xalign=0)
        self.status_label.set_wrap(True)
        content.append(self.status_label)

        split.set_start_child(sidebar)
        split.set_end_child(content)
        return split

    def _build_list_view(self) -> Gtk.Widget:
        selection_model = Gtk.SingleSelection(model=self.job_store.store)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_list_item_setup)
        factory.connect("bind", self._on_list_item_bind)

        list_view = Gtk.ListView(model=selection_model, factory=factory)
        list_view.set_hexpand(True)
        list_view.set_vexpand(True)
        list_view.set_enable_rubberband(True)
        return list_view

    def _on_list_item_setup(self, _factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, margin_top=6, margin_bottom=6, margin_start=6, margin_end=6)
        title = Gtk.Label(xalign=0)
        title.add_css_class("heading")
        subtitle = Gtk.Label(xalign=0)
        subtitle.add_css_class("caption")
        subtitle.set_wrap(True)
        row.append(title)
        row.append(subtitle)
        list_item.set_child(row)

    def _on_list_item_bind(self, _factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        item = list_item.get_item()
        row = list_item.get_child()
        if not item or not row:
            return
        labels = row.get_children()
        title: Gtk.Label = labels[0]
        subtitle: Gtk.Label = labels[1]
        title.set_text(Path(item.source_path).name)
        subtitle.set_text(f"{item.status.upper()} · {item.stage} · {item.created_at}")

    def _on_add_clicked(self, _button: Gtk.Button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Selecciona archivos")
        dialog.set_modal(True)

        audio_filter = Gtk.FileFilter(name="Audio")
        audio_filter.add_mime_type("audio/*")
        video_filter = Gtk.FileFilter(name="Vídeo")
        video_filter.add_mime_type("video/*")
        filter_store = Gio.ListStore(item_type=Gtk.FileFilter)
        filter_store.append(audio_filter)
        filter_store.append(video_filter)
        dialog.set_filters(filter_store)

        def response_cb(dialog_: Gtk.FileDialog, result: Gio.AsyncResult):
            try:
                files = dialog_.open_multiple_finish(result)
            except Exception:
                return
            self._add_files(files)

        dialog.open_multiple(self, None, response_cb)

    def _add_files(self, files: Iterable[Gio.File]):
        for file in files:
            path = file.get_path()
            if not path:
                continue
            job = Job(source_path=path)
            self.job_store.add_job(job)
        self.status_label.set_text(f"{len(self.job_store)} trabajos en cola")

    def _on_transcribe_clicked(self, _button: Gtk.Button):
        self.runner.run_all(self.job_store)
        self.status_label.set_text("Procesando trabajos")

    def _on_stop_clicked(self, _button: Gtk.Button):
        self.runner.stop(self.job_store)
        self.status_label.set_text("Procesamiento detenido")

    def _on_preferences_clicked(self, _button: Gtk.Button):
        app = self.get_application()
        if app:
            app.activate_action("preferences", None)
