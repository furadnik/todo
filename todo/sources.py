"""TODO sources."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

import requests


class Task:
    """Task impl."""

    def __init__(self, title: str, tags: list[str] | None = None, source: Source | None = None) -> None:
        """Save task info."""
        self._source = source
        self.title = title
        self.tags = tags or []

    def __hash__(self) -> int:
        """Hash task."""
        return hash(self.title + "!" + "#".join(self.tags))

    def __repr__(self) -> str:
        """Get a representation of Task."""
        return f"Task({self.title}, [{', '.join(self.tags)}])"

    def remove(self) -> None:
        """Remove self."""
        if self._source is not None:
            self._source.remove_task(self)
        else:
            raise ValueError("Cannot remove an unbound task.")

    def __eq__(self, o) -> bool:
        """Equal compare."""
        if isinstance(o, Task):
            return self.title == o.title and self.tags == o.tags
        elif isinstance(o, str):
            return self.title == o
        return NotImplemented

    def as_dict(self) -> dict:
        """Return the dictionary representation of a task."""
        return {"title": self.title, "tags": self.tags}


class Source(ABC):
    """A source of TODOs."""

    @abstractmethod
    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""

    @abstractmethod
    def remove_task(self, task: Task) -> None:
        """Remove task from todo."""

    @abstractmethod
    def add_task(self, title: str, tags: list[str] | None = None) -> Task:
        """Add task."""


class GoogleScriptSource(Source):
    """Source from google scripts."""

    def __init__(self, url: str) -> None:
        """Save url."""
        self._url = url

    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""
        res = requests.get(self._url, {"ged": "todoGet"}).text
        return (Task(x, source=self) for x in (res.split("\n") if res else []))

    def remove_task(self, task: Task) -> None:
        """Remove task."""
        requests.get(self._url, {"ged": "taskRemo", "task": task.title})

    def add_task(self, title: str, tags: list[str] | None = None) -> Task:
        """Remove task."""
        requests.get(self._url, {"ged": "taskAdd", "task": title})
        return Task(title, source=self)


class LocalSource(Source):
    """Source storing tasks locally."""

    def __init__(self, initial: list[str | dict]) -> None:
        """Save url."""
        self.tasks = [({"title": x} if isinstance(x, str) else x)
                      for x in initial]

    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""
        return (Task(**x, source=self) for x in self.tasks)

    def remove_task(self, task: Task) -> None:
        """Remove task."""
        self.tasks = [x for x in self.tasks if Task(**x) != task]

    def add_task(self, title: str, tags: list[str] | None = None) -> Task:
        """Remove task."""
        task_repr: dict = {"title": title, "tags": tags}
        if task_repr not in self.tasks:
            self.tasks.append(task_repr)
        return Task(**task_repr, source=self)


class TagSource(Source):
    """Get a sub-todolist with just specified tags."""

    def __init__(self, source: Source, tags: list[str]) -> None:
        """Save the source and filter tags."""
        self._source = source
        self._tags = tags

    def fetch(self) -> Iterable[Task]:
        """Fetch tasks."""
        for task in self._source.fetch():
            if not all(x in task.tags for x in self._tags):
                continue
            task_dict = task.as_dict()
            task_dict["tags"] = [x for x in task_dict["tags"] if x not in self._tags]
            yield Task(**task_dict, source=self._source)

    def remove_task(self, task: Task) -> None:
        """Remove task from todo."""
        task_dict = task.as_dict()
        task_dict["tags"] += self._tags
        self._source.remove_task(Task(**task_dict, source=self._source))

    def add_task(self, title: str, tags: list[str] | None = None) -> Task:
        """Add task."""
        tags = tags or []
        tags += self._tags
        task_dict = self._source.add_task(title, tags).as_dict()
        task_dict["tags"] = [x for x in task_dict["tags"] if x not in self._tags]
        return Task(**task_dict, source=self)
