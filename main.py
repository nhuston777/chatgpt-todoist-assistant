from todoist_api import extract_task_descriptions, count_open_tasks
from openai_api import get_task_summary, get_task_improvement_suggestions

def prompt_task_limit(interactive=True, streamlit_obj=None):
    total = count_open_tasks()

    if interactive and streamlit_obj:
        st = streamlit_obj
        st.markdown(f"### You currently have **{total} open tasks** in Todoist.")
        return st.number_input(
            "How many tasks would you like to analyze?",
            min_value=1,
            max_value=total,
            value=min(10, total),
            step=1
        )
    else:
        print(f"You currently have {total} open tasks.")
        try:
            num = int(input(f"How many would you like to analyze? (1–{total}): "))
            return max(1, min(num, total))
        except ValueError:
            print("Invalid input. Defaulting to 10.")
            return min(10, total)


def run_productivity_assistant(task_limit):
    task_descriptions = extract_task_descriptions(limit=task_limit)

    summary, messages = get_task_summary(task_descriptions)
    print("\n🧠 GPT Summary:\n")
    print(summary)

    try:
        num = int(input("\nHow many suggestions would you like GPT to make? "))
    except ValueError:
        print("Invalid input. Defaulting to 3.")
        num = 3

    print("\nGenerating specific suggestions...\n")
    suggestions = get_task_improvement_suggestions(messages, num)

    approved_suggestions = []
    for line in suggestions.splitlines():
        stripped = line.strip()
        if not stripped or not stripped.startswith("- "):
            continue

        print(f"\n🔹 {stripped}")
        choice = input("Approve this change? (y/n): ").strip().lower()

        if choice == "y":
            approved_suggestions.append(stripped)
        elif choice == "q":
            print("Exiting review early.")
            break

    print("\n✅ Approved Suggestions:")
    for s in approved_suggestions:
        print(f"- {s}")


if __name__ == "__main__":
    limit = prompt_task_limit(interactive=False)
    run_productivity_assistant(limit)
