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

    response = muterun_js(json_url_path, network_type, tx_file_name + '.json')
    url = response.stdout.decode("utf-8").replace("\n", "")

    #response = execute_js(json_root, tx_file_name + '.json')

    print(url)

    img = qrcode.make(url)
    type(img)  # qrcode.image.pil.PilImage
    img.save(tx_file_name + '.png')

    return tx_file_name + '.png'



  
    
