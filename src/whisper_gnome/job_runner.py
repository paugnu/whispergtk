from __future__ import annotations

import gi

gi.require_version("GLib", "2.0")
from gi.repository import GLib

from .models import JobStage, JobStatus
from .job_store import JobItem, JobStore


class JobRunner:
    def __init__(self) -> None:
        self._running = False

    def run_all(self, store: JobStore) -> None:
        if self._running:
            return
        self._running = True
        for item in store:
            self._run_item(item)
        self._running = False

    def stop(self, store: JobStore) -> None:
        for item in store:
            if item.status == JobStatus.RUNNING.value:
                item.set_status(JobStatus.CANCELED, JobStage.COMPLETED, "Detenido")
        self._running = False

    def _run_item(self, item: JobItem) -> None:
        if item.status != JobStatus.PENDING.value:
            return
        item.set_status(JobStatus.RUNNING, JobStage.PREPROCESS, "Preparando")
        GLib.idle_add(self._finish_item, item)

    def _finish_item(self, item: JobItem) -> bool:
        item.set_status(JobStatus.DONE, JobStage.COMPLETED, "DONE")
        item.progress = 1.0
        return False
