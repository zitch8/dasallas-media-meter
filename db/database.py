from abc import ABC, abstractmethod
from typing import List, Dict, Any

from models.task import Task


class DatabaseInterface(ABC):
    """
    Abstraction base class
    """

    @abstractmethod
    def connect(self) -> None:
        """For Mongo database connection"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """For Mongo database disconnection"""
        pass

    @abstractmethod
    def add_task(self, task: Task) -> bool:
        """Add a task into the database"""
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the database"""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        """Retrieve a single task by ID from the database"""
        pass
    
    @abstractmethod
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update a task in the database"""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the database"""
        pass