import requests
import streamlit as st
TODOIST_API_KEY = st.secrets["TODOIST_API_TOKEN"]
from datetime import datetime

def extract_task_descriptions(limit=10):
    base_url = "https://api.todoist.com/rest/v2"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}

    # Fetch projects
    project_lookup = {}
    projects_resp = requests.get(f"{base_url}/projects", headers=headers)
    if projects_resp.status_code == 200:
        for project in projects_resp.json():
            project_lookup[project["id"]] = project["name"]
    else:
        print(f"Error fetching projects: {projects_resp.status_code}")

    # Fetch labels
    label_lookup = {}
    labels_resp = requests.get(f"{base_url}/labels", headers=headers)
    if labels_resp.status_code == 200:
        for label in labels_resp.json():
            label_lookup[label["id"]] = label["name"]
    else:
        print(f"Error fetching labels: {labels_resp.status_code}")

    # Fetch sections
    section_lookup = {}
    sections_resp = requests.get(f"{base_url}/sections", headers=headers)
    if sections_resp.status_code == 200:
        for section in sections_resp.json():
            section_lookup[section["id"]] = section["name"]
    else:
        print(f"Error fetching sections: {sections_resp.status_code}")

    # Fetch tasks
    tasks_resp = requests.get(f"{base_url}/tasks", headers=headers)
    if tasks_resp.status_code != 200:
        print(f"Error fetching tasks: {tasks_resp.status_code}: {tasks_resp.text}")
        return []

    tasks = tasks_resp.json()
    tasks_by_id = {task["id"]: task for task in tasks}
    children_by_parent = {}

    for task in tasks:
        parent_id = task.get("parent_id")
        if parent_id:
            children_by_parent.setdefault(parent_id, []).append(task)

    def format_task(task, indent=0):
        title = task.get("content", "Untitled Task")
        project = project_lookup.get(task.get("project_id"), "Unknown Project")
        labels = [label_lookup.get(lid, f"label-{lid}") for lid in task.get("labels", [])]
        priority = task.get("priority", 1)
        due = task.get("due")
        if due:
            due_date = due.get("date", "No due date")
            is_recurring = due.get("recurring", False)
        else:
            due_date = "No due date"
            is_recurring = False
        section = section_lookup.get(task.get("section_id"), "No section")
        description = task.get("description", "")
        created_at = task.get("created_at", "")
        created_short = created_at[:10] if created_at else "Unknown"

        indent_str = "  " * indent
        meta = (
            f'Project: {project}, '
            f'Section: {section}, '
            f'Labels: {", ".join(labels) if labels else "None"}, '
            f'Priority: {priority}, '
            f'Due: {due_date}{" (Recurring)" if is_recurring else ""}, '
            f'Created: {created_short}'
        )
        if description:
            meta += f', Description: {description}'

        line = f'{indent_str}- "{title}" ({meta})'
        lines = [line]

        children = sorted(children_by_parent.get(task["id"], []), key=lambda t: t.get("order", 0))
        for child in children:
            lines.extend(format_task(child, indent + 1))

        return lines

    top_level_tasks = [t for t in tasks if not t.get("parent_id")]
    top_level_tasks = sorted(top_level_tasks, key=lambda t: t.get("order", 0))[:limit]

    task_descriptions = []
    for task in top_level_tasks:
        task_descriptions.extend(format_task(task))

    return task_descriptions
