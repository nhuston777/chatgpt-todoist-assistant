from openai_api import get_task_suggestions
from todoist_api import extract_task_descriptions

if __name__ == "__main__":
    try:
        limit_input = input("How many tasks would you like to analyze? (default is 5): ")
        limit = int(limit_input) if limit_input.strip() else 5
    except ValueError:
        print("Invalid input, using default of 5.")
        limit = 5

    task_descriptions = extract_task_descriptions(limit=limit)
    print("\nSending tasks to ChatGPT...\n")
    suggestions = get_task_suggestions(task_descriptions)
    print("\nGPT Suggestions:\n")
    print(suggestions)
