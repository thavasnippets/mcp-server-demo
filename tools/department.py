from mcp.server.fastmcp import FastMCP
from db import db


def register_department_tools(mcp: FastMCP):
    """Register all department-related tools."""

    @mcp.tool()
    def get_all_departments() -> str:
        """Get all departments from the database."""
        rows = db.execute_query('''SELECT d.id, d.name, e.name as manager_name, d.location, d.budget
                                   FROM dept d
                                   LEFT JOIN employees e ON d.manager_id = e.id''')
        if not rows:
            return "No departments found."

        result = "All Departments:\n"
        for row in rows:
            manager = row[2] if row[2] else "No manager assigned"
            result += f"ID: {row[0]}, Name: {row[1]}, Manager: {manager}, Location: {row[3]}, Budget: ${row[4]:,.2f}\n"
        return result

    @mcp.tool()
    def get_department_by_id(dept_id: int) -> str:
        """Get department information by ID."""
        rows = db.execute_query('''SELECT d.id, d.name, e.name as manager_name, d.location, d.budget
                                   FROM dept d
                                   LEFT JOIN employees e ON d.manager_id = e.id
                                   WHERE d.id = ?''', (dept_id,))
        if not rows:
            return f"No department found with ID {dept_id}"

        row = rows[0]
        manager = row[2] if row[2] else "No manager assigned"
        return f"ID: {row[0]}, Name: {row[1]}, Manager: {manager}, Location: {row[3]}, Budget: ${row[4]:,.2f}"
