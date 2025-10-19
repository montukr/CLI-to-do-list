import json
import os
from datetime import datetime, timedelta

tasks = []

def load_tasks():
    global tasks
    try:
        if os.path.exists("tasks.json"):
            with open("tasks.json", 'r') as file:
                tasks = json.load(file)
            print(f"Loaded {len(tasks)} tasks")
        else:
            print("No tasks file found. Starting fresh.")
    except:
        print("Error loading tasks")
        tasks = []

def save_tasks():
    try:
        with open("tasks.json", 'w') as file:
            json.dump(tasks, file, indent=2)
        print("Tasks saved")
    except:
        print("Error saving tasks")

def add_task():
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty")
        return

    due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except:
            print("Invalid date format")
            return

    if not due_date:
        due_date = None

    task_id = len(tasks) + 1
    task = {
        'id': task_id,
        'description': description,
        'due_date': due_date,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    tasks.append(task)
    print(f"Task added: '{description}'")
    save_tasks()

def view_all_tasks():
    if not tasks:
        print("No tasks found")
        return

    print("\n=== ALL TASKS ===")
    print("-" * 50)

    for task in tasks:
        status = "✓" if task['completed'] else "○"
        due_info = f" | Due: {task['due_date']}" if task['due_date'] else ""

        urgency = ""
        if task['due_date'] and not task['completed']:
            try:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                days_left = (due_date - today).days

                if days_left < 0:
                    urgency = " ⚠️ OVERDUE"
                elif days_left == 0:
                    urgency = " 🔥 DUE TODAY"
                elif days_left <= 3:
                    urgency = " ⏰ DUE SOON"
            except:
                pass

        print(f"{status} [{task['id']}] {task['description']}{due_info}{urgency}")

    print("-" * 50)

def view_completed_tasks():
    completed_tasks = []
    for task in tasks:
        if task['completed']:
            completed_tasks.append(task)

    if not completed_tasks:
        print("No completed tasks")
        return

    print("\n=== COMPLETED TASKS ===")
    print("-" * 50)

    for task in completed_tasks:
        due_info = f" | Due: {task['due_date']}" if task['due_date'] else ""
        print(f"✓ [{task['id']}] {task['description']}{due_info}")

    print("-" * 50)

def view_pending_tasks():
    pending_tasks = []
    for task in tasks:
        if not task['completed']:
            pending_tasks.append(task)

    if not pending_tasks:
        print("No pending tasks")
        return

    print("\n=== PENDING TASKS ===")
    print("-" * 50)

    for task in pending_tasks:
        due_info = f" | Due: {task['due_date']}" if task['due_date'] else ""

        urgency = ""
        if task['due_date']:
            try:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                days_left = (due_date - today).days

                if days_left < 0:
                    urgency = " ⚠️ OVERDUE"
                elif days_left == 0:
                    urgency = " 🔥 DUE TODAY"
                elif days_left <= 3:
                    urgency = " ⏰ DUE SOON"
            except:
                pass

        print(f"○ [{task['id']}] {task['description']}{due_info}{urgency}")

    print("-" * 50)

def view_due_soon_tasks():
    due_soon_tasks = []
    today = datetime.now().date()

    for task in tasks:
        if task['due_date'] and not task['completed']:
            try:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                days_left = (due_date - today).days
                if 0 <= days_left <= 3:
                    due_soon_tasks.append(task)
            except:
                continue

    if not due_soon_tasks:
        print("No tasks due soon")
        return

    print("\n=== TASKS DUE SOON ===")
    print("-" * 50)

    for task in due_soon_tasks:
        due_info = f" | Due: {task['due_date']}"

        try:
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            today = datetime.now().date()
            days_left = (due_date - today).days

            if days_left == 0:
                urgency = " 🔥 DUE TODAY"
            else:
                urgency = " ⏰ DUE SOON"
        except:
            urgency = ""

        print(f"○ [{task['id']}] {task['description']}{due_info}{urgency}")

    print("-" * 50)

def mark_completed():
    view_pending_tasks()

    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except:
        print("Invalid task ID")
        return

    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task_found = True
            if task['completed']:
                print("Task is already completed")
            else:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Task marked as completed: '{task['description']}'")
                save_tasks()
            break

    if not task_found:
        print("Task not found")

def edit_task():
    view_all_tasks()

    try:
        task_id = int(input("Enter task ID to edit: "))
    except:
        print("Invalid task ID")
        return

    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task_found = True

            print("Leave empty to keep current value:")
            new_desc = input("New description: ").strip()
            new_due = input("New due date (YYYY-MM-DD) or empty to remove: ").strip()

            changed = False

            if new_desc:
                old_desc = task['description']
                task['description'] = new_desc
                print(f"Description updated: '{old_desc}' → '{new_desc}'")
                changed = True

            if new_due == "":
                if task['due_date']:
                    task['due_date'] = None
                    print("Due date removed")
                    changed = True
            elif new_due:
                try:
                    datetime.strptime(new_due, '%Y-%m-%d')
                    old_date = task['due_date']
                    task['due_date'] = new_due
                    print(f"Due date updated: {old_date} → {new_due}")
                    changed = True
                except:
                    print("Invalid date format")
                    return

            if changed:
                task['modified_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_tasks()
            else:
                print("No changes made")
            break

    if not task_found:
        print("Task not found")

def delete_task():
    view_all_tasks()

    try:
        task_id = int(input("Enter task ID to delete: "))
    except:
        print("Invalid task ID")
        return

    task_found = False
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            task_found = True
            confirm = input("Are you sure? (y/N): ").lower()
            if confirm == 'y':
                description = task['description']
                tasks.pop(i)
                print(f"Task deleted: '{description}'")
                save_tasks()
            else:
                print("Delete cancelled")
            break

    if not task_found:
        print("Task not found")

def show_summary():
    total = len(tasks)
    completed = 0
    pending = 0
    due_soon = 0

    today = datetime.now().date()

    for task in tasks:
        if task['completed']:
            completed += 1
        else:
            pending += 1

            if task['due_date']:
                try:
                    due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    days_left = (due_date - today).days
                    if 0 <= days_left <= 3:
                        due_soon += 1
                except:
                    pass

    print(f"\n📊 TASK SUMMARY")
    print("-" * 30)
    print(f"Total Tasks:     {total}")
    print(f"Completed:       {completed}")
    print(f"Pending:         {pending}")
    print(f"Due Soon:        {due_soon}")
    print("-" * 30)

def show_menu():
    print("\n" + "="*40)
    print("📋 TO-DO LIST MANAGER")
    print("="*40)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Completed Tasks")
    print("4. View Pending Tasks")
    print("5. View Tasks Due Soon")
    print("6. Mark Task as Completed")
    print("7. Edit Task")
    print("8. Delete Task")
    print("9. Task Summary")
    print("0. Exit")
    print("="*40)

def main():
    print("Welcome to the To-Do List Manager!")
    load_tasks()

    while True:
        show_menu()

        try:
            choice = int(input("Enter your choice (0-9): "))
        except:
            print("Please enter a valid number")
            continue

        if choice == 1:
            add_task()
        elif choice == 2:
            view_all_tasks()
        elif choice == 3:
            view_completed_tasks()
        elif choice == 4:
            view_pending_tasks()
        elif choice == 5:
            view_due_soon_tasks()
        elif choice == 6:
            mark_completed()
        elif choice == 7:
            edit_task()
        elif choice == 8:
            delete_task()
        elif choice == 9:
            show_summary()
        elif choice == 0:
            print("Thanks for using the To-Do List Manager!")
            print("Your tasks have been saved.")
            break
        else:
            print("Invalid choice. Please select 0-9.")

if __name__ == "__main__":
    main()
