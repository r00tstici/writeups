import psycopg2
import os
from psycopg2 import sql

"""
Helper functions for communication with the main app database.
"""

CONNECTION_STRING = f"dbname='service' user='ringring' host='{os.environ['PGHOST']}' password={os.environ['PGPASSWORD']}"


def get_alarms(session_id):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    SELECT alarm_text, alarm_time FROM ringring.alarms
    WHERE session_id = {session_id}
    """).format(session_id=sql.Literal(session_id))
    cur.execute(query)
    data = []
    for result in cur.fetchall():
        data.append({'text': result[0],
                     'time': result[1]})
    conn.commit()
    conn.close()

    return data


def get_paying_sessions():
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    SELECT * FROM ringring.sessions WHERE session_id NOT IN 
        (SELECT session_id FROM ringring.sessions WHERE NOT is_billable AND is_vip)
        ORDER BY started DESC 
        LIMIT 1000;
    """)
    cur.execute(query)
    data = [{'guest_id': row[0]} for row in cur.fetchall()]
    conn.commit()
    conn.close()

    return data


def insert_alarm(session_id, time, text):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    INSERT INTO ringring.alarms (session_id, alarm_time, alarm_text) 
    VALUES (%s, %s, %s);
    """)
    cur.execute(query, (session_id, time, text))
    conn.commit()
    conn.close()


def update_invoicing(vips_are_billable=False):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    try:
        query = sql.SQL("""
        UPDATE ringring.sessions SET is_billable = (%s) WHERE is_vip = TRUE;
        """)
        cur.execute(query, [vips_are_billable])
    except (psycopg2.ProgrammingError, psycopg2.errors.CheckViolation):
        conn.rollback()
        return False
    conn.commit()
    conn.close()
    return True


def make_vip(session_id):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = """
    DELETE FROM ringring.sessions WHERE session_id = (%s);
    INSERT INTO ringring.sessions (session_id, is_billable, is_vip) VALUES (%s, %s, %s);
    """
    cur.execute(query, [session_id, session_id, False, True])
    conn.commit()
    conn.close()


def add_session(session_id):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = """
    INSERT INTO ringring.sessions (session_id) VALUES (%s);
    """
    cur.execute(query, [session_id])
    conn.commit()
    conn.close()
