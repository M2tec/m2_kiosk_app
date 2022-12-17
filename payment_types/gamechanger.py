import json
import subprocess
import requests
from pprint import pprint

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


def qr_code(tx_file_name, transaction_id, wallet_address, amount):
    print('-------- qr_code ----------')
    
    tx_json = cardano_transaction_json(transaction_id, wallet_address, amount)
    
    with open(tx_file_name + '.json', 'w') as outfile:
        json.dump(tx_json, outfile)
    
    #print()
    #print(tx_json)
    #print(type(tx_json))
    
    cardano_net = 'testnet'
    
    # npm gamechanger-dapp-cli - this is very slow
    #gc_cli = 'gamechanger-dapp-cli'
    #command_list = [gc_cli, cardano_net, 'build', '--template', 'printable', 'qr', '-a', tx_json, '-o', tx_file_name + '.png']
    #command_string = ' '.join(command_list)
    #print(command_string)
    #result = subprocess.run(command_list, stdout=subprocess.PIPE)
    
    
    
    # Generate qr code 
    print(tx_file_name + '.json')
    response = muterun_js('json-url-reduced/json-url-reduced.js', tx_file_name + '.json')
    #response = execute_js('json-url-reduced/json-url-reduced.js', tx_file_name + '.json')
    #print(response)
    url = response.stdout.decode("utf-8").replace("\n", "")

    print(url)

    img = qrcode.make(url)
    type(img)  # qrcode.image.pil.PilImage
    img.save(tx_file_name + '.png')




  
    
