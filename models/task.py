import datetime
from typing import Optional
from enum import Enum

class Priority(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

class Status(Enum):
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
                 task_id: Optional[str] = None,
                 status: Status = Status.PENDING,
                 creation_timestamp: datetime = None):
        
        self._task_id = task_id or self._generate_id()
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority
        self._status = status
        self._creation_timestamp = creation_timestamp

    @staticmethod
    def _generate_id() -> str:
        """
        Generate a unique task ID using datetime
        """
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    # Getters
    @property
    def task_id(self) -> str:
        return self._task_id
    
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
    
    # Setter with validation
    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else ""
    
    @due_date.setter
    def due_date(self, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("Due date must be a datetime object")
        self._due_date = value
    
    @priority.setter
    def priority(self, value: Priority):
        if not isinstance(value, Priority):
            raise ValueError("Priority must be a Priority enum value")
        self._priority = value
    
    @status.setter
    def status(self, value: Status):
        if not isinstance(value, Status):
            raise ValueError("Status must be a Status enum value")
        self._status = value

    def mark_completed(self):
        self._status = Status.COMPLETED
    
    def to_dict(self) -> dict:
        """
        Serialize the task to a dictionary
        """
        return {
            "task_id": self._task_id,
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