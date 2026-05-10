from mcp.server.fastmcp import FastMCP
from db import db


def register_education_tools(mcp: FastMCP):
    """Register all education-related tools."""

    @mcp.tool()
    def get_employee_education(employee_id: int) -> str:
        """Get education details for a specific employee."""
        rows = db.execute_query('''SELECT e.degree, e.institution, e.graduation_year, e.gpa, emp.name
                                   FROM education e
                                   JOIN employees emp ON e.employee_id = emp.id
                                   WHERE e.employee_id = ?
                                   ORDER BY e.graduation_year DESC''', (employee_id,))
        if not rows:
            return f"No education records found for employee ID {employee_id}"

        employee_name = rows[0][4] if rows else "Unknown"
        result = f"Education Details for {employee_name} (ID: {employee_id}):\n"
        for row in rows:
            gpa = f"{row[3]:.1f}" if row[3] else "N/A"
            result += f"Degree: {row[0]}, Institution: {row[1]}, Year: {row[2]}, GPA: {gpa}\n"
        return result
