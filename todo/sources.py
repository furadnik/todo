"""TODO sources."""
from __future__ import annotations

from abc import ABC, abstractmethod
from functools import partial
from typing import Iterable

import requests


class Task:
    """Task impl."""

    def __init__(self, source: Source, title: str, tags: list[str] | None = None) -> None:
        """Save task info."""
        self._source = source
        self.title = title
        self.tags = tags or []

    def __hash__(self) -> int:
        """Hash task."""
        return hash(self.title + "!" + "#".join(self.tags))

    def remove(self) -> None:
        """Remove self."""
        self._source.remove_task(self)

    def __eq__(self, o) -> bool:
        """Equal compare."""
        if isinstance(o, Task):
            return self.title == o.title
        return self.title == o


class Source(ABC):
    """A source of TODOs."""

    @abstractmethod
    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""

    @abstractmethod
    def remove_task(self, task: Task) -> None:
        """Remove task from todo."""

    @abstractmethod
    def add_task(self, title: str) -> Task:
        """Add task."""


class GoogleScriptSource(Source):
    """Source from google scripts."""

    def __init__(self, url: str) -> None:
        """Save url."""
        self._url = url

    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""
        res = requests.get(self._url, {"ged": "todoGet"}).text
        return map(partial(Task, self), res.split("\n") if res else [])

    def remove_task(self, task: Task) -> None:
        """Remove task."""
        requests.get(self._url, {"ged": "taskRemo", "task": task.title})

    def add_task(self, title: str) -> Task:
        """Remove task."""
        requests.get(self._url, {"ged": "taskAdd", "task": title})
        return Task(self, title)


class LocalSource(Source):
    """Source storing tasks locally."""

    def __init__(self, initial: list[str]) -> None:
        """Save url."""
        self.tasks = initial

    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""
        return (Task(self, title) for title in self.tasks)

    def remove_task(self, task: Task) -> None:
        """Remove task."""
        self.tasks.remove(task.title)

    def add_task(self, title: str) -> Task:
        """Remove task."""
        if title not in self.tasks:
            self.tasks.append(title)
        return Task(self, title)
