import logging
import requests
import hashlib
import os

"""
Helper functions for communication with the invoice service.
"""


PAYMENT_ON_ACCOUNT = 'room-bill'

logger = logging.getLogger('RingRing')


def add_to_invoice(guest_name, service, payment_type=PAYMENT_ON_ACCOUNT, notes=None):
    session = requests.session()
    if 'INVOICE_HOST' not in os.environ:
        logger.error(f'Could not create invoice for {service} for {guest_name}. INVOICE_HOST variabe is missing.')
        return

    guest_pseudonym = hashlib.md5(guest_name.encode('utf-8')).hexdigest()
    url = 'http://' + os.environ['INVOICE_HOST'] + ':7354/add'
    params = {'name': guest_pseudonym, 'item': service, 'payment-type': payment_type, 'note': notes}
    resp = session.post(url, data=params)
    return resp.json()['invoice_number']


def get_invoices(guest_name):
    session = requests.session()
    if 'INVOICE_HOST' not in os.environ:
        logger.error(f"Could not get invoice for '{guest_name}''. INVOICE_HOST variabe is missing.")
        return []
    if not guest_name:
        logger.warning(f"Abort getting invoice overview - mandatory parameter guest name '{guest_name}' is not set.")
        return []
    guest_pseudonym = hashlib.md5(guest_name.encode('utf-8')).hexdigest()
    url = 'http://' + os.environ['INVOICE_HOST'] + ':7354/'
    response = session.get(url, params={'name': guest_pseudonym})
    if response.status_code != 200:
        return []

    invoices = response.json()['invoices']
    for invoice in invoices:
        invoice['name'] = guest_name

    logger.info(f"Got invoice for guest {guest_name}: {invoices}")
    return invoices


def request_bill(guest_name):
    session = requests.session()
    if 'INVOICE_HOST' not in os.environ:
        logger.error(f"Could not get invoice for '{guest_name}''. INVOICE_HOST variabe is missing.")
        return [], None
    if not guest_name:
        logger.warning(f"Abort getting invoice overview - mandatory parameter guest name '{guest_name}' is not set.")
        return [], None
    guest_pseudonym = hashlib.md5(guest_name.encode('utf-8')).hexdigest()
    url = 'http://' + os.environ['INVOICE_HOST'] + ':7354/request-bill'
    response = session.get(url, params={'name': guest_pseudonym})
    if response.status_code != 200:
        logger.warning(f"Request to {url} with did not return successfully.")
        return {}
    data = response.json()
    return data['total']


def get_invoice_by_invoice_number(invoice_number, session_id):
    session = requests.session()
    guest_pseudonym = hashlib.md5(session_id.encode('utf-8')).hexdigest()
    if 'INVOICE_HOST' not in os.environ:
        logger.error(f'Could not get invoice {invoice_number}. INVOICE_HOST variabe is missing.')
        return []
    if not invoice_number:
        logger.warning("No invoice number provided.")
        return []

    url = 'http://' + os.environ['INVOICE_HOST'] + ':7354/invoice_details'
    params = {'invoice_number': invoice_number, 'guest_name': guest_pseudonym}
    response = session.get(url, params=params)

    if response.status_code != 200:
        try:
            response_text = response.text
        except:
            response_text = ""
        logger.warning(
            f"Request to {url} with params {params} did not return successfully. Return code: {response.status_code}. Response_text {response_text}")
        return {}
    invoice = response.json()['invoice']

    return invoice
