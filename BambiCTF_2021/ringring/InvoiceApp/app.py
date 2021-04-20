from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask_table import Table, Col
from urllib.parse import urlparse
from pathlib import Path
import logging.config
import secrets
import yaml
import json
import sys
from utils import invoice_db_helper
import datetime

ACCOUNT = 5
PAYMENT_ON_ACCOUNT = 'room-bill'
PAYMENT_SETTLED = 'cash'
OUTSTANDING_INVOICES = 'accounting/outstanding-invoices.log'
SETTLED_INVOICES = 'accounting/settled-invoices.log'

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class InvoiceFilter:
    def __init__(self, payment_type, invoice_status):
        """
        Custom logging filter.

        :param payment_type:
        :param invoice_status:
        """
        self.payment_type = payment_type
        self.invoice_status = invoice_status

    @staticmethod
    def get_invoice_status(payment_type):
        if payment_type == 'cash' or payment_type == 'debit':
            return 'settled'
        else:
            return 'outstanding'

    def filter(self, logRecord):
        return logRecord.levelno == ACCOUNT and self.get_invoice_status(self.payment_type) == self.invoice_status


@app.route('/')
def home():
    """
    Main entry point for the invoice app. Returns all invoices for a specific guest.

    :return:
    """
    guest_name = request.args.get('name')
    if not guest_name:
        return param_error('guest_name')

    log_level = request.args.get('log-level', 'DEBUG')
    controller = get_invoice_controller(log_level=log_level)
    controller.info(log_level)

    controller.info(f"Generating invoice overview for guest '{guest_name}'...")
    guest_invoices = invoice_db_helper.get_invoices_from_guest(guest_name)
    response = json.dumps({'invoices': guest_invoices, 'success': True}, default=str)
    return response


@app.route('/add', methods=['POST'])
def add_to_bill():
    """
    Endpoint to add an item to the invoice. Adds it both to the db as well as to the logfile.

    :return:
    """
    guest_name = request.form.get('name')
    if not guest_name:
        return param_error('name')

    invoice_item = request.form.get('item')
    if not invoice_item:
        return param_error('item')

    payment_type = request.form.get('payment-type', PAYMENT_ON_ACCOUNT)
    note = request.form.get('note', '')

    if not validate_invoice(guest_name, invoice_item):
        logger.warning(
            f"Aborting invoice accounting - invoice parameters guest name '{guest_name}' and item '{invoice_item}' are not valid (HTTP 404).")
        return jsonify(success=False), 400

    amount = get_price(invoice_item)
    invoice_number = get_invoice_number()
    invoice = {
        'invoice_number': invoice_number,
        'item': invoice_item,
        'guest_name': guest_name,
        'amount': amount,
        'note': note
    }
    controller = get_invoice_controller(payment_type=payment_type)
    controller.account(f'invoice #{invoice_number} accounted', extra=invoice)
    if payment_type == PAYMENT_SETTLED:
        paid = True
    else:
        paid = False

    invoice_db_helper.insert_invoice(invoice_number, invoice_item, guest_name, datetime.datetime.now(), amount, note,
                                     paid)
    return jsonify(success=True, invoice_number=invoice_number)


@app.route('/storno', methods=['POST'])
def storno():
    """
    Endpoint to delete an invoice from the db. Invoice will remain in the logfile.

    :return:
    """
    invoice_number = request.form.get('number')
    if not invoice_number:
        return param_error('number')

    if invoice_db_helper.delete_invoice(invoice_number):
        return jsonify(success=True)
    else:
        logger.warning(
            f"Something went wrong with your request.")
        return jsonify(success=False), 400


@app.route('/request-bill')
def request_bill():
    """
    Requesting the bill for a guest and marking respective invoices as payed.
    :return:
    """
    guest_name = request.args.get('name')
    if not guest_name:
        return param_error('name')

    logger.info(f"Requesting bill for guest '{guest_name}'...")

    total = invoice_db_helper.set_invoices_paid(guest_name)
    logger.info(f"{guest_name} payed total amount of {total}")
    if total or total == 0:
        response = json.dumps({'total': total, 'sucess': True}, default=str)
        return response
    else:
        return jsonify(success=False), 400


@app.route('/invoice_details')
def invoice_details():
    """
    Return full invoice details for an invoice number. Needs both the invoice number and the guest name.
    :return:
    """
    invoice_number = request.args.get('invoice_number')
    if not invoice_number:
        return param_error('invoice_number')

    guest_name = request.args.get('guest_name')
    if not guest_name:
        return param_error('guest_name')

    logger.info(f"Requesting invoice '{invoice_number}'...")

    invoice = invoice_db_helper.get_invoice_by_number(guest_name, invoice_number)

    logger.info(f"returning invoice information: {invoice}")

    response = json.dumps({'invoice': invoice, 'success': True}, default=str)
    return response


def validate_invoice(guest_name, invoice_item):
    return guest_name and invoice_item


def get_price(item):
    price_sheet = {
        'alarm': 1.50,
        'pizza': 6.00,
        'bread': 2.00,
        'fish': 15.00,
        'wine': 4.00,
        'room-service-food': 9.99,
        ''
        'reception': 0.0,
        'extra-cleaning': 20.0
    }
    return price_sheet.get(item, 0)


def get_invoice_number():
    return secrets.randbits(64)


def get_invoice_controller(payment_type=PAYMENT_ON_ACCOUNT, log_level='ACCOUNT'):
    """
    Helper function to return the correct logger.
    :param payment_type:
    :param log_level:
    :return:
    """
    with open('logger-config.yml', 'r') as yaml_file:
        config = yaml_file.read().format(payment_type=payment_type, level=log_level)
        config = yaml.load(config, Loader=yaml.Loader)
        logging.addLevelName(ACCOUNT, 'ACCOUNT')
        logging.config.dictConfig(config)
        logging.Logger.account = account
        logger = logging.getLogger('invoice_controller')
        # logger.debug('invoice-controller logger started.')
    return logger


def account(self, msg, *args, **kwargs):
    if self.isEnabledFor(ACCOUNT):
        self._log(ACCOUNT, msg, args, **kwargs)


def start_app(host):
    app.run(port=7354, host=host, debug=False)


def param_error(name):
    """
    Helper function for error handling on request parameters.

    :param name:
    :return:
    """
    return jsonify(success=False, message=f"missing parameter {name}"), 400


if __name__ == '__main__':
    start_app(host='0.0.0.0')
