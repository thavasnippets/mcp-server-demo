from mcp.server.fastmcp import FastMCP
from db import db


def register_swipe_tools(mcp: FastMCP):
    """Register all swipe/attendance-related tools."""

    @mcp.tool()
    def get_employee_swipes(employee_id: int) -> str:
        """Get all swipe in/out records for a specific employee."""
        rows = db.execute_query('''SELECT s.swipe_time, s.swipe_type, s.date, e.name
                                   FROM swipe s
                                   JOIN employees e ON s.employee_id = e.id
                                   WHERE s.employee_id = ?
                                   ORDER BY s.date DESC, s.swipe_time DESC''', (employee_id,))
        if not rows:
            return f"No swipe records found for employee ID {employee_id}"

        employee_name = rows[0][3] if rows else "Unknown"
        result = f"Swipe Records for {employee_name} (ID: {employee_id}):\n"
        for row in rows:
            result += f"Date: {row[2]}, Time: {row[0]}, Type: {row[1]}\n"
        return result

    @mcp.tool()
    def get_attendance_summary(date: str) -> str:
        """Get attendance summary for a specific date."""
        rows = db.execute_query('''SELECT e.name,
                                          MIN(CASE WHEN s.swipe_type = 'in' THEN s.swipe_time END) as check_in,
                                          MAX(CASE WHEN s.swipe_type = 'out' THEN s.swipe_time END) as check_out
                                   FROM employees e
                                   LEFT JOIN swipe s ON e.id = s.employee_id AND s.date = ?
                                   GROUP BY e.id, e.name
                                   ORDER BY e.name''', (date,))
        if not rows:
            return f"No attendance records found for date {date}"

        result = f"Attendance Summary for {date}:\n"
        for row in rows:
            check_in = row[1] if row[1] else "No check-in"
            check_out = row[2] if row[2] else "No check-out"
            result += f"Employee: {row[0]}, Check-in: {check_in}, Check-out: {check_out}\n"
        return result
