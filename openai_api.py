# openai_api.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_task_suggestions(task_list):
    task_text = "\n".join([f"- {task}" for task in task_list])

    prompt = (
        "Here is a structured list of tasks and subtasks from my Todoist. "
        "Please categorize them, suggest priorities (low, medium, high), identify duplicates, vague entries, and possible reorganizations. "
        "Suggest new categories I should be using if you detect I could organize my tasks better."
        "Help me think about due dates as well and suggest if I need to change any, either because I have too many on a given day or because one is dependent on another or for any other reason you might think of."
        "Subtasks are indented beneath their parent tasks:\n\n"
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
