# openai_api.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_task_summary(task_descriptions):
    task_text = "\n".join(task_descriptions)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful productivity assistant that helps users improve their task management using Todoist. "
                "You are concise, practical, and focused on helping the user better organize their time and priorities."
            )
        },
        {
            "role": "user",
            "content": (
                "Here is a structured list of tasks and subtasks from my Todoist, including project, section, labels, priority, due date, and description:\n\n"
                f"{task_text}\n\n"
                "First, give me an overview in paragraph form about the state of my task list—balance, focus, organization, and areas for improvement. "
                "Take a look at existing categories and let me know if I should recategorize anything or create new categories altogether."
                "Suggest priorities if you think I should have them (low, medium, high), and identify any duplicates or vague entries."
                "Help me think about due dates as well and suggest if I need to change any, either because I have too many on a given day or because one is dependent on another for any reason you might think of."
                "Then ask: 'How many specific, actionable suggestions would you like?' Don't give any suggestions yet—just the summary and that one question."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-4o-mini if you're optimizing cost
        messages=messages,
        temperature=0.5,
    )

    return response.choices[0].message.content, messages


def get_task_improvement_suggestions(messages, num_suggestions):
    messages.append({
    "role": "user",
    "content": f"I’d like {num_suggestions} specific, actionable suggestions. Please list each one on its own line starting with '- '."
    })


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
    )

    return response.choices[0].message.content
