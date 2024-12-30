import os
from pathlib import Path
import json

BASE_PATH = Path(__file__).parent
TASK_LEARN = 'task_learn'
TASK_LEARN_PATH = BASE_PATH / TASK_LEARN


def get_all_folder_and_file_name(path, folders: list[str]) -> dict[str, list]:
    file_in_dir = {}
    for folder in folders:
        try:
            if folder != "all_":
                file_in_dir[folder] = os.listdir(path / folder)
        except Exception:
            ...
    return file_in_dir


def get_all_tasks(path, folder, tasks_file) -> list[list]:
    all_tasks = [[]]
    for file_name in tasks_file:
        with open(path / folder / file_name, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            for i in tasks:
                all_tasks[0].append(i)
    return all_tasks


def write_tasks(path, file_name, tasks):
    path.mkdir(exist_ok=True)
    for i in tasks:
        with open(path / f'all_tasks_{file_name}.json', 'a', encoding='utf-8') as f:
            json.dump(i, f, ensure_ascii=False, indent=4)


def main(path):
    task_folders = get_all_folder_and_file_name(path, os.listdir(path))
    for folder, tasks_file in task_folders.items():
        all_tasks = get_all_tasks(path, folder, tasks_file)
        write_tasks(path.parent / 'all_tasks', folder, all_tasks)


main(TASK_LEARN_PATH)
