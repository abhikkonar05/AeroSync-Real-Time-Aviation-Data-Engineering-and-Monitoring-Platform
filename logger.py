from database.connection import engine
from sqlalchemy import text

def log_step(step, status):
    # Use a transaction context so the insert is committed properly
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO pipeline_logs (step, status) VALUES (:step, :status)"),
            {"step": step, "status": status}
        )