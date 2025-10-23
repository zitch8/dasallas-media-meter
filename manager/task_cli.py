import sys
from datetime import datetime, timedelta

from manager.task_manager import TaskManager
from models.task import Task, Priority, Status

class TaskCLI:
    """Command-line interface for task management"""

    def __init__(self, task_manager: TaskManager):
        """
        Initialize CLI with task manager.
        
        Args:
            task_manager: TaskManager instance
        """
        self.task_manager = task_manager
        self.running = True

    def run(self):
        """Main CLI loop."""
        self.entry()
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nEnter your choice: ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")

    def entry(self):
        """Entry message"""

        print("TASK MANAGEMENT SYSTEM")
        print("="*50)
    
    def display_menu(self):
        """Display main menu"""

        print("\n" + "-"*50)
        print("MAIN MENU")
        print("-"*50)
        print("1. Add New Task")
        print("2. List All Tasks")
        print("3. Update Task")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. Exit")
        print("-"*50)

    def handle_choice(self, choice: str):
        """Handle user menu choice"""

        actions = {
            '1': self.add_task,
            '2': self.list_tasks,
            '3': self.update_task,
            '4': self.mark_completed,
            '5': self.delete_task,
            '6': self.exit_app
        }
        
        action = actions.get(choice)
        if action:
            action()
        else:
            print("\nInvalid choice. Please try again.")

    def add_task(self):
        """Add a new task."""
        print("\n" + "="*50)
        print("ADD NEW TASK")
        print("="*50)
        
        try:
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty")
                return
            
            description = input("Description: ").strip()
            
            # Get due date
            due_date_str = input("Due Date (YYYY-MM-DD) or days from now (e.g., '3'): ").strip()
            due_date = self._parse_date(due_date_str)
            
            # Get priority
            print("Priority: 1=Low, 2=Medium, 3=High")
            priority_choice = input("Enter priority: ").strip()
            priority = self._parse_priority(priority_choice)
            
            # Create task
            task = self.task_manager.add_task(title, description, due_date, priority)
            
            if task:
                print(f"\nTask created successfully!")
                print(f"Task ID: {task.task_id}")
            else:
                print("\nFailed to create task")
                
        except ValueError as e:
            print(f"\nInvalid input: {e}")
        except Exception as e:
            print(f"\nError: {e}")

    def list_tasks(self):
        """List all tasks with optional filtering"""
        print("\n" + "="*50)
        print("LIST TASKS")
        print("="*50)
        
        # Ask for filters
        print("\nFilters (press Enter to skip):")
        
        filter_status = None
        status_input = input("Status (1=Pending, 2=In Progress, 3=Completed): ").strip()
        if status_input:
            filter_status = self._parse_status(status_input)
        
        filter_priority = None
        priority_input = input("Priority (1=Low, 2=Medium, 3=High): ").strip()
        if priority_input:
            filter_priority = self._parse_priority(priority_input)
        
        # Get sort option
        print("\nSort by: 1=Created, 2=Due Date, 3=Priority, 4=Title")
        sort_choice = input("Sort option (default=1): ").strip() or '1'
        sort_map = {'1': 'created_at', '2': 'due_date', '3': 'priority', '4': 'title'}
        sort_by = sort_map.get(sort_choice, 'created_at')
        
        # Get tasks
        tasks = self.task_manager.list_tasks(
            filter_status=filter_status,
            filter_priority=filter_priority,
            sort_by=sort_by
        )
        
        if not tasks:
            print("\nNo tasks found.")
            return
        
        # Display tasks
        print(f"\nFound {len(tasks)} task(s):")
        print("-"*50)
        
        for i, task in enumerate(tasks, 1):
            self._print_task_summary(i, task)

    def update_task(self):
        """Update a task"""
        task_id = input("\nEnter Task ID: ").strip()
        
        task = self.task_manager.get_task(task_id)
        if not task:
            print("\nTask not found")
            return
        
        print("\nCurrent task details:")
        self._print_task_details(task)
        
        print("\nEnter new values (press Enter to skip):")
        
        updates = {}
        
        # Update depending on values provided

        title = input(f"Title [{task.title}]: ").strip()
        if title:
            updates['title'] = title
        
        description = input(f"Description [{task.description}]: ").strip()
        if description:
            updates['description'] = description
        
        due_date_str = input(f"Due Date (YYYY-MM-DD) [{task.due_date.strftime('%Y-%m-%d')}]: ").strip()
        if due_date_str:
            updates['due_date'] = self._parse_date(due_date_str)
        
        priority_input = input(f"Priority (1=Low, 2=Medium, 3=High) [{task.priority.value}]: ").strip()
        if priority_input:
            updates['priority'] = self._parse_priority(priority_input)
        
        status_input = input(f"Status (1=Pending, 2=In Progress, 3=Completed) [{task.status.value}]: ").strip()
        if status_input:
            updates['status'] = self._parse_status(status_input)
        
        if updates:
            if self.task_manager.update_task(task_id, **updates):
                print("\nTask updated successfully")
            else:
                print("\nFailed to update task")
        else:
            print("\nNo changes made")
    
    def mark_completed(self):
        """Mark a task as completed."""
        task_id = input("\nEnter Task ID: ").strip()
        
        if self.task_manager.mark_completed(task_id):
            print("\nTask marked as completed")
        else:
            print("\nFailed to mark task as completed")
    
    def delete_task(self):
        """Delete a task."""
        task_id = input("\nEnter Task ID: ").strip()
        
        task = self.task_manager.get_task(task_id)
        if not task:
            print("\nTask not found")
            return
        
        print("\nTask to delete:")
        self._print_task_details(task)
        
        confirm = input("\nAre you sure you want to delete this task? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if self.task_manager.delete_task(task_id):
                print("\nTask deleted successfully")
            else:
                print("\nFailed to delete task")
        else:
            print("\nDeletion cancelled")

    def exit_app(self):
        """Exit the application."""
        print("\nThank you for using Task Management System!")
        self.running = False
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string."""
        # Try parsing as number of days
        try:
            days = int(date_str)
            return datetime.now() + timedelta(days=days)
        except ValueError:
            pass
        
        # Try parsing as date
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or number of days")
    
    def _parse_priority(self, priority_str: str) -> Priority:
        """Parse priority string."""
        priority_map = {'1': Priority.LOW, '2': Priority.MEDIUM, '3': Priority.HIGH}
        priority = priority_map.get(priority_str)
        if not priority:
            raise ValueError("Invalid priority. Use 1, 2, or 3")
        return priority
    
    def _parse_status(self, status_str: str) -> Status:
        """Parse status string."""
        status_map = {'1': Status.PENDING, '2': Status.IN_PROGRESS, '3': Status.COMPLETED}
        status = status_map.get(status_str)
        if not status:
            raise ValueError("Invalid status. Use 1, 2, or 3")
        return status

    def _print_task_summary(self, index: int, task: Task):
        """Print task summary."""
        status_icon = "Complete" if task.status == Status.COMPLETED else "Incomplete"
        priority_icon = task.priority.value
        
        print(f"{index}. {status_icon} [{priority_icon}] {task.title[:40]}")
        print(f"   ID: {task.task_id[:16]}... | Due: {task.due_date.strftime('%Y-%m-%d')} | Status: {task.status.value}")
        print()
    
    def _print_task_details(self, task: Task):
        """Print detailed task information."""
        print("\n" + "="*50)
        print("TASK DETAILS")
        print("="*50)
        print(f"Task ID: {task.task_id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"Priority: {task.priority.value}")
        print(f"Status: {task.status.value}")
        print(f"Created: {task.creation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)