import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk, GdkPixbuf

# Thanks to  Gio test files at GNOME repo: glib/blob/master/gio/tests/gdbus-example-server.c
# Generating interface from XML is easy. Look at the above file on how it is done.
# A better resource : http://maemo.org/maemo_training_material/maemo4.x/html/
#                     maemo_Platform_Development_Chinook/
#                     Chapter_03_Using_the_GLib_wrappers_for_DBus.html
#                     #DBusinterfacedefinitionusingXML

xml = (
    "<node>"
    "  <interface name='org.m2tec.paypad'>"
    "    <method name='PollAlive'>"
    "      <arg type='s' name='msg' direction='in'/>"
    "      <arg type='s' name='serviceId' direction='out'/>"
    "    </method>"
    "    <method name='SetPayment'>"
    "      <arg type='s' name='transactionId' direction='in'/>"
    "      <arg type='s' name='walletAddress' direction='in'/>"
    "      <arg type='s' name='payAmount' direction='in'/>"
    "      <arg type='s' name='ServiceId' direction='in'/>"
    "      <arg type='s' name='greeting' direction='out'/>"
    "    </method>"
    "    <method name='Quit'/>"
    "  </interface>"
    "</node>"
)

node = Gio.DBusNodeInfo.new_for_xml(xml)  # We make a node for the xml
#loop = GLib.MainLoop() # A loop to handle API

def handle_method_call(
        connection, sender, object_path, interface_name, method_name, params, invocation
):
    """
    This is the top-level function that handles all the method calls to our server.
    The first four parameters are self-explanatory.
    `method_name` is a string that describes our method name.
    `params` is a GLib.Variant that are inputs/parameters to the method.
    `invocation` is a Gio.DBusMethodInvocation, something like a messenger that transports
    our reply back to sender.
    """

    print("CALLED")
    # We need to unpack GLib.Variant to a Python object. The unpacked one is always a
    # tuple.
    if method_name == "PollAlive":
        msg = params.unpack()[0]  # First argument is what we need
        print(f"FROM {sender} : {msg}")

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        # print("date and time =", dt_string)

        service_id = GLib.Variant("(s)", (f"sID-{dt_string}",))
        invocation.return_value(service_id)  # Nothing to say, so just return None.

        # Send the answer as a http request to Odoo
        TIMEOUT = 10
        endpoint = 'http://localhost:' + odoo_port + '/pos_cardano/notification'

        headers = {
            'Content-Type': 'application/json'
        }

        diagnosis_data = {
            "SaleToPOIResponse": {"DiagnosisResponse": {"HostDiagnosisFlag": False},
                                  "MessageHeader": {"MessageCategory": "Diagnosis",
                                                    "MessageClass": "Service",
                                                    "MessageType": "Response",
                                                    "POIID": "Terminal1",
                                                    "ProtocolVersion": "3.0",
                                                    "SaleID": "Shop (Mitchell Admin) (ID: "
                                                              "1)",
                                                    "ServiceID": "sID-" + dt_string}}}

        request_odoo = requests.post(endpoint, data=json.dumps(diagnosis_data), headers=headers, timeout=TIMEOUT)


    elif method_name == "SetPayment":
        transaction_id = params.unpack()[0]
        wallet_id = params.unpack()[1]
        pay_amount = float(params.unpack()[2])
        service_id = params.unpack()[3]

        print(f"FROM {sender} : CONFIRMED {pay_amount}")
        greeting = GLib.Variant(
            "(s)", (f"Amount set to: {pay_amount}",)
        )  # All form of return should be a
        # variant.
        invocation.return_value(greeting)

        wallet = Wallet(wallet_id, backend=WalletREST(port=8090))
        wallet_address = str(wallet.first_unused_address())
        print(wallet_address)

        create_qr_code(transaction_id, wallet_address, pay_amount)

        qr_code_file_name = 'static/shop_qr_code-' + transaction_id + '.png'
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(qr_code_file_name)
        pixbuf = pixbuf.scale_simple(380, 380, GdkPixbuf.InterpType.BILINEAR)
        image1.set_from_pixbuf(pixbuf)

        amount_label.set_text("{:.2f}".format(pay_amount))

        check_blockchain.count = 0
        print(transaction_id + ' ' + service_id)
        GLib.timeout_add(5000, check_blockchain, transaction_id, service_id, wallet_id)

    elif method_name == "Quit":
        loop.quit()
        invocation.return_value(None)


def on_bus_acquired(connection, name):

    """
    The function that introduces our server to the world. It is called automatically
    when we get the bus we asked.
    """

    # Remember the node we made earlier? That has a list as interfaces attribute.
    # From that get our interface. We made only one interface, so we get the first
    # interface.

    print("Bus acquired for name, ", name)
    reg_id = connection.register_object(
        "/org/m2tec/paypad", node.interfaces[0], handle_method_call, None, None
    )


def on_name_acquired(connection, name):

    """
    What to do after name acquired?
    """

    print("Name acquired :", name)


def on_name_lost(connection, name):

    """
    What to do after our name is lost? May be just exit.
    """

    print("Name lost :", name)
    exit(0)