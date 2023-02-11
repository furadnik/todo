"""Script entry point for CLI usage."""
from .client import TodoList
from .config import get_source_from_config
from argparse import ArgumentParser


source = get_source_from_config()
todo = TodoList(source)

ap = ArgumentParser()
sp = ap.add_subparsers()

todo_list = sp.add_parser("list", aliases=["l", "get", "g"], help="list tasks.")
todo_list.set_defaults(func=lambda _, td: [print(x.title) for x in td.get_tasks()])

todo_remo = sp.add_parser("remo", aliases=["r", "d", "delete"], help="delete task.")
todo_remo.add_argument("task", type=str, help="task title.")
todo_remo.set_defaults(func=lambda args, td: td.remove_task(args.task))

todo_add = sp.add_parser("add", aliases=["a", "c", "create"], help="create task.")
todo_add.add_argument("task", type=str, help="task title.")
todo_add.set_defaults(func=lambda args, td: td.add_task(args.task))

args = ap.parse_args()

args.func(args, todo)
