from typing import List, Optional
from datetime import datetime

from models.task import Task, Priority, Status
from db.database import DatabaseInterface

class TaskManager:
    """
    Manages tasks using a database interface
    """

    def __init__(self, db_interface: DatabaseInterface):
        self.db_interface = db_interface
        self.db_interface.connect()

    def __del__(self):
        self.db_interface.disconnect()

    def get_all_tasks(self) -> List[Task]:
        return self.db_interface.get_all_tasks()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.get_all_tasks():
            if task.task_id == task_id:
                return task
            
        return None

    def add_task(self, 
                title: str, 
                description: str, 
                due_date: datetime, 
                priority: Priority) -> Optional[Task]:

        try:
            task = Task(title=title,
                description=description,
                due_date=due_date,
                priority=priority)
            return task
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
        
    def list_tasks(self, 
                   filter_status: Optional[Status] = None,
                   filter_priority: Optional[Priority] = None,
                   filter_due_before: Optional[datetime] = None) -> List[Task]:
        
        tasks = self.db_interface.get_all_tasks()
        filtered_tasks = self._apply_filters(
            tasks, 
            filter_status, 
            filter_priority, 
            filter_due_before
        )
        
        return filtered_tasks
    
    def _apply_filters(self, tasks: List[Task],
                      status: Optional[Status],
                      priority: Optional[Priority],
                      due_before: Optional[datetime]) -> List[Task]:
        """
        Apply filters to task list.
        """
        filtered = tasks
        
        if status:
            filtered = [t for t in filtered if t.status == status]
        
        if priority:
            filtered = [t for t in filtered if t.priority == priority]
        
        if due_before:
            filtered = [t for t in filtered if t.due_date <= due_before]
        
        return filtered

    def update_task(self, task_id: str, **updates) -> bool:
        try:
            task = self.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return False
            
            db_updates = {}
            if 'title' in updates:
                db_updates['title'] = updates['title']
            
            if 'description' in updates:
                    task.description = updates['description']
                    db_updates['description'] = updates['description']
                
            if 'due_date' in updates:
                task.due_date = updates['due_date']
                db_updates['due_date'] = updates['due_date'].isoformat()
            
            if 'priority' in updates:
                task.priority = updates['priority']
                db_updates['priority'] = updates['priority'].value
            
            if 'status' in updates:
                task.status = updates['status']
                db_updates['status'] = updates['status'].value
            
            return self.db_interface.update_task(task_id, db_updates)
        
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id: str) -> bool:
        return self.db_interface.delete_task(task_id)
    
    def mark_completed(self, task_id: str) -> bool:
        return self.update_task(task_id, status=Status.COMPLETED)