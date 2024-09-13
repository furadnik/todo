"""Main TODO list client."""
from typing import Iterable, Iterator, Optional, Union

from .sources import Source, Task


class TodoList:
    """TODO Client Representation."""

    def __init__(self, source: Source) -> None:
        """Save source."""
        self._source = source

    def __repr__(self) -> str:
        """Return a representation of a todo list."""
        return f"TodoList{{{', '.join(map(repr, self))}}}"

    def __contains__(self, item) -> bool:
        """Whether todo list contains item."""
        return item in list(self.get_tasks())

    def __iter__(self) -> Iterator[Task]:
        """Return iterator of task."""
        return iter(self.get_tasks())

    def __len__(self) -> int:
        """Get the number of tasks."""
        return len(list(iter(self)))

    def get_tasks(self) -> Iterable[Task]:
        """Get tasks on TODO list."""
        return self._source.fetch()

    def find_task_by_title(self, title: str, case_sensitive: bool = False) -> Optional[Task]:
        """Return first found task, or None."""
        ltitle = title.lower()
        for x in self.get_tasks():
            if x.title == title or (not case_sensitive and x.title.lower() == ltitle):
                return x
        return None

    def find_tasks_by_tag(self, tag: str, case_sensitive: bool = False) -> Iterable[Task]:
        """Return first found task, or None."""
        ltag = tag.lower()
        for x in self.get_tasks():
            if tag in x.tags or (not case_sensitive and ltag in {y.lower() for y in x.tags}):
                yield x

    def remove_task(self, title: str, case_sensitive: bool = False, fail: bool = False) -> None:
        """Remove task."""
        task = self.find_task_by_title(title, case_sensitive=case_sensitive)
        if task is not None:
            task.remove()
        elif fail:
            raise Exception("Task not on TODO list.")

    def add_task(self, title: str, tags: list[str] | None = None, allow_duplicate: bool = False,
                 fail: bool = False) -> Task:
        """Add a task."""
        if not allow_duplicate and (task := self.find_task_by_title(title)) is not None:
            if fail:
                raise Exception("Task already in TODO.")
            return task
        else:
            return self._source.add_task(title, tags)

    def import_task(self, task: Task, **kwargs) -> Task:
        """Import a task."""
        return self.add_task(task.title, tags=task.tags, **kwargs)

    def import_tasks(self, tasks: Iterable[Task], **kwargs) -> Iterable[Task]:
        """Import multiple tasks."""
        return [self.import_task(task, **kwargs) for task in tasks]

    def add_tasks(self, title_iter: Iterable[str], *args, **kwargs) -> Iterable[Task]:
        """Add tasks."""
        return [self.add_task(title, *args, **kwargs) for title in title_iter]

    def remove_tasks(self, title_iter: Iterable[Union[str, Task]], *args, **kwargs) -> None:
        """Add tasks."""
        for task in title_iter:
            if isinstance(task, Task):
                task.remove()
            else:
                self.remove_task(task, *args, **kwargs)
