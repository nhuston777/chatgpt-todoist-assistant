from todoist_api import extract_task_descriptions
from openai_api import get_task_summary, get_task_improvement_suggestions

if __name__ == "__main__":
    try:
        limit_input = input("How many tasks would you like to analyze? (default is 5): ")
        limit = int(limit_input) if limit_input.strip() else 5
    except ValueError:
        print("Invalid input, using default of 5.")
        limit = 5

    task_descriptions = extract_task_descriptions(limit=limit)

    # Step 1: Get overview and ask how many suggestions to generate
    summary, messages = get_task_summary(task_descriptions)

    print("\n🧠 GPT Summary:\n")
    print(summary)

    try:
        num = int(input("\nHow many suggestions would you like GPT to make? "))
    except ValueError:
        print("Invalid input. Defaulting to 3 suggestions.")
        num = 3

    print("\nGenerating specific suggestions...\n")
    suggestions = get_task_improvement_suggestions(messages, num)

    # Step 2: Interactive CLI approval loop
    approved_suggestions = []
    print("\n📝 GPT Raw Suggestions:\n")
    print(suggestions)
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
