"""Main TODO list client."""
from typing import Iterable, Optional, Iterator, Union
from .sources import Source, Task


class TodoList:
    """TODO Client Representation."""

    def __init__(self, source: Source) -> None:
        """Save source."""
        self._source = source

    def __contains__(self, item) -> bool:
        """Whether todo list contains item."""
        return item in list(self.get_tasks())

    def __iter__(self) -> Iterator[Task]:
        """Return iterator of task."""
        return self.get_tasks()

    def get_tasks(self) -> Iterable[Task]:
        """Get tasks on TODO list."""
        return self._source.fetch()

    def find_task_by_title(self, title: str) -> Optional[Task]:
        """Return first found task, or None."""
        for x in self.get_tasks():
            if x.title == title:
                return x

    def remove_task(self, title: str, fail: bool = False) -> None:
        """Remove task."""
        task = self.find_task_by_title(title)
        if task is not None:
            task.remove()
        elif fail:
            raise Exception("Task not on TODO list.")

    def add_task(self, title: str, allow_duplicate: bool = False, fail: bool = False) -> Task:
        """Add a task."""
        if not allow_duplicate and self.find_task_by_title(title) is not None:
            if fail:
                raise Exception("Task already in TODO.")
        else:
            return self._source.add_task(title)

    def add_tasks(self, title_iter: Iterator[str], *args, **kwargs) -> Iterator[Task]:
        """Add tasks."""
        return [self.add_task(title, *args, **kwargs) for title in title_iter]

    def remove_tasks(self, title_iter: Iterator[Union[str, Task]], *args, **kwargs) -> None:
        """Add tasks."""
        for task in title_iter:
            if isinstance(task, Task):
                task.remove()
            else:
                self.remove_task(task, *args, **kwargs)
