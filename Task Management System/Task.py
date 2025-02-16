import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json


class Task:
    def __init__(self, title, description, start_date, end_date):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        task = cls(task_dict['title'], task_dict['description'], task_dict['start_date'], task_dict['end_date'])
        task.completed = task_dict['completed']
        return task

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Title: {self.title}\nDescription: {self.description}\nStart Date: {self.start_date}\nEnd Date: {self.end_date}\nStatus: {status}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, start_date, end_date):
        task = Task(title, description, start_date, end_date)
        self.tasks.append(task)
        self.update_task_list()

    def list_tasks(self):
        return [str(task) for task in self.tasks]

    def mark_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_completed()
            self.update_task_list()

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.update_task_list()

    def save_tasks(self, filename):
        with open(filename, 'w') as file:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, file)

    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as file:
                tasks_dict = json.load(file)
                self.tasks = [Task.from_dict(task) for task in tasks_dict]
        except FileNotFoundError:
            print("No saved tasks found.")

    def update_task_list(self):
        task_list_str = "\n\n".join(self.list_tasks())
        task_list_display.config(state=tk.NORMAL)
        task_list_display.delete(1.0, tk.END)  # Clear the text box
        task_list_display.insert(tk.END, task_list_str)
        task_list_display.config(state=tk.DISABLED)  # Make it read-only


def add_task_gui():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Validate inputs
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        return

    task_manager.add_task(title, description, start_date, end_date)
    clear_inputs()


def clear_inputs():
    title_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)
    start_date_entry.delete(0, tk.END)
    end_date_entry.delete(0, tk.END)


def mark_completed_gui():
    task_index = int(task_index_entry.get()) - 1
    if 0 <= task_index < len(task_manager.tasks):
        task_manager.mark_task_completed(task_index)
        messagebox.showinfo("Success", "Task marked as completed.")
    else:
        messagebox.showerror("Error", "Invalid task index.")


def delete_task_gui():
    task_index = int(task_index_entry.get()) - 1
    if 0 <= task_index < len(task_manager.tasks):
        task_manager.delete_task(task_index)
        messagebox.showinfo("Success", "Task deleted successfully.")
    else:
        messagebox.showerror("Error", "Invalid task index.")


def save_tasks_gui():
    task_manager.save_tasks("tasks.json")
    messagebox.showinfo("Success", "Tasks saved successfully.")


def load_tasks_gui():
    task_manager.load_tasks("tasks.json")
    task_manager.update_task_list()


# Create main application window
root = tk.Tk()
root.title("Task Management System")
root.geometry("750x700")
root.config(bg="#ffebcd")  # Light orange background for the whole window

# Initialize TaskManager
task_manager = TaskManager()
task_manager.load_tasks("tasks.json")

# Create Heading with unique font style, size, and color
heading_label = tk.Label(root, text="TASK MANAGEMENT SYSTEM", bg="#ffebcd", font=("Arial", 24, "bold"), fg="#8e44ad", pady=20)
heading_label.pack()

# Create colorful input labels and entry widgets
font_style = ("Arial", 12)

title_label = tk.Label(root, text="Task Title:", bg="#f39c12", font=font_style, fg="white")
title_label.pack(pady=10)
title_entry = tk.Entry(root, width=50, font=font_style, bd=2, relief="solid", bg="#e67e22")
title_entry.pack(pady=5)

description_label = tk.Label(root, text="Task Description:", bg="#f39c12", font=font_style, fg="white")
description_label.pack(pady=10)
description_entry = tk.Text(root, height=5, width=50, font=font_style, bd=2, relief="solid", bg="#e67e22")
description_entry.pack(pady=5)

start_date_label = tk.Label(root, text="Start Date (YYYY-MM-DD):", bg="#f39c12", font=font_style, fg="white")
start_date_label.pack(pady=10)
start_date_entry = tk.Entry(root, width=50, font=font_style, bd=2, relief="solid", bg="#e67e22")
start_date_entry.pack(pady=5)

end_date_label = tk.Label(root, text="End Date (YYYY-MM-DD):", bg="#f39c12", font=font_style, fg="white")
end_date_label.pack(pady=10)
end_date_entry = tk.Entry(root, width=50, font=font_style, bd=2, relief="solid", bg="#e67e22")
end_date_entry.pack(pady=5)

task_index_label = tk.Label(root, text="Enter Task Index:", bg="#f39c12", font=font_style, fg="white")
task_index_label.pack(pady=10)
task_index_entry = tk.Entry(root, width=50, font=font_style, bd=2, relief="solid", bg="#e67e22")
task_index_entry.pack(pady=5)

# Create colorful buttons with hover effects
def on_hover(event, button, color):
    button.config(bg=color)

def on_leave(event, button, color):
    button.config(bg=color)

# Button Styles
button_style = {
    "font": font_style,
    "fg": "white",
    "bd": 2,
    "relief": "solid",
    "width": 20
}

add_task_button = tk.Button(root, text="Add Task", **button_style, command=add_task_gui, bg="#1abc9c")
add_task_button.pack(pady=10)
add_task_button.bind("<Enter>", lambda event, button=add_task_button: on_hover(event, button, "#16a085"))
add_task_button.bind("<Leave>", lambda event, button=add_task_button: on_leave(event, button, "#1abc9c"))

mark_completed_button = tk.Button(root, text="Mark as Completed", **button_style, command=mark_completed_gui, bg="#3498db")
mark_completed_button.pack(pady=10)
mark_completed_button.bind("<Enter>", lambda event, button=mark_completed_button: on_hover(event, button, "#2980b9"))
mark_completed_button.bind("<Leave>", lambda event, button=mark_completed_button: on_leave(event, button, "#3498db"))

delete_task_button = tk.Button(root, text="Delete Task", **button_style, command=delete_task_gui, bg="#e74c3c")
delete_task_button.pack(pady=10)
delete_task_button.bind("<Enter>", lambda event, button=delete_task_button: on_hover(event, button, "#c0392b"))
delete_task_button.bind("<Leave>", lambda event, button=delete_task_button: on_leave(event, button, "#e74c3c"))

save_tasks_button = tk.Button(root, text="Save Tasks", **button_style, command=save_tasks_gui, bg="#9b59b6")
save_tasks_button.pack(pady=10)
save_tasks_button.bind("<Enter>", lambda event, button=save_tasks_button: on_hover(event, button, "#8e44ad"))
save_tasks_button.bind("<Leave>", lambda event, button=save_tasks_button: on_leave(event, button, "#9b59b6"))

load_tasks_button = tk.Button(root, text="Load Tasks", **button_style, command=load_tasks_gui, bg="#f39c12")
load_tasks_button.pack(pady=10)
load_tasks_button.bind("<Enter>", lambda event, button=load_tasks_button: on_hover(event, button, "#e67e22"))
load_tasks_button.bind("<Leave>", lambda event, button=load_tasks_button: on_leave(event, button, "#f39c12"))

# Create a colorful, scrollable task list display
task_list_display = tk.Text(root, height=10, width=60, font=font_style, wrap=tk.WORD, state=tk.DISABLED, bd=2, relief="solid", bg="#f1c40f")
task_list_display.pack(pady=20)

# Start the GUI main loop
root.mainloop()
