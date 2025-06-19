import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
        
    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.todos, file, indent=4)
    
    def add_todo(self, task, priority="medium"):
        """Add a new todo item"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "priority": priority.lower(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"Added: {task}")
    
    def list_todos(self, show_completed=False):
        """List all todos, optionally including completed ones"""
        print("\nTo-Do List:")
        print("-" * 30)
        for todo in self.todos:
            if not todo["completed"] or show_completed:
                status = "✓" if todo["completed"] else " "
                print(f"{todo['id']}. [{status}] {todo['task']} (Priority: {todo['priority']})")
        print("-" * 30)
    
    def complete_todo(self, todo_id):
        """Mark a todo as completed"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todos()
                print(f"Completed: {todo['task']}")
                return
        print(f"Todo with ID {todo_id} not found.")
    
    def delete_todo(self, todo_id):
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                deleted_task = self.todos.pop(i)["task"]
                self.save_todos()
                # Update IDs of remaining todos
                for j, t in enumerate(self.todos[i:], start=i):
                    t["id"] = j + 1
                self.save_todos()
                print(f"Deleted: {deleted_task}")
                return
        print(f"Todo with ID {todo_id} not found.")
    
    def clear_completed(self):
        """Remove all completed todos"""
        initial_count = len(self.todos)
        self.todos = [todo for todo in self.todos if not todo["completed"]]
        if len(self.todos) < initial_count:
            # Update IDs after clearing
            for i, todo in enumerate(self.todos, start=1):
                todo["id"] = i
            self.save_todos()
            print(f"Removed {initial_count - len(self.todos)} completed tasks.")
        else:
            print("No completed tasks to remove.")

def display_menu():
    """Display the main menu"""
    print("\nTo-Do List Application")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Clear Completed Tasks")
    print("6. Exit")

def get_priority():
    """Get valid priority from user"""
    while True:
        priority = input("Enter priority (high/medium/low): ").lower()
        if priority in ["high", "medium", "low"]:
            return priority
        print("Invalid priority. Please enter high, medium, or low.")

def main():
    todo_list = TodoList()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            task = input("Enter task: ")
            priority = get_priority()
            todo_list.add_todo(task, priority)
        elif choice == "2":
            show_completed = input("Show completed tasks? (y/n): ").lower() == "y"
            todo_list.list_todos(show_completed)
        elif choice == "3":
            try:
                todo_id = int(input("Enter task ID to complete: "))
                todo_list.complete_todo(todo_id)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            try:
                todo_id = int(input("Enter task ID to delete: "))
                todo_list.delete_todo(todo_id)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            todo_list.clear_completed()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()