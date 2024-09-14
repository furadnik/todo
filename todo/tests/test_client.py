from functools import partial
from unittest import TestCase
from unittest.mock import Mock

from todo.client import Task, TodoList


class TestTodoList(TestCase):

    def setUp(self):
        self.source = Mock()
        self.todo_list = TodoList(self.source)
        self.source.fetch = lambda: map(partial(Task, source=self.todo_list), ["a", "b", "c"])

    def test_iterator(self):
        self.assertEqual([x.title for x in self.todo_list], ["a", "b", "c"])

    def test_contains(self):
        self.assertTrue("a" in self.todo_list)

    def test_contains_tasks(self):
        for task in self.todo_list:
            self.assertTrue(task in self.todo_list)

    def test_not_contains(self):
        self.assertFalse("d" in self.todo_list)

    def test_finding(self):
        self.assertIsNone(self.todo_list.find_task_by_title("task"))
        self.assertIsNotNone(self.todo_list.find_task_by_title("a"))
