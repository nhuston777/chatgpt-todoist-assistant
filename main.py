from todoist_api import get_tasks
from openai_api import get_task_suggestions

def extract_task_titles(limit=5):
    import requests
    from config import TODOIST_API_TOKEN

    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        task_titles = [task['content'] for task in tasks[:limit]]
        return task_titles
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

if __name__ == "__main__":
    try:
        limit_input = input("How many tasks would you like to analyze? (default is 5): ")
        limit = int(limit_input) if limit_input.strip() else 5
    except ValueError:
        print("Invalid input, using default of 5.")
        limit = 5

    task_titles = extract_task_titles(limit=limit)
    print("\nSending tasks to ChatGPT...\n")
    suggestions = get_task_suggestions(task_titles)
    print("\nGPT Suggestions:\n")
    print(suggestions)
