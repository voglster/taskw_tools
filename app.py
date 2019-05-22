from collections import defaultdict
from taskw import TaskWarrior
from PyInquirer import prompt

w = TaskWarrior()

project_tasks = defaultdict(list)

for status, task_list in w.load_tasks().items():
    if status == "pending":
        for task in task_list:
            project_name = task.get("project")
            if project_name is not None and "." in project_name:
                project_name = project_name.split(".")[0]
            project_tasks[project_name].append(task)


def has_next(tasks):
    for t in tasks:
        if "next" in t.get("tags"):
            return True
    return False


def add_next_tag_to_task(task):
    if "tags" not in task:
        task["tags"] = []
    tags = task["tags"]

    if "next" not in tags:
        tags.append("next")


def prompt_user_to_pick_a_task(message, tasks):
    questions = [
        {
            "type": "list",
            "name": "task",
            "message": message,
            "choices": [{"name": t["description"], "value": t} for t in tasks],
        }
    ]

    return prompt(questions).get("task")


if __name__ == "__main__":
    for project, tasks in project_tasks.items():
        if project is not None and not has_next(tasks):
            task = prompt_user_to_pick_a_task(
                f"Which task is next for {project}?", tasks
            )
            add_next_tag_to_task(task)
            w.task_update(task)
