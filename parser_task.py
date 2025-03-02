import json
import os
from typing import Any

import requests

FILES = os.listdir('all_tasks')
URL_CREATE_QUESTION = 'http://127.0.0.1:8000/create_question'
PATH = r'all_tasks/'


def parse_file(path: str, files: list[str], url_create_question=None) -> None:
    count = 0
    for address in files:
        tasks_for_db = []
        with open(f'{path}/{address}', 'r', encoding='utf-8') as f:
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
                                d['category'] = {'title': i['title']}

                if url_create_question is not None:
                    try:
                        response = requests.post(
                            url_create_question, json=d, timeout=2.0
                        )
                        response.raise_for_status()
                    except Exception as e:
                        count += 1
                else:
                    tasks_for_db.append(d)
                    create_task_for_db(address, tasks_for_db)


def create_task_for_db(
    address: str,
    tasks_for_db: list[dict[str, Any]],
    indent: int = 2,
    ensure_ascii: bool = False,
    encoding: str = 'utf-8',
    name_folder_to_save: str = 'fixture',
) -> None:
    from pathlib import Path

    path_to_save = Path(__file__).parent / name_folder_to_save
    path_to_save.mkdir(exist_ok=True)

    with open(
        f'{path_to_save}/000{address.split('.')[0]}_db_v2.json',
        'w',
        encoding=encoding,
    ) as f:
        json.dump(tasks_for_db, f, ensure_ascii=ensure_ascii, indent=indent)


def main(path: str, files: list[str], url_create_question: str = None) -> None:
    parse_file(
        path=path,
        files=files,
        url_create_question=url_create_question,
    )


if __name__ == '__main__':
    main(path=PATH, files=FILES)
