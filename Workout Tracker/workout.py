import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts)

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)

class WorkoutApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Workout Tracker")
        self.master.geometry("400x300")
        self.master.configure(bg="#f0f0f0")
        
        self.user = None
        
        # Main frame
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Profile setup frame
        self.profile_frame = ttk.LabelFrame(self.main_frame, text="Profile Setup", padding="10")
        self.profile_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.name_label = ttk.Label(self.profile_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.name_entry = ttk.Entry(self.profile_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        self.age_label = ttk.Label(self.profile_frame, text="Age:")
        self.age_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.age_entry = ttk.Entry(self.profile_frame, width=30)
        self.age_entry.grid(row=1, column=1, pady=5)
        
        self.weight_label = ttk.Label(self.profile_frame, text="Weight (kg):")
        self.weight_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.weight_entry = ttk.Entry(self.profile_frame, width=30)
        self.weight_entry.grid(row=2, column=1, pady=5)
        
        self.setup_button = ttk.Button(self.profile_frame, text="Set Up Profile", command=self.setup_profile)
        self.setup_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Workout frame
        self.workout_frame = ttk.LabelFrame(self.main_frame, text="Workout Actions", padding="10")
        self.workout_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.workout_button = ttk.Button(self.workout_frame, text="Add Workout", state=tk.DISABLED, command=self.add_workout)
        self.workout_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.view_button = ttk.Button(self.workout_frame, text="View Workouts", state=tk.DISABLED, command=self.view_workouts)
        self.view_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.save_button = ttk.Button(self.workout_frame, text="Save Data", state=tk.DISABLED, command=self.save_data)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.load_button = ttk.Button(self.workout_frame, text="Load Data", state=tk.DISABLED, command=self.load_data)
        self.load_button.grid(row=0, column=3, padx=5, pady=5)

    def setup_profile(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        weight = float(self.weight_entry.get())
        self.user = User(name, age, weight)

        self.profile_frame.grid_forget()
        
        self.workout_button.config(state=tk.NORMAL)
        self.view_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)

    def add_workout(self):
        date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
        exercise_type = simpledialog.askstring("Input", "Enter the exercise type:")
        duration = simpledialog.askinteger("Input", "Enter the duration (minutes):")
        calories_burned = simpledialog.askinteger("Input", "Enter the calories burned:")
        
        if date and exercise_type and duration and calories_burned:
            workout = Workout(date, exercise_type, duration, calories_burned)
            self.user.add_workout(workout)
            messagebox.showinfo("Success", "Workout added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def view_workouts(self):
        workouts = self.user.view_workouts()
        if workouts:
            messagebox.showinfo("Workouts", workouts)
        else:
            messagebox.showinfo("No Workouts", "You haven't added any workouts yet.")

    def save_data(self):
        filename = simpledialog.askstring("Input", "Enter the filename to save data:")
        if filename:
            self.user.save_data(filename)
            messagebox.showinfo("Success", "Data saved successfully!")
        else:
            messagebox.showerror("Error", "Filename cannot be empty.")

    def load_data(self):
        filename = simpledialog.askstring("Input", "Enter the filename to load data:")
        if filename:
            try:
                self.user.load_data(filename)
                messagebox.showinfo("Success", "Data loaded successfully!")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
        else:
            messagebox.showerror("Error", "Filename cannot be empty.")

def main():
    root = tk.Tk()
    app = WorkoutApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()