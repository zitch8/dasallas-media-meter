from typing import Any, Dict, List

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from db.database import DatabaseInterface
from models.task import Task

class DatabaseManager(DatabaseInterface):
    """MongoDB implementation for storage"""

    def __init__(self, 
                 uri: str, 
                 db_name: str,
                 collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)

            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]

            print(f"Connected to MongoDB: {self.db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    def add_task(self, task: Task) -> bool:
        try:
            task_dict = task.to_dict()
            self.collection.insert_one(task_dict)
            return True
        except PyMongoError as e:
            print(f"Error adding task: {e}")
            return False
        
    def get_task(self, task_id):
        try:
            doc = self.collection.find_one({"_task_id": task_id})
            if doc:
                doc.pop('_id', None)
                return Task.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error retrieving task: {e}")
            return None

    def get_all_tasks(self) -> List[Task]:
        try:
            cursor = self.collection.find({})
            tasks = []
            for doc in cursor:
                doc.pop('_id', None)
                tasks.append(Task.from_dict(doc))
            return tasks
        except PyMongoError as e:
            print(f"Error retrieving tasks: {e}")
            return []
        
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        try:
            result = self.collection.update_one(
                {"_task_id": task_id},
                {"$set": updates}
            )
            return result.modified_count >= 1
        except PyMongoError as e:
            print(f"Error updating task: {e}")
            return False
        
    def delete_task(self, task_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_task_id": task_id})
            return result.deleted_count >= 1
        except PyMongoError as e:
            print(f"Error deleting task: {e}")
            return False