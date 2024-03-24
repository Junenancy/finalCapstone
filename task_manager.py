# Import necessary modules
import os
from datetime import datetime, date

# Define datetime format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to load tasks from tasks.txt
def load_tasks():
    # Check if tasks.txt exists
    if not os.path.exists("tasks.txt"):
        return []  # Return an empty list if file doesn't exist
    task_list = []

    # Read tasks from tasks.txt
    with open("tasks.txt", 'r') as task_file:
        for t_str in task_file:
            curr_t = {}
            # Split task attributes and populate dictionary
            task_components = t_str.strip().split(";")
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
            curr_t['completed'] = True if task_components[5] == "Yes" else False
            task_list.append(curr_t)

    return task_list

# Function to save tasks to tasks.txt
def save_tasks(task_list):
    # Write tasks to tasks.txt
    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            # Format task attributes and write to file
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_file.write(";".join(str_attrs) + "\n")

# Function to register a new user
def reg_user(username_password):
    # Prompt for new username and password
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please choose a different one.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    # Add new user to dictionary and user.txt
    username_password[new_username] = new_password
    with open("user.txt", "a") as user_file:
        user_file.write(f"\n{new_username};{new_password}")
    print("New user added.")

# Function to add a new task
def add_task(task_list):
    # Prompt for task details
    task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add new task to task list and save to file
    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    # Display all tasks
    for index, task in enumerate(task_list, start=1):
        print(f"Task {index}:")
        print(f"Title: {task['title']}")
        print(f"Assigned to: {task['username']}")
        print(f"Due Date: {task['due_date'].strftime('%Y-%m-%d')}")
        print(f"Description: {task['description']}")
        print(f"Completed: {'Yes' if task['completed'] else 'No'}")
        print()

#Function to a mark task as complete
def mark_task_complete(task_list, user_tasks, task_index):
    task_to_complete = user_tasks[task_index]  # Get the task from user_tasks
    # Find the corresponding task in task_list and mark it as complete
    for index, task in enumerate(task_list):
        if task == task_to_complete:
            task_list[index]['completed'] = True
            save_tasks(task_list)
            print("Task marked as complete.")
            return
    print("Error: Task not found in task list.")

# Function to edit a task
def edit_task(task_list, task_index):
    selected_task = task_list[user_tasks.index(selected_task)]
    
    print("Select which field you want to edit:")
    print("1. Username")
    print("2. Due Date")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        new_username = input("Enter new username: ")
        selected_task['username'] = new_username
    elif choice == "2":
        while True:
            try:
                new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
    else:
        print("Invalid choice.")
        return
    
    save_tasks(task_list)
    print("Task successfully edited.")

# Function to view tasks assigned to the current user
def view_mine(curr_user, task_list):
    # Display tasks assigned to the current user
    user_tasks = [task for task in task_list if task['username'] == curr_user]
    if not user_tasks:
        print("No tasks assigned to you.")
        return

    while True:
        for index, task in enumerate(user_tasks, start=1):
            print(f"Task {index}:")
            print(f"Title: {task['title']}")
            print(f"Due Date: {task['due_date'].strftime('%Y-%m-%d')}")
            print(f"Description: {task['description']}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print()
        
        user_input = input("Please select task or input -1\n")
        if user_input == '-1':
            break
        elif user_input.isdigit():
            task_index = int(user_input) - 1
            if 0 <= task_index < len(user_tasks):
                selected_task = user_tasks[task_index]
                if selected_task['completed']:
                    print("Task completed:", selected_task['completed'])
                else:
                    edit_choice = input("Do you want to mark the task as complete (enter 'complete') or edit the task (enter 'edit')?\n").lower()
                    if edit_choice == 'complete':
                        mark_task_complete(task_list, user_tasks, task_index)
                    elif edit_choice == 'edit':
                        edit_task(task_list, task_index)
                    else:
                        print("Invalid input. Please enter 'complete' or 'edit'.")
            else:
                print("Invalid input. Please enter 'complete' or 'edit',")
        else:
            print("Invalid input. Please enter a valid task number or -1 to return to the main menu.")
                                  

# Function to generate reports
def generate_reports(username_password, task_list):
    # Task Overview Report
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now())

    with open("task_overview.txt", "w") as report_file:
        report_file.write("Task Overview Report\n")
        report_file.write(f"Total number of tasks: {total_tasks}\n")
        report_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        report_file.write(f"Total number of uncompleted tasks: {incomplete_tasks}\n")
        report_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        if total_tasks != 0:
            report_file.write(f"Percentage of tasks that are incomplete: {incomplete_tasks / total_tasks * 100:.2f}%\n")
            report_file.write(f"Percentage of tasks that are overdue: {overdue_tasks / total_tasks * 100:.2f}%\n")
        else: 
            report_file.write("Percentage of tasks that are incomplete: 0.00%\n")
            report_file.write("Percentage of tasks that are overdue: 0.00%\n")

    # User Overview Report
    total_users = len(username_password)
    with open("user_overview.txt", "w") as report_file:
        report_file.write("User Overview Report\n")
        report_file.write(f"Total number of users: {total_users}\n")
        report_file.write(f"Total number of tasks: {total_tasks}\n")

        for username, password in username_password.items():
            user_tasks = sum(1 for task in task_list if task['username'] == username)
            completed_user_tasks = sum(1 for task in task_list if task['username'] == username and task['completed'])
            incomplete_user_tasks = user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in task_list if task['username'] == username and not task['completed'] and task['due_date'] < datetime.now())

            report_file.write(f"\n{username}:\n")
            report_file.write(f"Total number of tasks assigned: {user_tasks}\n")
            if user_tasks != 0:
                report_file.write(f"Percentage of total tasks assigned: {user_tasks / total_tasks * 100:.2f}%\n")
                report_file.write(f"Percentage of completed tasks: {completed_user_tasks / user_tasks * 100:.2f}%\n")
                report_file.write(f"Percentage of incomplete tasks: {incomplete_user_tasks / user_tasks * 100:.2f}%\n")
                report_file.write(f"Percentage of overdue tasks: {overdue_user_tasks / user_tasks * 100:.2f}%\n")
            else:
                report_file.write("Percentage of total tasks assigned: 0.00%\n")
                report_file.write("Percentage of completed tasks: 0.00%\n")
                report_file.write("Percentage of incomplete tasks: 0.00%\n")
                report_file.write("Percentage of overdue tasks: 0.00%\n")

# Function to display statistics
def display_statistics(curr_user, username_password, task_list):
    # Check if user is admin
    if curr_user != 'admin':
        print("You do not have permission to view statistics.")
        return

    # Generate reports
    generate_reports(username_password, task_list)

    # Display reports
    with open("task_overview.txt", "r") as report_file:
        print(report_file.read())

    with open("user_overview.txt", "r") as report_file:
        print(report_file.read())

# Main function
def main():
    task_list = load_tasks()
    username_password = {}

    # Read user credentials from user.txt
    with open("user.txt", 'r') as user_file:
        for user in user_file:
            username, password = user.strip().split(';')
            username_password[username] = password

    # Login
    while True:
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user in username_password and username_password[curr_user] == curr_pass:
            print("Login Successful!")
            break
        else:
            print("Incorrect username or password. Please try again.")
    
    # Main menu loop
    while True:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

        if menu == 'r':
            reg_user(username_password)

        elif menu == 'a':
            add_task(task_list)

        elif menu == 'va':
            view_all(task_list)

        elif menu == 'vm':
            view_mine(curr_user, task_list)

        elif menu == 'ds':
            display_statistics(curr_user, username_password, task_list)
            
        elif menu == 'gr':
            generate_reports(username_password, task_list)
            

        elif menu == 'e':
            print('Goodbye!!!')
            break

        else:
            print("Invalid option. Please try again.")

main()
