import json
import os

import requests

files = os.listdir('all_tasks')
PATH = r'all_tasks/'
count = 0
for addres in files:
    tasks_for_db = []
    with open(f'{PATH}/{addres}', 'r', encoding='utf-8') as f:
        file_in_tasks = json.load(f)
        for task in file_in_tasks:
            d = {}
            m = 1000000
            for key, value in task.items():
                if key in ('answers', 'title', 'additional'):
                    d[key] = value
                elif key == 'question':
                    d['text_question'] = value
                elif key == 'time':
                    d['time_decision'] = value
                elif key == 'interviewCount':
                    d['interview_count'] = value
                elif key == 'blocks':
                    d['blocks'] = []
                    for block in value:
                        block['level'] = block.pop('ID')
                        d['blocks'].append(block)
                    for i in d['blocks']:
                        if m > i['level']:
                            m = i['level']
                            d['category'] = i['title']

            response = requests.post(
                'http://127.0.0.1:8000/create_question', json=d
            )
            # tasks_for_db.append(d)

    # with open(
    #     f'fixture/{addres.split('.')[0]}_db_v2.json', 'w', encoding='utf-8'
    # ) as f:
    #     json.dump(tasks_for_db, f, ensure_ascii=False, indent=2)
