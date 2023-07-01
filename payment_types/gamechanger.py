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
import subprocess
import requests
from pprint import pprint
import os

import qrcode
import qrcode.image.svg

import json
import brotli
import base64

def base64_encode(string):
    """
    Removes any `=` used as padding from the encoded string.
    """
    encoded = base64.urlsafe_b64encode(string)
    return encoded.rstrip(b"=").rstrip(b"\n")


def base64_decode(string):
    """
    Adds back in the required padding before decoding.
    """
    padding = 4 - (len(string) % 4)
    string = string + (b"=" * padding)
    return base64.urlsafe_b64decode(string)

def json_deindent(data):
    #data = json.loads(data)
    data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return data

def gc_encode(gc_script):
    json_string = json_deindent(gc_script)
    brotli_data = brotli.compress(json_string.encode())
    url_string = base64_encode(brotli_data)
    return url_string.decode()

def gc_decode(url_string):
    brotli_data = base64_decode(url_string.encode())
    json_string = brotli.decompress(brotli_data)
    return json_string.decode()


def cardano_transaction_json(json_dict):

    network_type = json_dict["network_type"]
    wallet_address = json_dict["wallet_address"]
    transaction_id = str(json_dict["transaction_id"])
    token_policyID = json_dict["token_policyID"]
    token_name = json_dict["token_name"]
    requested_amount = float(json_dict["amount"]) * 1000000

    metadata_dict = {
        '123': {'message': transaction_id}
    }
    amounts_dict_1 = {
        'quantity': str(int(requested_amount)),
        'policyId': token_policyID,
        'assetName': token_name
    }

    amounts_list = [amounts_dict_1]

    outputs_dict = {
        wallet_address: amounts_list
    }

    transaction_dict = {
        'type': 'tx',
        'title': transaction_id,
        'description' : 'M2tec POS transaction',
        'outputs': outputs_dict,
    }

    #print(json.dumps(transaction_dict, indent=4, sort_keys=True))


    return transaction_dict


def qr_code(json_dict):
    print('-------- qr_code ----------')
    print(json_dict)      
    network_type = json_dict["network_type"]
    transaction_id = str(json_dict["transaction_id"])
    
    tx_json = cardano_transaction_json(json_dict)
  
    # Generate qr code 
    url = gc_encode(tx_json)

    print("URL:" + url)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=22,
        border=2,
        image_factory=qrcode.image.svg.SvgPathFillImage
    )

    qr.add_data(url)
    qr.make()
    img = qr.make_image(back_color="white")
    
    return img.to_string()



  
    
