import sys
from config.config import Config
from db.database_manager import DatabaseManager

from manager.task_manager import TaskManager
from manager.task_cli import TaskCLI

def main():
    try:
        
        db_config = Config.get_database_config()
        
        database = DatabaseManager(**db_config)
        
        # Connect to database
        database.connect()
        
        # Initialize task manager
        task_manager = TaskManager(database)
        
        # Initialize CLI
        cli = TaskCLI(task_manager)
        
        # Run application
        cli.run()
        
        # Cleanup
        database.disconnect()
        
        return 0
    
    except Exception as e:
        print(f"\nUnexpected Error: {e}")


if __name__ == "__main__":
    sys.exit(main())