#!/bin/python3

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

import os
import secrets
import string
import subprocess
import locale
import platform
import json

import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf  # NOQA

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
HOME_DIR = os.path.expanduser('~')


def get_config_data():
    try:
        if platform.machine() == 'x86_64':
            config_folder = HOME_DIR + "/.config/m2-kiosk/"
        else:
            #config_folder = "/var/www/m2-kiosk/.config/"
            config_folder = HOME_DIR + "/.config/m2-kiosk/"
            
        # print(config_folder)
        config_file = "config.json"
        f = open(config_folder + config_file)
        config_data = json.load(f)
        f.close()
    except FileNotFoundError:
        print("Config file not found: " + config_folder + config_file)
    return config_data


def set_payment_image(image1, image_data='' ):

    if image_data == '':
        image_file=ROOT_DIR + '/static/m2tec_logo.svg'
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_file)
    else:
        loader = GdkPixbuf.PixbufLoader()
        loader.write(image_data)
        loader.close()
        pixbuf = loader.get_pixbuf()


    #pixbuf = pixbuf.scale_simple(480, 480, GdkPixbuf.InterpType.BILINEAR)
    image1.set_from_pixbuf(pixbuf)
    
def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def check_odoo_and_cardano(odoo_port, wallet_port):

    # Check if Odoo is running
    if is_port_in_use(int(odoo_port)):
        print("Connecting to Odoo on port: " + str(odoo_port))
    else:
        print("Make sure Odoo is running on port: " + str(odoo_port))
        quit()

    # Check if Cardano wallet backend is running
    if is_port_in_use(int(wallet_port)):
        print("Connecting to Cardano wallet backend on port: " + str(wallet_port))
    else:
        print("Make sure the Cardano wallet backend is running on port: " + str(wallet_port))
        quit()
