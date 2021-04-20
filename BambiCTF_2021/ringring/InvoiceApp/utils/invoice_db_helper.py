import psycopg2
import os
from psycopg2 import sql
import logging
import sys

"""
Helper functions for communication with the invoice app database.
"""


CONNECTION_STRING = f"dbname='invoice' user='ringring' host='{os.environ['PGHOST']}' password={os.environ['PGPASSWORD']}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def set_invoices_paid(guest_name):
    get_du_amount = sql.SQL("""SELECT SUM(amount) FROM invoices.invoices
    WHERE name = {guest_name} AND paid = FALSE ;""").format(guest_name=sql.Literal(guest_name))
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute(get_du_amount)
    total_amount = cur.fetchone()[0]
    if not total_amount:
        total_amount = 0
    conn.commit()
    conn.close()

    query = sql.SQL("""UPDATE invoices.invoices SET paid = TRUE 
    WHERE name = {guest_name};""").format(guest_name=sql.Literal(guest_name))
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        return total_amount

    except psycopg2.ProgrammingError as e:
        logger.warning("something went wrong with the query")
        logger.warning(str(e))
        return


def get_invoice_by_number(guest_name, invoice_number):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    SELECT invoice_number, item, name, amount, note, paid FROM invoices.invoices
    WHERE name = {name} AND invoice_number = {invoice_number};
    """).format(name=sql.Literal(guest_name), invoice_number=sql.Literal(invoice_number))
    cur.execute(query)
    data = []
    for result in cur.fetchall():
        data.append({'invoice_number': result[0],
                     'item': result[1],
                     'name': result[2],
                     'amount': result[3],
                     'note': result[4],
                     'paid': result[5]})
    conn.commit()
    conn.close()

    if len(data) > 1:
        logger.warning(f'Multiple invoices found with the name invoice number: {data}')
    return data[0]


def get_invoices_from_guest(guest_name):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    SELECT item, amount, paid FROM invoices.invoices
    WHERE name = {name};
    """).format(name=sql.Literal(guest_name))
    cur.execute(query)
    data = []
    for result in cur.fetchall():
        data.append({
            'item': result[0],
            'amount': result[1],
            'paid': result[2]})
    conn.commit()
    conn.close()

    return data


def delete_invoice(invoice_number):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    DELETE FROM invoices.invoices WHERE invoice_number = {number};
    
    """).format(number=sql.Literal(invoice_number))
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        return True

    except psycopg2.ProgrammingError:
        return False


def insert_invoice(invoice_number, item, name, time, amount, note, paid):
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    query = sql.SQL("""
    INSERT INTO invoices.invoices (invoice_number, item, name, time, amount, note, paid) 
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """)
    cur.execute(query, (invoice_number, item, name, time, amount, note, paid))
    conn.commit()
    conn.close()
