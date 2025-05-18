# openai_api.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_task_suggestions(task_list):
    task_text = "\n".join([f"- {task}" for task in task_list])

    prompt = (
        "Here is a list of tasks from my Todoist. "
        "Please categorize them (e.g., work, home, errands), suggest priorities (low, medium, high), "
        "and identify anything that looks duplicate, vague, or should be broken into subtasks:\n\n"
        f"{task_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a productivity assistant helping a user organize tasks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
