from gi.repository import Gio, GLib, Gdk, Gtk, GdkPixbuf
import json
from pprint import pprint

from m2_util import *
from payment_types import *
from payment_validators import *

import gi
gi.require_version('Gdk', '3.0')
gi.require_version("Gtk", "3.0")
gi.require_version('Soup', '2.4')


def check_cors_origin(message):
    # Set the cors header

    # Match origin to localhost
    allow_list = ['m2-paypad', 'localhost', '127.0.0.1', 'm2paypad.home']
    origin = message.request_headers.get_list("Origin")
    # print("Origin: " + str(origin))

    cors_local_url = ""
    if origin is None:
        cors_local_url = "http://localhost/"
    else:
        for allow_url in allow_list:
            if allow_url in origin:
                # cors_local_url = "http://" + allow_url + ":5000"
                cors_local_url = "http://" + allow_url

    return cors_local_url

# Handle payment request for the gamechanger wallet
def payment_request(server, message, path, query, client_context, data):
    print('-------- payment request ----------')

    try:
        json_dict = json.loads(message.request_body.data)
        # print()
        # pprint(repr(json_dict))
        # print()
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        return

    payment_request_simple(server, json_dict)

    # HTTP Response
    cors_local_url = check_cors_origin(message)
    # print("Cors_local_url: " + cors_local_url)
    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    message.set_status(200)


def payment_request_simple(server, json_dict):
    print("payment_request_simple")

    server.window1.remove(server.start_main_box)
    server.window1.add(server.payment_main_box)
    server.window1.show_all()

    transaction_id = str(json_dict["transaction_id"])
    requested_amount = float(json_dict["amount"])
    wallet_address = json_dict["wallet_address"]

    print(transaction_id)
    # Create a Gamechanger QR-code
    tx_file_name = '/tmp/shop_data-' + transaction_id
    print(tx_file_name)
    gamechanger.qr_code(
        tx_file_name, transaction_id, wallet_address, int(
            requested_amount * 1000000))

    # Set QR code image
    set_payment_image(server.payment_image, tx_file_name + '.png')
    server.payment_label.set_text("{:.2f}".format(requested_amount))
    server.window1.show_all()

# Handle payment status for the gamechanger wallet
def payment_status(server, message, path, query, client_context, data):
    print('-------- payment status ----------')

    try:
        json_dict = json.loads(message.request_body.data)
        pprint(json_dict)
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        return

    transaction_id = json_dict["transaction_id"]
    requested_amount = json_dict["amount"]
    wallet_address = json_dict["wallet_address"]
    network_type = json_dict["network_type"]

    payment_status = koios.payment_validate(
        network_type, transaction_id, wallet_address, requested_amount)
    # payment_status = dummy.payment_validate(network_type, transaction_id, wallet_address, requested_amount)

    print("Koios return: " + repr(payment_status))

    tx_json = {"network_type": network_type,
               "transaction_id": transaction_id,
               "wallet_address": wallet_address,
               "requested_amount": requested_amount,
               "payment_status": payment_status
               }

    cors_local_url = check_cors_origin(message)

    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    print("Cors local url: \t" + cors_local_url)

    message.set_status_full(200, payment_status)
    message.set_response('text/plain', Soup.MemoryUse.COPY, payment_status.encode('utf-8'))


# Handle payment request to clear the window
def clear_display_request(server, message, path, query, client_context, data):

    # Update UI
    set_payment_image(server.payment_image)
    server.payment_box.hide()

    # HTTP Response
    cors_local_url = check_cors_origin(message)
    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    print("Cors local url: \t" + cors_local_url)
    # Send answer to paypad

    message.set_status(200)
