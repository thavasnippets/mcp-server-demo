import sqlite3
from typing import List, Tuple, Any, Optional


class Database:
    def __init__(self, db_path: str = 'employees.db'):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Execute a SELECT query and return results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_write(self, query: str, params: Tuple = ()) -> None:
        """Execute an INSERT, UPDATE, or DELETE query."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def get_employee_count(self) -> int:
        """Get total number of employees."""
        result = self.execute_query("SELECT COUNT(*) FROM employees")
        return result[0][0] if result else 0

    def get_department_count(self) -> int:
        """Get total number of departments."""
        result = self.execute_query("SELECT COUNT(*) FROM dept")
        return result[0][0] if result else 0

    def get_swipe_count(self) -> int:
        """Get total number of swipe records."""
        result = self.execute_query("SELECT COUNT(*) FROM swipe")
        return result[0][0] if result else 0

    def get_education_count(self) -> int:
        """Get total number of education records."""
        result = self.execute_query("SELECT COUNT(*) FROM education")
        return result[0][0] if result else 0


# Global database instance
db = Database()
