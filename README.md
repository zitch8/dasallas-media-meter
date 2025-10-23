# dasallas-media-meter

## Installation

1. Create virtual environment:
```
python -m venv .venv
source venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

For Python Version 3.11 or Later
```
python -m pip install "pymongo[srv]==3.11"
```

## Configuration

Edit `config.py` or set .env variables:

```
MONGO_URI="mongodb://localhost:27017/"
MONGO_DB="taskmanagement"
MONGO_COLLECTION="tasks"
```

## Usage

Run the application:
```
python main.py
```

### Main Menu Options

1. **Add New Task** - Create a new task with title, description, due date, and priority
2. **List All Tasks** - View all tasks with optional filtering by status, priority, or due date
3. **Update Task** - Modify task details
4. **Mark Task as Completed** - Change task status to completed
5. **Delete Task** - Remove a task from the system
6. **Exit** - Close the application

## Project Structure
```
dasallas-meida-meter/
│
├── main.py                  # Entry point
├── models/
│   └── task.py              # Task class and other model classes
├── manager/
│   └── task_manager.py      # Handles CRUD logic
│   └── task_cli.py          # Handles command-line interface
├── db/
│   └── database.py          # Database interface
│   └── database_manager.py  # Handles MongoDB implementation
├── config/
│   └── config.py            # MongoDB connection details
├── requirements.txt
└── README.md
```

