import json

PATH = r'D:\Dev\Interview_tasks\all_tasks\all_tasks_algo.json'

tasks = []


with open(PATH, 'r', encoding='utf-8') as f:
    all_ = json.load(f)
    for i in all_:
        tasks.append(i)

print(tasks)
