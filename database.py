"""
Database module for Myco Logger application.
Handles SQLite database operations for mushroom cultivation experiments.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd


DATABASE_PATH = Path(__file__).parent / "data" / "mushroom_tracker.db"


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """
    Initialize the database and create tables if they don't exist.
    Returns connection for immediate use if needed.
    """
    # Ensure data directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        cursor = conn.cursor()

        # Create experiments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                substrate_type TEXT NOT NULL,
                substrate_details TEXT,
                spawn_ratio REAL,
                substrate_weight_kg REAL,
                container_type TEXT,
                inoculation_date DATE NOT NULL,
                colonization_date DATE,
                first_pin_date DATE,
                status TEXT NOT NULL,
                contamination_type TEXT,
                contamination_notes TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    return True


def add_experiment(**kwargs) -> int:
    """
    Add a new experiment to the database.

    Args:
        **kwargs: Experiment fields (experiment_name, substrate_type, etc.)

    Returns:
        int: ID of the newly created experiment
    """
    required_fields = ['experiment_name', 'substrate_type', 'inoculation_date', 'status']

    # Validate required fields
    for field in required_fields:
        if field not in kwargs:
            raise ValueError(f"Missing required field: {field}")

    # Build dynamic SQL query
    fields = list(kwargs.keys())
    placeholders = ', '.join(['?' for _ in fields])
    field_names = ', '.join(fields)
    values = [kwargs[field] for field in fields]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO experiments ({field_names}) VALUES ({placeholders})",
            values
        )
        experiment_id = cursor.lastrowid
        conn.commit()

    return experiment_id


def get_all_experiments() -> pd.DataFrame:
    """
    Retrieve all experiments as a pandas DataFrame.

    Returns:
        pd.DataFrame: All experiments
    """
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM experiments ORDER BY created_at DESC", conn)

    return df


def get_experiment_by_id(experiment_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single experiment by its ID.

    Args:
        experiment_id: The experiment ID

    Returns:
        dict: Experiment data or None if not found
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None


def update_experiment(experiment_id: int, **kwargs) -> bool:
    """
    Update an experiment's fields.

    Args:
        experiment_id: The experiment ID
        **kwargs: Fields to update

    Returns:
        bool: True if successful
    """
    if not kwargs:
        return False

    # Build dynamic UPDATE query
    set_clause = ', '.join([f"{field} = ?" for field in kwargs.keys()])
    values = list(kwargs.values()) + [experiment_id]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE experiments SET {set_clause} WHERE id = ?",
            values
        )
        conn.commit()

        return cursor.rowcount > 0


def delete_experiment(experiment_id: int) -> bool:
    """
    Delete an experiment by its ID.

    Args:
        experiment_id: The experiment ID

    Returns:
        bool: True if successful
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM experiments WHERE id = ?", (experiment_id,))
        conn.commit()

        return cursor.rowcount > 0


def get_experiments_by_status(status: str) -> pd.DataFrame:
    """
    Filter experiments by status.

    Args:
        status: The status to filter by

    Returns:
        pd.DataFrame: Filtered experiments
    """
    with get_connection() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM experiments WHERE status = ? ORDER BY created_at DESC",
            conn,
            params=(status,)
        )

    return df


def get_stats() -> Dict[str, Any]:
    """
    Get summary statistics about experiments.

    Returns:
        dict: Statistics including total_count, active_count,
              contaminated_count, success_rate
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Total count
        cursor.execute("SELECT COUNT(*) FROM experiments")
        total_count = cursor.fetchone()[0]

        # Active count (not done or contaminated)
        cursor.execute("""
            SELECT COUNT(*) FROM experiments
            WHERE status NOT IN ('done', 'contaminated')
        """)
        active_count = cursor.fetchone()[0]

        # Contaminated count
        cursor.execute("SELECT COUNT(*) FROM experiments WHERE status = 'contaminated'")
        contaminated_count = cursor.fetchone()[0]

        # Success rate (non-contaminated / total * 100)
        if total_count > 0:
            success_rate = ((total_count - contaminated_count) / total_count) * 100
        else:
            success_rate = 0.0

    return {
        'total_count': total_count,
        'active_count': active_count,
        'contaminated_count': contaminated_count,
        'success_rate': round(success_rate, 1)
    }
