CREATE SCHEMA IF NOT EXISTS invoices;

CREATE TABLE IF NOT EXISTS invoices.invoices
(
    invoice_number text,
    item text,
    name text,
    time timestamptz,
    amount numeric,
    note text,
    paid boolean
);

CREATE INDEX IF NOT EXISTS invoice_idx ON invoices.invoices(name, invoice_number);
CREATE INDEX IF NOT EXISTS invoicenumber_idx ON invoices.invoices(invoice_number);
