from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

gi.require_version("GObject", "2.0")
from gi.repository import GObject, Gio

from .models import Job, JobStage, JobStatus
from .utils.timefmt import format_datetime


class JobItem(GObject.GObject):
    id = GObject.Property(type=str)
    source_path = GObject.Property(type=str)
    created_at = GObject.Property(type=str)
    status = GObject.Property(type=str)
    stage = GObject.Property(type=str)
    progress = GObject.Property(type=float)
    message = GObject.Property(type=str)

    def __init__(self, job: Job):
        super().__init__()
        self.update_from_job(job)

    def update_from_job(self, job: Job) -> None:
        self.id = job.id
        self.source_path = job.source_path
        self.created_at = format_datetime(job.created_at)
        self.status = job.status.value
        self.stage = job.stage.value
        self.progress = job.progress
        self.message = job.message

    def set_status(self, status: JobStatus, stage: JobStage | None = None, message: str | None = None) -> None:
        self.status = status.value
        if stage:
            self.stage = stage.value
        if message is not None:
            self.message = message


class JobStore:
    def __init__(self) -> None:
        self.store = Gio.ListStore(item_type=JobItem)

    def add_job(self, job: Job) -> JobItem:
        item = JobItem(job)
        self.store.append(item)
        return item

    def __len__(self) -> int:
        return self.store.get_n_items()

    def __iter__(self):
        for idx in range(len(self)):
            yield self.store.get_item(idx)

    def clear(self) -> None:
        self.store.remove_all()
