from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELED = "canceled"


class JobStage(str, Enum):
    QUEUED = "queued"
    PREPROCESS = "preprocess"
    TRANSCRIBE = "transcribe"
    POSTPROCESS = "postprocess"
    COMPLETED = "completed"


@dataclass
class Job:
    source_path: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: JobStatus = JobStatus.PENDING
    stage: JobStage = JobStage.QUEUED
    progress: float = 0.0
    message: str = ""
