import os
import secrets
import string
import subprocess


import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

def set_payment_image(image1, image_file=ROOT_DIR + '/static/m2tec_logo_github.png'):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_file)
    pixbuf = pixbuf.scale_simple(380, 380, GdkPixbuf.InterpType.BILINEAR)
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



