import json
import os

d = {
    'answers': [
        {'content': str, 'difficulty': str},
    ],
    'blocks': [
        {'title': str, 'level': int},
    ],
    'additional': str | None,
    'interview_count': int,
    'question': str,
    'time_decision': int,
    'title': str,
}


files = os.listdir('/all_tasks')
PATH = r'all_tasks/'

for addres in files:
    tasks_for_db = []
    with open(f'{PATH}/{addres}', 'r', encoding='utf-8') as f:
        file_in_tasks = json.load(f)
        for task in file_in_tasks:
            d = {}
            for key, value in task.items():
                if key in ('answers', 'question', 'title', 'additional'):
                    d[key] = value
                elif key == 'time':
                    d['time_decision'] = value
                elif key == 'interviewCount':
                    d['interview_count'] = value
                elif key == 'blocks':
                    d['blocks'] = []
                    for block in value:
                        block['level'] = block.pop('ID')
                        d['blocks'].append(block)

            tasks_for_db.append(d)

    with open(
        f'fixture/{addres.split('.')[0]}_db.json', 'w', encoding='utf-8'
    ) as f:
        json.dump(tasks_for_db, f, ensure_ascii=False, indent=2)
