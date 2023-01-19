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

from Naked.toolshed.shell import execute_js, muterun_js
import qrcode


def cardano_transaction_json(transaction_id, wallet_address, amount):
    metadata_dict = {
        '123': {'message': transaction_id}
    }
    amounts_dict_1 = {
        'quantity': str(int(amount)),
        'policyId': 'ada',
        'assetName': 'ada'
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


def qr_code(network_type, transaction_id, wallet_address, amount):
    print('-------- qr_code ----------')
    
    tx_json = cardano_transaction_json(transaction_id, wallet_address, amount)
    
    tx_file_name = '/tmp/shop_data-' + transaction_id
    
    with open(tx_file_name + '.json', 'w') as outfile:
        json.dump(tx_json, outfile)
    
    #print()
    #print(tx_json)
    #print(type(tx_json))
    
    #network_type = 'testnet'
    
    # npm gamechanger-dapp-cli - this is very slow
    #gc_cli = 'gamechanger-dapp-cli'
    #command_list = [gc_cli, network_type, 'build', '--template', 'printable', 'qr', '-a', tx_json, '-o', tx_file_name + '.png']
    #command_string = ' '.join(command_list)
    #print(command_string)
    #result = subprocess.run(command_list, stdout=subprocess.PIPE)

    tx_file_name = '/tmp/shop_data-' + transaction_id
    print(tx_file_name)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    json_url_path = ROOT_DIR + '/../json-url-reduced/json-url-reduced.js'

    # Generate qr code 
    print('json file: \t' + tx_file_name + '.json')
    tx_file_name_json = tx_file_name + '.json'
    arg_in = f"{network_type} {tx_file_name_json}"

    response = muterun_js(json_url_path, arg_in)
    url = response.stdout.decode("utf-8").replace("\n", "")

    #response = execute_js(json_root, tx_file_name + '.json')

    print(url)

    img = qrcode.make(url)
    type(img)  # qrcode.image.pil.PilImage
    img.save(tx_file_name + '.png')

    return tx_file_name + '.png'



  
    
