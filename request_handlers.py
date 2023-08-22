#!/usr/bin/python3

#
# This file is part of the m2-kiosk-app distribution (https://github.com/M2tec/m2_kiosk_app).
# Copyright (c) 2023 Maarten Menheere.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import json
from pprint import pprint

from m2_util import *
from payment_types import *
from payment_validators import *

import gi
gi.require_version('Gdk', '3.0')
gi.require_version("Gtk", "3.0")
gi.require_version('Soup', '2.4')
from gi.repository import Gio, GLib, Gdk, Gtk, GdkPixbuf, Soup  # NOQA

def pretty_print_json(ugly_json):  
    parsed_json = json.loads(ugly_json)
    pretty_json = json.dumps(parsed_json, indent=4)
    print(pretty_json)

def remove_child_widget(server):
    child_widgets = server.window1.get_children()
    for w in child_widgets:
        widget_type = type(w).__name__
        if widget_type == 'Box':
            child_widget = w
               
    server.window1.remove(child_widget)

if platform.machine() == 'x86_64':
    config_folder = HOME_DIR + "/.config/m2-kiosk/"
else:
#    config_folder = "/var/www/m2-kiosk-web/.config/"
    config_folder = HOME_DIR + "/.config/m2-kiosk/"
    
    
config_file = "config.json"


def get_config():
    try:
        f = open(config_folder + config_file)
        config_data = json.load(f)
        f.close()
        create_config = False
    except FileNotFoundError:
        print("Config file not found: " + config_folder + config_file)
        create_config = True
    except json.decoder.JSONDecodeError:
        print("Config file not readable " + config_folder + config_file)
        create_config = True

    if create_config:
        try:
            print("Creating new config file")
            print(config_folder)
            os.makedirs(config_folder, exist_ok=True)
        except OSError as error:
            print(error)

        try:
            print("Reading config file")
            f = open("/usr/local/share/m2-kiosk-app-hyper/m2_config_template.json", "r")
            template_data = f.read()
            f.close()
            print(template_data)
        except FileNotFoundError:
            print("Template file not found")

        try:
            f = open(config_folder + config_file, "w")
            f.write(template_data)
            f.close()
        except OSError as e:
            print(e)

        try:
            f = open(config_folder + config_file)
            config_data = json.load(f)
            f.close()
        except OSError as e:
            print(e)
    return config_data


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
    pretty_print_json(message.request_body.data)
    print()
    
    try:
        json_dict = json.loads(message.request_body.data)
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
    #print(json_dict)
    remove_child_widget(server)
    server.window1.add(server.payment_main_box)
    server.window1.show_all()

    requested_amount = float(json_dict["amount"])
    token_name = json_dict["token_name"]
    
    tx_file_name = gamechanger.qr_code(json_dict)

    # Set QR code image
    set_payment_image(server.payment_image, tx_file_name)

    config_data = get_config()
    locale_setting = config_data["globals"]["locale_setting"]
    locale.setlocale(locale.LC_ALL, locale_setting)

    requested_amount = locale.format_string('%.2f', requested_amount, grouping=True)
    server.token_name.set_text(token_name)
    
    server.payment_label.set_text(requested_amount)
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

    remove_child_widget(server)
    server.window1.add(server.start_main_box)
    server.window1.show_all()
       
    # HTTP Response
    cors_local_url = check_cors_origin(message)
    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    print("Cors local url: \t" + cors_local_url)
    # Send answer to paypad

    message.set_status(200)
    
    
# Save configuration
def save_configuration_request(server, message, path, query, client_context, data):

    try:
        config_data = json.loads(message.request_body.data)
        pprint(config_data)
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        return    

    with open(config_folder + config_file, 'w') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)

    # HTTP Response
    cors_local_url = check_cors_origin(message)
    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    print("Cors local url: \t" + cors_local_url)
    # Send answer to paypad

    message.set_status(200)  
     
     
# Load configuration
def load_configuration_request(server, message, path, query, client_context, data):

     # HTTP Response
    cors_local_url = check_cors_origin(message)
    message.response_headers.append("Access-Control-Allow-Origin", cors_local_url)
    print("Cors local url: \t" + cors_local_url)

    config_data = json.dumps(get_config())
    #print(type(config_data))
    message.set_status_full(200, config_data)
    message.set_response('text/plain', Soup.MemoryUse.COPY, config_data.encode('utf-8'))
    # Send answer to paypad
    
    
    
