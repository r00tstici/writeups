#!/usr/bin/env bash

OUTSTANDING_LOG="/InvoiceApp/accounting/outstanding-invoices.log"
SETTLED_LOG="/InvoiceApp/accounting/settled-invoices.log"

[ -f $OUTSTANDING_LOG ] && mv ${OUTSTANDING_LOG}{,$(date +%d-%m-%Y-%H-%M-%S)}
[ -f $SETTLED_LOG ] && mv ${SETTLED_LOG}{,$(date +%d-%m-%Y-%H-%M-%S)}
echo "Files rotated."
