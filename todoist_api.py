# todoist_api.py

import requests
from config import TODOIST_API_TOKEN

def get_tasks():
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            print(f"- {task['content']} (id: {task['id']})")
    else:
        print(f"Error {response.status_code}: {response.text}")
