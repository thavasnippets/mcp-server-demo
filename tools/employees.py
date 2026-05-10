from mcp.server.fastmcp import FastMCP
from db import db


def register_employee_tools(mcp: FastMCP):
    """Register all employee-related tools."""

    @mcp.tool()
    def get_all_employees() -> str:
        """Get all employees from the database."""
        rows = db.execute_query('SELECT * FROM employees')
        if not rows:
            return "No employees found."

        result = "All Employees:\n"
        for row in rows:
            result += f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Salary: ${row[3]:,.2f}, Hire Date: {row[4]}\n"
        return result

    @mcp.tool()
    def get_employee_by_id(employee_id: int) -> str:
        """Get employee information by ID."""
        rows = db.execute_query(
            'SELECT * FROM employees WHERE id = ?', (employee_id,))
        if not rows:
            return f"No employee found with ID {employee_id}"

        row = rows[0]
        return f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Salary: ${row[3]:,.2f}, Hire Date: {row[4]}"

    @mcp.tool()
    def get_employees_by_department(department: str) -> str:
        """Get all employees in a specific department."""
        rows = db.execute_query(
            'SELECT * FROM employees WHERE department = ?', (department,))
        if not rows:
            return f"No employees found in department '{department}'"

        result = f"Employees in {department}:\n"
        for row in rows:
            result += f"ID: {row[0]}, Name: {row[1]}, Salary: ${row[3]:,.2f}, Hire Date: {row[4]}\n"
        return result

    @mcp.tool()
    def get_department_summary() -> str:
        """Get a summary of employees by department."""
        rows = db.execute_query(
            'SELECT department, COUNT(*), AVG(salary) FROM employees GROUP BY department')
        if not rows:
            return "No department data found."

        result = "Department Summary:\n"
        for row in rows:
            result += f"Department: {row[0]}, Count: {row[1]}, Average Salary: ${row[2]:,.2f}\n"
        return result
