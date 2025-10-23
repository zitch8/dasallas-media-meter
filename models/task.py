import datetime
from typing import Optional

class Priority:
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

class Status:
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

class Task:
    """
    Single task representation
    """

    def __init__(self, 
                 title: str, 
                 description: str, 
                 due_date: datetime, 
                 priority: Priority,
                 creation_timestamp: datetime,
                 status: Status = Status.PENDING):
        
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority
        self._status = status
        self._creation_timestamp = creation_timestamp

    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def due_date(self) -> datetime:
        return self._due_date
    
    @property
    def priority(self) -> Priority:
        return self._priority
    
    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def creation_timestamp(self) -> datetime:
        return self._creation_timestamp
    
    # @title.setter
    # def title(self, value: str):
    #     if not value or not value.strip():
    #         raise ValueError("Title cannot be empty.")
    #     self._title = value

    # @description.setter
    # def description(self, value: str):
    #     self._description = value

    def mark_completed(self):
        self._status = Status.COMPLETED
    
    def to_dict(self) -> dict:
        """
        Serialize the task to a dictionary
        """
        return {
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date.isoformat(),
            "priority": self._priority,
            "status": self._status,
            "creation_timestamp": self._creation_timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Deserialize a task from a dictionary
        """
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=datetime.datetime.fromisoformat(data["due_date"]),
            priority=data["priority"],
            status=data.get("status", Status.PENDING),
            creation_timestamp=datetime.datetime.fromisoformat(data["creation_timestamp"])
        )